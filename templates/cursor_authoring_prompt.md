# Coding-Agent Task-Authoring Prompt (Template)

Use this when delegating full authoring of a Terminus 3 task package to an
external coding agent (Cursor, Claude Code, Copilot Workspace, etc.) from a
short concept brief. It is deliberately generic — fill in the bracketed
placeholders per task, don't hand-tune the surrounding instructions.

This template assumes the agent has (or you attach) read access to this
kit — `REGULATIONS.md`, `checklists/`, `templates/`, `reviewer_recovery/`,
`difficulty_calibration/`, `docker_environment_review/`, and
`tools/validate_task.py`. If the agent's tool can't browse a repo, paste
`REGULATIONS.md` and `templates/` into its context instead.

---

## Prompt to paste

```
You are authoring a complete Terminus 3 task package. Follow the
Terminus 3 Regulations Kit in this repo as the spec — do not invent
requirements that aren't in it, and do not skip requirements because they
seem inconvenient.

Task brief:
- Slug: [TASK_SLUG]
- Category: [CATEGORY]   Subcategory: [SUBCATEGORY, or "propose one from
  the official taxonomy and flag it for confirmation if you're not sure
  it's canonical"]
- Languages: [LANGUAGES]
- Concept: [CONCEPT — paste the full brief: what's broken, why it's hard,
  why it's novel vs. adjacent tasks, any low-risk implementation notes the
  brief already suggests]

Deliverables — produce exactly this file manifest, nothing more:
    task.toml
    instruction.md
    environment/Dockerfile
    solution/solve.sh
    tests/Dockerfile
    tests/test.sh
    tests/test_outputs.py
(A working `rubrics.txt` or rubric draft and a scratch README are fine to
keep alongside for your own iteration, but must NOT end up in the final
submission — see REGULATIONS.md §4/§12.)

Ground rules, in priority order when anything trades off:
1. Follow REGULATIONS.md section by section (§1 Task Design & Novelty
   through §12 Submission). Use templates/ as your starting scaffold, not
   as filler — every placeholder must become real, task-specific content
   or be deleted.
2. Oracle (solution/solve.sh) demonstrates the actual workflow — commands,
   builds, real interaction with the environment — never hardcodes or
   detects-and-prints the expected answer. Deterministic and repeatable.
   If the workflow would naturally touch values that are stable in one
   build but not guaranteed stable across environments (addresses, PIDs,
   loader-assigned IDs, timestamps, iteration order, etc.), pin them via a
   controlled/deterministic mechanism (fixed seeds, disabled ASLR,
   recorded golden data, a simulated/offline harness) rather than
   assuming today's raw value is portable — see REGULATIONS.md §7.
3. Verifier (tests/) runs in a separate container, is fully deterministic
   (no wall-clock, no network, no unseeded randomness, no raw
   environment-dependent values asserted directly — check invariants or
   golden values instead, see REGULATIONS.md §8), tests every requirement
   in instruction.md plus real edge cases, and would fail a
   plausible-but-incorrect implementation. No oracle leakage.
4. instruction.md describes WHAT must be achieved, not HOW — no
   implementation walkthroughs, no solution hints, no oracle logic. The
   agent solving the task later should have to infer the specific
   decomposition from the environment, not receive it as a checklist
   (Strong Task Principle A, reviewer_recovery/strong_task_principles.md).
   Roughly two short paragraphs or <=20 bullets. Absolute filesystem
   paths. No canary strings anywhere.
5. Novelty: compare against Terminal-Bench 2.1/3.0 and prior Terminus
   tasks at the level of the specific mechanism exercised, not just the
   category/subcategory label (REGULATIONS.md §1) — state in your own
   working notes what makes this mechanically distinct, using the brief's
   "why unique" reasoning as a starting point, not a copy-paste destination
   for instruction.md.
6. Difficulty should come from reasoning, interacting constraints, state,
   and semantic verification depth — never from ambiguity, hidden
   information, or padding (REGULATIONS.md §14,
   difficulty_calibration/legitimate_vs_artificial_difficulty.md). Declare
   the tier in task.toml with a real difficulty_explanation tied to the
   pass-rate band, not just a label.
7. Dockerfiles: digest-pinned FROM, sanctioned/justified base image,
   pinned package versions, solution/tests never copied into the agent
   image, tmux+asciinema installed in the agent image, cache-friendly
   layering, multi-stage build if compilation is required (see
   docker_environment_review/).
8. Rubric: cumulative 10-40, at least one negative line, every line
   `Agent ..., ±N` with only magnitudes 1/2/3/5, rewards task-specific
   engineering behavior rather than "passed tests, +N" (REGULATIONS.md
   §9) — draft it, but do not include rubrics.txt in the final manifest.

When something is genuinely ambiguous or not inferable from this brief or
the kit (e.g. the exact taxonomy subcategory, a resource limit, which of
two conflicting timeout values applies — see NOTES_ON_CONFLICTS.md) — ask
me directly instead of guessing or inventing a plausible-sounding value.

Before declaring this done:
- Run `python3 tools/validate_task.py <task-folder>` and fix every FAIL;
  address every WARN or explain why it's a false positive.
- Every item the validator marks MANUAL still needs an explicit answer —
  walk through the matching file in checklists/ by hand and report your
  self-rating (✅/⚠/❌) for each, per checklists/12_self_check.md.
- Confirm the final manifest matches REGULATIONS.md §4 exactly, with
  README.md/rubrics.txt excluded and no extra enclosing directory, before
  packaging (checklists/11_submission_packaging.md).

Report back with: the file tree you produced, your self-ratings against
checklists/01, 02, 07, 08, 09, and 13, the validate_task.py summary line,
and an explicit list of anything you're unsure about.
```

## Notes on using this template

- Keep the brief (`[CONCEPT]` block) exactly as given to you — don't
  paraphrase or compress it before pasting it in; loss of detail there is
  the single most common source of a mismatched task.
- If the agent doesn't have repo access to this kit, attach at minimum
  `REGULATIONS.md`, `templates/`, and `tools/validate_task.py` to its
  context before sending the prompt.
- This template intentionally does not soften rule 6 to increase perceived
  difficulty via ambiguity — if the resulting task comes back rated as
  "too easy," fix it per common_rejection_reasons.md's "Preserve
  Difficulty" framing, not by removing information from instruction.md.
