# Notes on Conflicts Between Source Documents

This kit was built from two provided prompts:

- **Doc 1**: "Terminus 3 Task Improvement Prompt"
- **Doc 2**: "Terminus 3 Compliance & Quality Review Prompt"

Doc 2 is more detailed and is treated as the **canonical/latest** source wherever
the two overlap without conflict. Where they actually disagree, both versions
are recorded below instead of silently picking one — confirm with your team
which is correct before relying on this kit for a real submission.

## 1. Timeout ownership (UNRESOLVED — needs your confirmation)

| Field | Doc 1 says | Doc 2 says |
|---|---|---|
| Verifier `timeout_sec` | ≥ 1800 sec | just "set" (no minimum stated) |
| Agent `timeout_sec` | "appropriate", typically 7200 sec | ≥ 1800 sec, "appropriate for expected runtime" |

The kit's `task.toml` template comments both possibilities. **Do not assume
either is correct without checking the current Terminus 3 spec directly.**

**Update from Doc 4**: Doc 4 states "runtime appropriate: complexity matches
the configured agent timeout (minimum 1800s, typically 60–90 minutes)" —
this puts the 1800s minimum on the **agent** timeout, agreeing with Doc 2
rather than Doc 1. That's now 2-of-3 sources (Doc 2, Doc 4) favoring agent
timeout for the minimum. However, Doc 4's *typical* value (60–90 min =
3600–5400s) does not match Doc 1's stated typical of 7200s (120 min) either
— so the "typical" figure is still unresolved even though the "minimum"
figure now leans toward agent timeout ≥1800s. Treat the minimum as
reasonably well-supported; still confirm the typical value against the live
spec.

## 2. Difficulty tier pass-rate bands (Doc 2 used as canonical — more specific)

Doc 1 names four tiers (Frontier, Advanced, Core, Base) with no numeric bands.
Doc 2 gives explicit expected pass-rate ranges:

- Frontier: <20%
- Advanced: 20–50%
- Core: 50–80%
- Base: 80–100%

Kit uses Doc 2's numbers. Doc 1 is not in conflict here, just less specific.

## 3. Required file manifest (Doc 2 used as canonical — more specific)

Doc 1 refers generically to `environment/`, `solution/`, `tests/` as folders.
Doc 2 gives an exact manifest:

```
task.toml
instruction.md
environment/Dockerfile
solution/solve.sh
tests/Dockerfile
tests/test.sh
tests/test_outputs.py
```

Kit scaffold follows Doc 2's exact manifest.

## 4. Rubric requirements — new in Doc 2 only

Doc 1 does not mention a rubric at all. Doc 2 introduces detailed rubric
syntax rules (cumulative score 10–40, at least one negative reward, line
format `Agent ... , ±N`, only ±1/±2/±3/±5, no ±4, checkbox unchecked before
submission) and simultaneously states `rubrics.txt` must be **excluded**
from the final submission ZIP. This implies the rubric is authored
internally (e.g. inline in `task.toml` or a working file kept outside the
package) — the kit includes an `rubric_INTERNAL_reference.md` that is
explicitly labeled "do not include in submission ZIP."

## 5. task.toml field list — Doc 2 adds several fields not in Doc 1

Doc 2 adds: `author_name`, `author_email`, `artifacts`,
`difficulty_explanation`, `solution_explanation`, `verification_explanation`,
`relevant_experience`, and a `tags` count constraint (3–6). Doc 1 mentioned
`explanations`, `artifacts`, `tags`, `languages` generically. Kit uses Doc 2's
explicit list.

## 6a. Doc 3 relationship to Docs 1–2 (not a conflict, but noted)

Doc 3 ("Task Recovery & Reviewer Response Prompt") does not restate or
contradict any of the specific values from Docs 1–2 (timeouts, file
manifest, rubric syntax, tmux/asciinema, etc.) — it operates at a different
layer entirely: what to do *after* a reviewer has already responded to a
submission, rather than how to author/self-review one beforehand. It has
been added to the kit as a separate `reviewer_recovery/` section rather than
merged into REGULATIONS.md's core checklist, since mixing "author this" and
"recover this after rejection" guidance in one checklist would blur which
mode you're in. No values needed reconciling here.

## 6. Automated validation commands — new in Doc 2 only

Doc 2 specifies exact CLI checks:
```
stb harbor run -a oracle -p <task-folder>
stb harbor check
stb harbor run -m @openai/gpt-5.6 -p <task-folder> -k 5
stb harbor run -m @anthropic/claude-opus-5 -p <task-folder> -k 5
```
Doc 1 only refers to these generically as "Automated CI / GPT-5.6 evaluation /
Claude Opus 5 evaluation." Kit uses Doc 2's exact commands in the local
validation checklist.
