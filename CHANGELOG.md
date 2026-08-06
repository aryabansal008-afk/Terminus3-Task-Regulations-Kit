# Changelog

Tracks which source prompt/spec introduced or changed each part of this
kit, so future updates (new prompts, new live-spec versions) can be folded
in the same way instead of guessed at. See "Extending this kit" in
`README.md` for the process this log supports.

Each entry: **source** (the prompt/doc that drove the change) → **what
changed** → **where**.

## Doc 1 — Task Improvement Prompt
Initial checklist baseline: task design/novelty, difficulty (qualitative
tiers only), instructions, required folders (generic), environment
(including the original "sanctioned base image" requirement), oracle
solution, automated validation (generic CI/eval mentions).
→ `REGULATIONS.md` §1–§2, §6–§7, §10 (baseline).

## Doc 2 — Compliance & Quality Review Prompt
Treated as canonical over Doc 1 wherever more specific: explicit
pass-rate bands per difficulty tier, exact required-file manifest, full
`task.toml` field list, rubric syntax rules (new), exact `stb harbor ...`
validation commands.
→ `REGULATIONS.md` §2–§5, §9–§10; `NOTES_ON_CONFLICTS.md` items 1–6.

**Known open item from Doc 1 vs Doc 2**: verifier vs agent `timeout_sec`
minimum ownership was never fully resolved — see `NOTES_ON_CONFLICTS.md`
item 1. Confirm against the live spec before relying on either value.

## Doc 3 — Task Recovery & Reviewer Response Prompt
New layer, not a revision of Docs 1–2: post-rejection recovery workflow.
Added Strong Task Principles A–F, common rejection reasons cross-referenced
to `REGULATIONS.md`, and the reviewer response report format.
→ `reviewer_recovery/` (new folder); `REGULATIONS.md` §13–§15.

## Doc 4 — (referenced inline in REGULATIONS.md §1/§3/§9, no dedicated folder)
Refined Task Design & Novelty (computation vs problem-setup novelty must
both be checked; added Standalone and Language-compliance requirements),
tightened Instructions (WHAT-not-HOW, no offloading length limits into
environment docs, spec files must read as genuine docs), and added
behavioral-quality requirements on top of Doc 2's rubric syntax rules.
Also supplied the agent-timeout-minimum data point used in
`NOTES_ON_CONFLICTS.md` item 1.
→ `REGULATIONS.md` §1, §3, §9; `checklists/13_standalone_internet_language.md`
  (new checklist file, since Doc 4's Standalone/Language items didn't fit
  cleanly into the existing Task Design checklist).

## Doc 5 — Difficulty Evaluation & Calibration Prompt
New layer: qualitative tier definitions (complementing Doc 2's numeric
bands), legitimate-vs-artificial-difficulty reference (including the
obscure-trivia-vs-deep-domain-reasoning distinction), failure-analysis
workflow for recalibrating off real eval logs, response template.
→ `difficulty_calibration/` (new folder); referenced from
  `REGULATIONS.md` §2.

## Doc 6 — Docker Engineer & Infrastructure Reviewer Prompt
New layer: detailed Dockerfile requirements (cache-friendly layering,
build efficiency, isolation, minimalism, OCI labels), file-handling
requirements (.dockerignore contents, COPY strategy, no heredoc-embedded
source), verifier-Dockerfile-specific requirements, review response
template. Also restored the "sanctioned base image" requirement, which was
present in Doc 1 but dropped from `REGULATIONS.md` §6 on the first
consolidation pass.
→ `docker_environment_review/` (new folder); `REGULATIONS.md` §6 (restored
  item + full detail delegated to this folder).

## Kit infrastructure pass (this update)
Not driven by a new source prompt — a review of the kit's own completeness
against its stated goal ("maximize the likelihood of passing all future
tasks," reusable/task-agnostic infrastructure rather than a one-off).
Everything in `REGULATIONS.md`/`checklists/` was already comprehensive and
consistent with the six source docs; the gap was that every check was
manual-only, with no way to catch mechanical mistakes before a human or
LLM-as-Judge review pass.
- Added `tools/validate_task.py`: dependency-free validator that
  mechanically checks a task folder against every objectively-checkable
  rule already in `REGULATIONS.md` (required files, `task.toml` fields and
  values, digest pinning, forbidden `COPY`s, canary strings, rubric
  syntax/score bounds, obvious verifier determinism red flags, leftover
  template placeholders) and explicitly flags the rest as `MANUAL` with a
  pointer to the matching `checklists/` file, so no requirement is silently
  unchecked.
- Added `tools/README.md` documenting its scope, exit codes, and how to
  extend it when a new rule is added.
- Added this `CHANGELOG.md` and a "Kit structure at a glance" /
  "Extending this kit" section in `README.md`, so the next new source
  prompt gets folded in following the same pattern Docs 3/5/6 already
  established, instead of each contributor re-deriving the convention.
- No changes to the substance of any existing rule, checklist, or
  template — this pass only adds tooling and process documentation.

## Foundation pass — native/systems-domain task review (this update)
Triggered by reviewing a proposed task (`elf-tls-dtp-modid`: an ELF
dynamic-loader TLS/DTV lifecycle bug spanning a Rust loader and a Go
host). Not a task-specific addition — the task surfaced two gaps in the
kit's existing guidance that apply to any task in a narrow technical
domain, not just this one:

- **Novelty comparison can miss mechanically-unrelated tasks that share a
  taxonomy label**, or mechanically-identical tasks with different
  surface framing, if compared only by `category`/`subcategory`. Added a
  "mechanism-level novelty check" bullet to `REGULATIONS.md` §1 and
  `checklists/01_task_design_and_novelty.md` generalizing this — applies
  to any narrow technical-domain task (a specific subsystem, protocol, or
  runtime behavior), not just native/systems tasks.
- **Determinism guidance (§7 oracle, §8 verifier) covered
  time/randomness/network but not "environmental" nondeterminism** —
  values like addresses, PIDs, loader-assigned IDs, or compiled-in
  timestamps that are stable within one build but not guaranteed stable
  across environments. Added matching bullets to `REGULATIONS.md` §7/§8,
  `checklists/07_oracle_solution.md`, `checklists/08_verifier.md`, and
  three heuristic (non-blocking `WARN`) scans to
  `tools/validate_task.py`'s verifier check (raw hex value assertions,
  `os.getpid()`, `hex(id(...))`) as a first-pass signal — real coverage of
  this still requires the manual review the checklist points to.

No task-specific content (ELF, TLS, DTV, Rust/Go specifics) was added
anywhere in the kit — the two gaps above are stated generically so they
apply to any future task that happens to touch loader/runtime internals,
concurrency, hardware interaction, or any other domain where "stable in
this build" and "portable across environments" can silently diverge.

## Delegated-authoring pass (this update)
Added `templates/cursor_authoring_prompt.md`: a generic prompt template
for handing full task-package authoring to an external coding agent
(Cursor, Claude Code, etc.) from a short concept brief. Not tied to any
specific task — takes `[TASK_SLUG]`/`[CATEGORY]`/`[SUBCATEGORY]`/
`[LANGUAGES]`/`[CONCEPT]` placeholders and encodes the kit's priority
order (REGULATIONS.md compliance → oracle/verifier determinism →
instruction discipline → mechanism-level novelty → legitimate difficulty →
Docker requirements → rubric syntax), plus an explicit instruction to ask
rather than guess on ambiguity and to close the loop with
`tools/validate_task.py` and the `checklists/` self-ratings before
declaring the package done.
