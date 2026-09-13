# Terminus 3 Task Regulations Kit

This kit does **not** contain a finished task - no actual task materials
(instruction.md content, oracle logic, verifier tests) were provided, so
nothing here fabricates task-specific content. It gives you:

1. **REGULATIONS.md** - the full merged checklist from both source prompts,
   organized by review section, with canonical values where the two prompts
   agree.
2. **NOTES_ON_CONFLICTS.md** - the specific places where the two prompts
   disagree or one is more specific than the other, so nothing was merged
   silently.
3. **checklists/** - one file per review section, each usable standalone as
   a pass/fail worksheet (✅ / ⚠ / ❌) when you actually review a task.
4. **templates/** - a scaffold matching Doc 2's exact required file manifest,
   with inline comments explaining what Terminus 3 expects in each file.
   These are placeholders, not real content - fill in per task specifics.
5. **reviewer_recovery/** - This is a *different mode* from the other
   two: docs 1–2 are for authoring/reviewing a task before submission;
   this folder is for responding to reviewer feedback after a rejection.
   Contains the "Strong Task Principles" (A–F) deep evaluation rubric, a
   common rejection reasons scan list cross referenced to REGULATIONS.md,
   and a fill in response template matching the required recovery report
   format.
6. **difficulty_calibration/** - Qualitative tier definitions
   (complementing the pass-rate bands in REGULATIONS.md), a legitimate
   vs artificial difficulty reference (including the obscure trivia vs
   deep domain reasoning distinction), a failure analysis workflow for
   when real eval logs exist, and a fill in response template.
7. **docker_environment_review/** - added from a sixth prompt ("Docker
   Engineer & Infrastructure Reviewer Prompt"). Detailed Dockerfile
   requirements (cache friendly layering, build efficiency, isolation,
   minimalism), file handling requirements (.dockerignore, COPY strategy,
   no heredoc-embedded source), verifier Dockerfile specific requirements,
   and a fill in review response template.

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
6. Package per `checklists/11_submission_packaging.md` - no enclosing
   directory, no `README.md`, no `rubrics.txt`.
7. If a task comes back from review rejected or flagged, switch to
   `reviewer_recovery/` - use `reviewer_response_template.md` to structure
   your response, `strong_task_principles.md` to diagnose root causes the
   reviewer may not have stated explicitly, and
   `common_rejection_reasons.md` to scan for issues proactively.

   >Feel free to ⭐ this repository

