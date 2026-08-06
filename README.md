# Terminus 3 Task Regulations Kit

A consolidated reference + starter scaffold for authoring a Terminus 3 task
that satisfies the requirements described in the two review prompts you
provided ("Task Improvement Prompt" and "Compliance & Quality Review Prompt").

This kit does **not** contain a finished task — no actual task materials
(instruction.md content, oracle logic, verifier tests) were provided, so
nothing here fabricates task-specific content. It gives you:

1. **REGULATIONS.md** — the full merged checklist from both source prompts,
   organized by review section, with canonical values where the two prompts
   agree.
2. **NOTES_ON_CONFLICTS.md** — the specific places where the two prompts
   disagree or one is more specific than the other, so nothing was merged
   silently.
3. **checklists/** — one file per review section, each usable standalone as
   a pass/fail worksheet (✅ / ⚠ / ❌) when you actually review a task.
4. **templates/** — a scaffold matching Doc 2's exact required file manifest,
   with inline comments explaining what Terminus 3 expects in each file.
   These are placeholders, not real content — fill in per-task specifics.
5. **reviewer_recovery/** — added from a third prompt ("Task Recovery &
   Reviewer Response Prompt"). This is a *different mode* from the other
   two: docs 1–2 are for authoring/reviewing a task before submission;
   this folder is for responding to reviewer feedback after a rejection.
   Contains the "Strong Task Principles" (A–F) deep-evaluation rubric, a
   common-rejection-reasons scan list cross-referenced to REGULATIONS.md,
   and a fill-in response template matching the required recovery report
   format.
6. **difficulty_calibration/** — added from a fifth prompt ("Difficulty
   Evaluation & Calibration Prompt"). Qualitative tier definitions
   (complementing the pass-rate bands in REGULATIONS.md §2), a legitimate-
   vs-artificial-difficulty reference (including the obscure-trivia-vs-
   deep-domain-reasoning distinction), a failure-analysis workflow for
   when real eval logs exist, and a fill-in response template.
7. **docker_environment_review/** — added from a sixth prompt ("Docker
   Engineer & Infrastructure Reviewer Prompt"). Detailed Dockerfile
   requirements (cache-friendly layering, build efficiency, isolation,
   minimalism), file-handling requirements (.dockerignore, COPY strategy,
   no heredoc-embedded source), verifier-Dockerfile-specific requirements,
   and a fill-in review response template. Also restores a "sanctioned
   base image" requirement that was in Doc 1 but got dropped from
   REGULATIONS.md §6 on the first pass — fixed now.

## How to use this

1. Copy `templates/` into a new folder, rename it to your task's slug.
2. Fill in `task.toml`, `instruction.md`, `environment/Dockerfile`,
   `solution/solve.sh`, `tests/*` with your actual task content — or, if
   delegating authoring to an external coding agent (Cursor, Claude Code,
   etc.), use `templates/cursor_authoring_prompt.md` as the prompt
   template.
3. Run `tools/validate_task.py <your-task-folder>` early and often — it
   mechanically checks everything in `checklists/` that can be checked
   without judgment (required files, task.toml fields, digest pinning,
   canary strings, rubric syntax, etc.) and tells you exactly which
   remaining items need a human/LLM-as-Judge pass. See
   `tools/README.md`.
4. Work through `checklists/` in order before packaging — including the
   items the validator can't check for you (novelty, instruction tone,
   verifier depth, oracle quality).
5. Resolve the items in `NOTES_ON_CONFLICTS.md` against the current live
   Terminus 3 spec (this kit can't know which version is authoritative).
6. Package per `checklists/11_submission_packaging.md` — no enclosing
   directory, no `README.md`, no `rubrics.txt`.
7. If a task comes back from review rejected or flagged, switch to
   `reviewer_recovery/` — use `reviewer_response_template.md` to structure
   your response, `strong_task_principles.md` to diagnose root causes the
   reviewer may not have stated explicitly, and
   `common_rejection_reasons.md` to scan for issues proactively.

## Required file manifest (per Doc 2, canonical)

```
task.toml
instruction.md
environment/Dockerfile
solution/solve.sh
tests/Dockerfile
tests/test.sh
tests/test_outputs.py
```

## Kit structure at a glance

```
REGULATIONS.md                 canonical merged checklist (start here)
NOTES_ON_CONFLICTS.md          where source docs disagree / need confirmation
CHANGELOG.md                   what changed each time a new source doc was folded in
checklists/                    one pass/fail worksheet per REGULATIONS.md section
templates/                     scaffold matching the required file manifest
tools/validate_task.py         automated first-pass check against templates/checklists
reviewer_recovery/             post-rejection response workflow (Doc 3)
difficulty_calibration/        difficulty tier calibration workflow (Doc 5)
docker_environment_review/     Dockerfile-specific deep dive (Doc 6)
```

## Extending this kit

This kit is meant to absorb new source prompts/specs over time without
duplicating what's already here:

- A new prompt that **refines an existing section** → update that section
  in `REGULATIONS.md` and the matching `checklists/NN_*.md` file in place;
  note the change and its source in `CHANGELOG.md`. Don't fork a parallel
  copy of a section that already exists.
- A new prompt that **adds a genuinely new review layer** (like Docs 3, 5,
  6 did) → give it its own top-level folder plus a matching `checklists/`
  entry, cross-referenced from `REGULATIONS.md`, exactly as the existing
  folders do.
- A new prompt that **conflicts** with an existing rule → do not silently
  overwrite; add an entry to `NOTES_ON_CONFLICTS.md` recording both
  versions and which one the kit currently treats as canonical, plus why.
- Any new objectively-checkable rule (a required field, a syntax
  constraint, a forbidden pattern) → add a corresponding check to
  `tools/validate_task.py` rather than leaving it as a manual-only
  checklist item, so future tasks benefit automatically.
