#!/usr/bin/env python3
"""
Terminus 3 task validator.

Mechanically checks a task folder against the objective, machine-checkable
rules in REGULATIONS.md. This is a *first pass*, not a substitute for the
human/LLM-as-Judge review described in checklists/ — it only catches what
can be verified without judgment (files present, syntax, pinning, canary
strings, etc). Anything requiring judgment (novelty, whether difficulty is
legitimate, whether the verifier is semantically deep, instruction tone) is
explicitly out of scope and flagged as "MANUAL" so it isn't silently
skipped.

Usage:
    python3 tools/validate_task.py /path/to/task-folder
    python3 tools/validate_task.py /path/to/task-folder --strict   # non-zero exit on any WARN too

Design goals (why this file exists, not just the checklists/ markdown):
- Generic and reusable: takes any task folder, no task-specific assumptions.
- Safe to run repeatedly during authoring, not just before submission.
- Fails loudly on missing/malformed required structure, but never invents
  or auto-fixes content — it only reports.
- No third-party dependencies (stdlib only) so it runs anywhere this kit is
  used, including inside a build/CI step later if one is wired up.

This script intentionally does NOT:
- Judge novelty, task quality, or difficulty legitimacy (see checklists/01,
  02, and difficulty_calibration/).
- Run `stb harbor ...` commands (see checklists/10) — that requires the
  actual Terminus 3 CLI/tooling, which this kit does not assume is present.
- Inspect oracle/verifier *semantics* (whether tests actually validate the
  right thing) — only their syntactic/structural compliance.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback for older Python
    tomllib = None


PASS, WARN, FAIL, MANUAL, SKIP = "PASS", "WARN", "FAIL", "MANUAL", "SKIP"

REQUIRED_FILES = [
    "task.toml",
    "instruction.md",
    "environment/Dockerfile",
    "solution/solve.sh",
    "tests/Dockerfile",
    "tests/test.sh",
    "tests/test_outputs.py",
]

# Files that must exist for authoring convenience but must NOT ship in the
# final submission ZIP (REGULATIONS.md §4/§12). The validator only warns
# about these when run in --pre-submission mode against the actual archive
# contents; against a working folder they're expected to exist.
EXCLUDED_FROM_SUBMISSION = ["README.md", "rubrics.txt"]

REQUIRED_TOML_FIELDS = [
    "name", "category", "subcategory", "tags", "languages", "difficulty",
    "expert_time_estimate_hours", "author_name", "author_email", "artifacts",
    "difficulty_explanation", "solution_explanation", "verification_explanation",
    "relevant_experience",
]

VALID_DIFFICULTY_TIERS = {"frontier", "advanced", "core", "base"}
VALID_REWARD_MAGNITUDES = {1, 2, 3, 5}

# Known canary-string markers used across LLM eval ecosystems. Extend this
# list if the live Terminus 3 spec names a specific canary string format.
CANARY_PATTERNS = [
    r"BENCHMARK DATA SHOULD NEVER APPEAR IN TRAINING",
    r"canary[ _-]?string",
    r"\bcanary\b",
]


@dataclass
class Result:
    section: str
    item: str
    status: str
    detail: str = ""


@dataclass
class Report:
    results: list = field(default_factory=list)

    def add(self, section: str, item: str, status: str, detail: str = ""):
        self.results.append(Result(section, item, status, detail))

    def counts(self):
        c = {PASS: 0, WARN: 0, FAIL: 0, MANUAL: 0, SKIP: 0}
        for r in self.results:
            c[r.status] += 1
        return c

    def print_report(self):
        current_section = None
        for r in self.results:
            if r.section != current_section:
                print(f"\n## {r.section}")
                current_section = r.section
            marker = {
                PASS: "[PASS]", WARN: "[WARN]", FAIL: "[FAIL]",
                MANUAL: "[MANUAL]", SKIP: "[SKIP]",
            }[r.status]
            line = f"  {marker} {r.item}"
            if r.detail:
                line += f" — {r.detail}"
            print(line)

        c = self.counts()
        print(
            f"\nSummary: {c[PASS]} pass, {c[WARN]} warn, {c[FAIL]} fail, "
            f"{c[MANUAL]} manual (see checklists/), {c[SKIP]} skipped."
        )
        if c[MANUAL]:
            print(
                "Items marked MANUAL cannot be auto-checked — work through "
                "the matching file in checklists/ by hand or via LLM-as-Judge review."
            )


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def check_required_files(task_dir: Path, report: Report):
    section = "Required Files & Packaging (REGULATIONS.md §4)"
    for rel in REQUIRED_FILES:
        p = task_dir / rel
        if p.exists():
            report.add(section, rel, PASS)
        else:
            report.add(section, rel, FAIL, "missing")

    for rel in EXCLUDED_FROM_SUBMISSION:
        p = task_dir / rel
        if p.exists():
            report.add(
                section, f"{rel} (exclude at packaging time)", WARN,
                "present in working folder — fine for authoring, but must "
                "be stripped from the final submission ZIP (see "
                "checklists/11_submission_packaging.md)",
            )


def scan_canaries(task_dir: Path, report: Report):
    section = "Canary Strings (REGULATIONS.md §1, §3)"
    hits = []
    for p in task_dir.rglob("*"):
        if p.is_dir():
            continue
        # Skip this kit's own docs about canary strings so the validator
        # doesn't flag its own guidance text.
        if p.name == "validate_task.py":
            continue
        text = read_text(p)
        if text is None:
            continue
        for pattern in CANARY_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                hits.append(f"{p.relative_to(task_dir)} matches /{pattern}/")
                break
    if hits:
        for h in hits:
            report.add(section, "no canary strings", FAIL, h)
    else:
        report.add(section, "no canary strings", PASS)


def parse_toml(path: Path):
    text = read_text(path)
    if text is None:
        return None, "file not found or unreadable"
    if tomllib is not None:
        try:
            return tomllib.loads(text), None
        except Exception as e:  # noqa: BLE001
            return None, f"TOML parse error: {e}"
    # Minimal fallback: extremely small subset, only used if tomllib is
    # unavailable (pre-3.11 Python). Not a full TOML parser.
    return None, "tomllib unavailable (Python 3.11+ required for full task.toml validation)"


def check_task_toml(task_dir: Path, report: Report):
    section = "task.toml (REGULATIONS.md §5)"
    data, err = parse_toml(task_dir / "task.toml")
    if data is None:
        report.add(section, "parse task.toml", FAIL if err and "not found" in err else WARN, err or "unknown error")
        return

    for field_name in REQUIRED_TOML_FIELDS:
        if field_name in data and data[field_name] not in (None, "", []):
            report.add(section, f"field `{field_name}` present", PASS)
        else:
            report.add(section, f"field `{field_name}` present", FAIL, "missing or empty")

    tags = data.get("tags")
    if isinstance(tags, list):
        if 3 <= len(tags) <= 6:
            report.add(section, "tags count 3-6", PASS, f"{len(tags)} tags")
        else:
            report.add(section, "tags count 3-6", FAIL, f"{len(tags)} tags")

    difficulty = data.get("difficulty")
    if isinstance(difficulty, str):
        if difficulty.lower() in VALID_DIFFICULTY_TIERS:
            report.add(section, "difficulty is a valid tier", PASS, difficulty)
        else:
            report.add(section, "difficulty is a valid tier", FAIL, f"got '{difficulty}'")

    report.add(
        section, "difficulty tier matches actual task characteristics", MANUAL,
        "see checklists/02_difficulty.md and difficulty_calibration/",
    )

    agent = data.get("agent", {})
    ts = agent.get("timeout_sec")
    if isinstance(ts, (int, float)):
        if ts >= 1800:
            report.add(section, "[agent] timeout_sec >= 1800", PASS, str(ts))
        else:
            report.add(section, "[agent] timeout_sec >= 1800", WARN,
                        f"{ts} — below the 1800s floor most sources agree on; "
                        "see NOTES_ON_CONFLICTS.md item 1")
    else:
        report.add(section, "[agent] timeout_sec set", FAIL, "missing")

    verifier = data.get("verifier", {})
    if isinstance(verifier.get("timeout_sec"), (int, float)):
        report.add(section, "[verifier] timeout_sec set", PASS)
    else:
        report.add(section, "[verifier] timeout_sec set", FAIL, "missing")
    if verifier.get("environment_mode") == "separate":
        report.add(section, '[verifier] environment_mode == "separate"', PASS)
    else:
        report.add(section, '[verifier] environment_mode == "separate"', FAIL,
                    f"got {verifier.get('environment_mode')!r}")

    env = data.get("environment", {})
    if isinstance(env.get("build_timeout_sec"), (int, float)):
        report.add(section, "[environment] build_timeout_sec set", PASS)
    else:
        report.add(section, "[environment] build_timeout_sec set", FAIL, "missing")
    net_mode = env.get("network_mode")
    if net_mode in ("public", "offline"):
        report.add(section, "[environment] network_mode valid", PASS, net_mode)
    else:
        report.add(section, "[environment] network_mode valid", WARN,
                    f"got {net_mode!r} — confirm against live spec's accepted values")
    report.add(
        section, "resource footprint (~2 CPU / 8GB RAM / 10GB storage, no GPU)",
        MANUAL, "not declared in task.toml directly — verify against Dockerfile/environment behavior",
    )


def check_instruction_md(task_dir: Path, report: Report):
    section = "instruction.md (REGULATIONS.md §3)"
    p = task_dir / "instruction.md"
    text = read_text(p)
    if text is None:
        report.add(section, "instruction.md readable", FAIL, "missing")
        return

    stripped = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    if not stripped:
        report.add(section, "instruction.md has content", FAIL,
                    "only template comments remain — write the real prompt")
        return

    bullet_lines = [l for l in stripped.splitlines() if re.match(r"^\s*[-*]\s+", l)]
    paragraphs = [p for p in re.split(r"\n\s*\n", stripped) if p.strip()]
    if bullet_lines:
        if len(bullet_lines) <= 20:
            report.add(section, "length: <=20 bullets", PASS, f"{len(bullet_lines)} bullets")
        else:
            report.add(section, "length: <=20 bullets", WARN, f"{len(bullet_lines)} bullets — trim or restructure")
    else:
        if len(paragraphs) <= 3:
            report.add(section, "length: ~2 short paragraphs", PASS, f"{len(paragraphs)} paragraph block(s)")
        else:
            report.add(section, "length: ~2 short paragraphs", WARN, f"{len(paragraphs)} paragraph blocks — consider tightening")

    has_abs_path = bool(re.search(r"[`\"']/[\w.\-/]+[`\"']|`/[\w.\-/]+`", stripped)) or bool(re.search(r"(?<![:\w])/[a-zA-Z0-9_\-./]+", stripped))
    if has_abs_path:
        report.add(section, "uses absolute filesystem paths", PASS)
    else:
        report.add(section, "uses absolute filesystem paths", WARN,
                    "no obvious absolute path (e.g. /app/output.json) found — confirm manually")

    for manual_item in [
        "human-written tone, no AI-generated writing patterns",
        "describes WHAT not HOW; no implementation walkthroughs or solution hints",
        "every requirement inferable from provided materials",
        "does not leak oracle logic",
        "would survive LLM-as-Judge review",
    ]:
        report.add(section, manual_item, MANUAL, "see checklists/03_instructions.md")


def check_dockerfile_common(path: Path, section: str, report: Report, *, is_environment: bool):
    text = read_text(path)
    if text is None:
        report.add(section, f"{path.name} present", FAIL, "missing")
        return

    from_lines = [l for l in text.splitlines() if l.strip().upper().startswith("FROM")]
    if not from_lines:
        report.add(section, "has a FROM line", FAIL)
    else:
        unpinned = [l for l in from_lines if "@sha256:" not in l]
        if unpinned:
            report.add(section, "every FROM is digest-pinned", FAIL,
                        "; ".join(l.strip() for l in unpinned))
        else:
            report.add(section, "every FROM is digest-pinned", PASS)
        placeholder = [l for l in from_lines if "REPLACE" in l.upper()]
        if placeholder:
            report.add(section, "no leftover REPLACE_ME placeholders", FAIL,
                        "template placeholder still present in FROM line")

    if re.search(r"apt-get\s+upgrade", text):
        report.add(section, "no `apt-get upgrade`", FAIL)
    else:
        report.add(section, "no `apt-get upgrade`", PASS)

    if is_environment:
        for forbidden in ["solution/", "tests/"]:
            if re.search(rf"COPY\s+{re.escape(forbidden)}", text):
                report.add(section, f"does not COPY {forbidden} into image", FAIL)
            else:
                report.add(section, f"does not COPY {forbidden} into image", PASS)

        has_tmux = "tmux" in text
        has_asciinema = "asciinema" in text
        if has_tmux and has_asciinema:
            report.add(section, "tmux + asciinema installed", PASS)
        else:
            missing = [n for n, present in (("tmux", has_tmux), ("asciinema", has_asciinema)) if not present]
            report.add(section, "tmux + asciinema installed", WARN, f"not found: {', '.join(missing)}")

    for manual_item in [
        "sanctioned/approved base image, or justification documented",
        "cache-friendly layer ordering (stable deps before task files)",
        "package versions pinned (beyond base image digest)",
        "multi-stage build used if compilation required",
        "no oversized bundled files",
    ]:
        report.add(section, manual_item, MANUAL, "see docker_environment_review/")


def check_environment(task_dir: Path, report: Report):
    section = "Environment / Dockerfile (REGULATIONS.md §6)"
    check_dockerfile_common(task_dir / "environment" / "Dockerfile", section, report, is_environment=True)

    dockerignore = task_dir / "environment" / ".dockerignore"
    text = read_text(dockerignore)
    if text is None:
        report.add(section, ".dockerignore present", WARN, "missing — add one; see docker_environment_review/file_handling_requirements.md")
    else:
        missing = [entry for entry in ("solution/", "tests/") if entry not in text]
        if missing:
            report.add(section, ".dockerignore excludes solution/ and tests/", WARN, f"missing: {', '.join(missing)}")
        else:
            report.add(section, ".dockerignore excludes solution/ and tests/", PASS)


def check_verifier(task_dir: Path, report: Report):
    section = "Verifier (REGULATIONS.md §8)"
    check_dockerfile_common(task_dir / "tests" / "Dockerfile", section, report, is_environment=False)

    test_py = read_text(task_dir / "tests" / "test_outputs.py")
    if test_py is None:
        report.add(section, "tests/test_outputs.py present", FAIL, "missing")
    else:
        if "NotImplementedError" in test_py and "def test_placeholder" in test_py:
            report.add(section, "tests/test_outputs.py has real assertions", FAIL,
                        "still the unmodified placeholder — write real tests")
        else:
            report.add(section, "tests/test_outputs.py has real assertions", PASS)

        for bad_pattern, label in [
            (r"\btime\.time\(\)", "no wall-clock dependence (time.time())"),
            (r"\brandom\.\w+\(", "no unseeded randomness (random module)"),
            (r"\brequests\.(get|post|put|delete)\(", "no live network calls (requests)"),
            (r"\burllib\.request\.", "no live network calls (urllib)"),
            (r"assert\s+\S+\s*==\s*(0x[0-9a-fA-F]+|['\"]0x[0-9a-fA-F]+['\"])",
             "no hardcoded raw hex address/offset asserted directly (pin via fixture/golden value instead)"),
            (r"\bos\.getpid\(\)", "no raw PID asserted directly (environment-dependent)"),
            (r"\bhex\(id\(", "no raw object-identity/address asserted directly (environment-dependent)"),
        ]:
            if re.search(bad_pattern, test_py):
                report.add(section, label, WARN, "pattern found — confirm it's not a real determinism/network risk")
            else:
                report.add(section, label, PASS)

    for manual_item in [
        "every requirement in instruction.md is tested",
        "edge cases covered",
        "validates semantics, not superficial formatting",
        "no oracle leakage; not trivially hardcodable/gameable",
        "a plausible-but-incorrect implementation would fail",
    ]:
        report.add(section, manual_item, MANUAL, "see checklists/08_verifier.md and reviewer_recovery/strong_task_principles.md (B, F)")


def check_solution(task_dir: Path, report: Report):
    section = "Oracle Solution (REGULATIONS.md §7)"
    p = task_dir / "solution" / "solve.sh"
    text = read_text(p)
    if text is None:
        report.add(section, "solution/solve.sh present", FAIL, "missing")
        return
    if "set -euo pipefail" in text or "set -e" in text:
        report.add(section, "fails fast on error (set -e...)", PASS)
    else:
        report.add(section, "fails fast on error (set -e...)", WARN, "no `set -e`-style guard found")
    for manual_item in [
        "deterministic and repeatable",
        "demonstrates the real workflow (not just printing the expected answer)",
        "does not shortcut the task",
        "reflects how a strong engineer would actually solve it",
    ]:
        report.add(section, manual_item, MANUAL, "see checklists/07_oracle_solution.md")


def check_rubric(task_dir: Path, report: Report):
    section = "Rubric (REGULATIONS.md §9)"
    # Rubric is deliberately NOT part of the submission ZIP; look for the
    # kit's own scratch file or a rubrics.txt left in the working folder.
    candidates = [task_dir / "rubrics.txt", task_dir / "rubric_INTERNAL_reference.md"]
    found = next((c for c in candidates if c.exists()), None)
    if found is None:
        report.add(section, "rubric draft found for validation", SKIP,
                    "no rubrics.txt or rubric_INTERNAL_reference.md in this folder — "
                    "validate manually if the rubric lives elsewhere (e.g. inline in a review tool)")
        return

    text = read_text(found) or ""
    lines = [l.strip() for l in text.splitlines()
             if l.strip().startswith("Agent") and re.search(r",\s*[+\-]\d+\s*$", l.strip())]
    if not lines:
        report.add(section, f"parseable rubric lines found in {found.name}", WARN,
                    "no lines matched the `Agent ..., ±N` pattern — check formatting or that this isn't just template scaffolding")
        return

    total = 0
    bad_magnitude = []
    has_negative = False
    for line in lines:
        m = re.search(r",\s*([+\-])(\d+)\s*$", line)
        sign, mag = m.group(1), int(m.group(2))
        signed = mag if sign == "+" else -mag
        total += signed
        if sign == "-":
            has_negative = True
        if mag not in VALID_REWARD_MAGNITUDES:
            bad_magnitude.append(line)

    report.add(section, "every line begins with 'Agent' and ends with ', ±N'", PASS, f"{len(lines)} lines parsed")
    if bad_magnitude:
        report.add(section, "only magnitudes 1/2/3/5 used (no ±4)", FAIL, "; ".join(bad_magnitude))
    else:
        report.add(section, "only magnitudes 1/2/3/5 used (no ±4)", PASS)
    report.add(section, "at least one negative reward line", PASS if has_negative else FAIL)
    if 10 <= total <= 40:
        report.add(section, "cumulative score between 10 and 40", PASS, f"total={total}")
    else:
        report.add(section, "cumulative score between 10 and 40", FAIL, f"total={total}")

    if found.name == "rubrics.txt":
        report.add(section, "rubrics.txt excluded from submission ZIP", WARN,
                    "reminder: strip this file at packaging time (checklists/11)")

    for manual_item in [
        "measures engineering behavior, not just automatic pass/fail",
        "rewards task-specific reasoning, avoids vague/subjective criteria",
    ]:
        report.add(section, manual_item, MANUAL, "see checklists/09_rubric.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("task_dir", type=Path, help="Path to the task folder (containing task.toml, instruction.md, etc.)")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on WARN as well as FAIL")
    args = parser.parse_args()

    task_dir = args.task_dir
    if not task_dir.is_dir():
        print(f"error: {task_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    report = Report()
    check_required_files(task_dir, report)
    scan_canaries(task_dir, report)
    check_task_toml(task_dir, report)
    check_instruction_md(task_dir, report)
    check_environment(task_dir, report)
    check_solution(task_dir, report)
    check_verifier(task_dir, report)
    check_rubric(task_dir, report)

    report.print_report()

    c = report.counts()
    if c[FAIL] > 0 or (args.strict and c[WARN] > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
