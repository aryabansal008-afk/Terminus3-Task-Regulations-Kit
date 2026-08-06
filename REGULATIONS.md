# Terminus 3 Task Regulations — Consolidated Checklist

Merged from Doc 1 ("Task Improvement Prompt") and Doc 2 ("Compliance &
Quality Review Prompt"). Where the two disagreed or one was more specific,
see NOTES_ON_CONFLICTS.md — this file states the canonical merged version.

## 1. Task Design & Novelty
- Goal is clear, specific, and unambiguous.
- Every requirement is inferable from the provided materials (no hidden
  expectations the agent can't discover).
- Grounded in a realistic software engineering / technical domain.
- Requires genuine debugging, implementation, investigation, or engineering
  — not shallow pattern matching.
- Requires multi-step reasoning, intermediate state, and adaptation during
  execution; cannot be solved by a single command or straight-line script.
- Difficulty comes from reasoning, not from prompt ambiguity.
- No unnecessary complexity.
- Genuinely novel — not a reskin or near-duplicate of Terminal-Bench 2.1,
  Terminal-Bench 3.0, or previous Terminus tasks. Evaluate **both** the
  underlying computation and the problem setup — two tasks can differ in
  surface framing while testing the identical computation, or vice versa;
  either alone can still fail novelty. (refined — Doc 4)
- Multi-step: requires genuine reasoning, intermediate state, branching,
  recovery, or reacting to previous results — not solvable by a single
  command or straight-line execution. (refined — Doc 4)
- Testable: fully specified, deterministic, self-contained, and objectively
  verifiable. (Doc 4)
- **Standalone** (new — Doc 4): completes without human interaction after
  launch; all inputs come from files, flags, or environment variables — no
  step requires a human to intervene mid-run.
- Exactly one category and one subcategory selected from the official
  taxonomy.
- No canary strings anywhere in the repository.
- **Language compliant** (new — Doc 4): primary language(s) correctly
  declared in `task.toml` `languages`; consider whether a multi-language
  design (e.g. a Python service driven by a shell/Go/Rust tool) would
  strengthen the task naturally rather than forcing it in artificially.
- **Mechanism-level novelty check** (refined — kit pass): for tasks in a
  narrow technical domain (e.g. a specific subsystem, protocol, or runtime
  behavior), compare against prior tasks at the level of the *specific
  mechanism exercised*, not just `category`/`subcategory`. Two tasks can
  share a taxonomy label while being mechanically unrelated (e.g. two
  "debugging" tasks touching entirely different subsystems), or look
  unrelated on the surface while exercising the same underlying mechanism.
  When authoring or reviewing, name the mechanism explicitly (in your own
  notes, not necessarily in `instruction.md`) so it can be diffed against
  past tasks rather than relying on the taxonomy label alone.

## 2. Difficulty
Difficulty is determined by **expected pass rate**, not opinion. Never
invent or assert specific pass rates as fact — only reason about which band
the task's characteristics suggest. If actual GPT-5.6 / Claude Opus 5
evaluation results are available, treat them as the source of truth over
qualitative reasoning (but still run failure analysis first — see
`difficulty_calibration/failure_analysis_workflow.md` — before using raw
pass rate to recalibrate).

| Tier | Expected pass rate | Qualitative description (Doc 5) |
|---|---|---|
| Frontier | <20% | Specification inference, interacting correctness axes, semantic artifacts, deep domain reasoning |
| Advanced | 20–50% | Clear goal but difficult execution, interacting constraints, stateful reasoning |
| Core | 50–80% | Well-specified multi-step task with meaningful edge cases |
| Base | 80–100% | Non-trivial but readily solvable by a competent frontier model |

Full detail, including the obscure-trivia-vs-deep-domain-reasoning
distinction: `difficulty_calibration/`.

## 3. Instructions (instruction.md)
- Human-written; avoids AI-generated writing patterns.
- Concise — roughly two short paragraphs or ≤20 bullets.
- No canary strings.
- No unnecessary verbosity.
- Contains all explicit requirements and all implicit expectations needed
  for successful completion.
- Does not leak oracle logic.
- Uses absolute filesystem paths (e.g. `/app/output.json`), not relative
  ones.
- Explicitly specifies required output files and formats.
- Would survive LLM-as-Judge review.
- Sounds like a real engineer's request, not AI-generated text. (Doc 4)
- Describes **what** must be achieved, not **how** to achieve it. (Doc 4)
- Contains no implementation walkthroughs, solution hints, API blueprints,
  excessive formatting, or highlighted solution details. (Doc 4 — this is
  stricter than "doesn't leak oracle logic": it also rules out incidental
  hints like a suspiciously-detailed API sketch or a bolded "key insight.")
- Logical instructions are **not** moved into environment documents (e.g.
  a Dockerfile comment, a README inside `environment/`) as a way to dodge
  instruction.md's length/conciseness limit. (new anti-gaming rule — Doc 4)
- Any supporting specification files the task references (schemas, RFCs,
  API contracts, business rules) read like genuine engineering
  documentation — not like a disguised hidden prompt or solution guide.
  (new — Doc 4)

## 4. Required Files & Packaging
Exact manifest (canonical, per Doc 2):
```
task.toml
instruction.md
environment/Dockerfile
solution/solve.sh
tests/Dockerfile
tests/test.sh
tests/test_outputs.py
```
- `rubrics.txt` excluded from the submission ZIP.
- `README.md` excluded from the submission ZIP.
- No extra enclosing directory in the ZIP — files sit at the archive root.
- No missing files, no extra nesting.

## 5. task.toml
Required fields:
- `name`
- `category`
- `subcategory`
- `tags` (3–6)
- `languages`
- `difficulty`
- `expert_time_estimate_hours`
- `author_name`
- `author_email`
- `artifacts`
- `difficulty_explanation`
- `solution_explanation`
- `verification_explanation`
- `relevant_experience`

`[agent]` block:
- `timeout_sec` — see NOTES_ON_CONFLICTS.md re: minimum value
- appropriate for the task's expected runtime

`[verifier]` block:
- `timeout_sec` set
- `environment_mode = "separate"`

`[environment]` block:
- `build_timeout_sec` set
- `network_mode = "public"` unless the task specifically requires offline
  execution
- compatible with ~2 CPU cores, 8 GB RAM, 10 GB storage
- no GPU dependency

## 6. Environment (Docker)
Full detail (file handling, verifier-Dockerfile specifics, review response
template): `docker_environment_review/`.

- Every `FROM` image is digest-pinned.
- **Sanctioned**: final runtime image uses an approved Terminal-Bench base
  image, or the Dockerfile includes a clear justification for a
  non-canonical base. (Doc 1 + Doc 6 — this was in Doc 1 originally but was
  missed in the first pass of this checklist; restored now.)
- Package versions pinned.
- Dockerfile builds successfully.
- `solution/` is never copied into the environment image.
- `tests/` is never copied into the environment image.
- Secrets/credentials, expected outputs/golden values, and any
  verifier-only assets are never copied into the agent image either. (Doc 6
  — broader than just the solution/tests folders.)
- Verifier image contains all required test dependencies.
- Environment is reproducible; no nondeterministic build steps.
- Parent directories for every artifact exist.
- tmux and asciinema installed.
- Cache-friendly layer ordering: stable dependencies before frequently
  changing task files. (Doc 6)
- `apt` operations consolidated; never `apt-get upgrade`; caches cleaned in
  the same layer as the install. (Doc 6)
- Multi-stage builds used when compilation is required, so build tooling
  doesn't ship in the final image. (Doc 6)
- Complete: no runtime package installation by agent or verifier. (Doc 6)
- No oversized bundled files; environment stays under size limits.
- Appropriate `.dockerignore` — see `docker_environment_review/file_handling_requirements.md`
  for the full list of what it should exclude.
- Resource-aware against this task's actual declared `task.toml` limits,
  not just the general target. (Doc 6)

## 7. Oracle Solution (solution/solve.sh)
- Deterministic.
- Human-written.
- Demonstrates the intended workflow — not merely printing the expected
  answer.
- Does not shortcut the task.
- Repeatable; guaranteed to satisfy the verifier every run.
- Reflects how a strong engineer would actually solve the task.
- **Environment-dependent values are pinned, not incidental** (refined —
  kit pass): if the workflow naturally produces values that are stable
  within a single container/build but not guaranteed stable across
  environments — memory addresses, pointer values, PIDs, file descriptors,
  loader-assigned IDs, compiled-in timestamps, hash-seed-dependent
  iteration order — the oracle (and any fixtures it relies on) should pin
  or derive these through a controlled/deterministic mechanism (fixed
  seeds, disabled ASLR, a simulated/offline harness, recorded golden data)
  rather than assuming today's raw runtime value will still be produced by
  a correct solution tomorrow. This is distinct from the classic
  time/randomness/network triad in §8 below — that covers *behavioral*
  nondeterminism, this covers *environmental* nondeterminism that can look
  stable in one build but silently vary in another.

## 8. Verifier (tests/)
- `environment_mode = "separate"` (isolated from agent's environment).
- Never relies on hidden oracle artifacts.
- Tests are deterministic: no wall-clock dependence, no network
  dependence, no unseeded randomness.
- **Tests do not assert raw environment-dependent values** (refined — kit
  pass): if a correct solution's output legitimately contains addresses,
  offsets, PIDs, loader-assigned IDs, or similar values that can vary
  across otherwise-correct environments/builds, the verifier checks the
  *relationship or invariant* that must hold (e.g. "this ID differs from
  the value recorded before reload," "no live ID is reused") or compares
  against a golden value produced by the same pinned/simulated mechanism
  the oracle uses — never a hardcoded raw value assumed to be portable.
  See §7's matching note.
- Validates semantics, not superficial formatting.
- Every requirement stated in `instruction.md` is tested.
- Edge cases covered.
- Tests cannot be trivially hardcoded / gamed.
- A plausible-but-incorrect implementation fails the verifier.
- No oracle leakage into the verifier.
- pytest-driven (`tests/test_outputs.py`).

## 9. Rubric
(New in Doc 2 — not mentioned in Doc 1. Doc 4 adds behavioral-quality
requirements on top of the syntax rules below.)
- Measures engineering behavior rather than automatic test execution — a
  line like "Agent passed all tests, +5" is weak; prefer lines that credit
  specific reasoning/engineering decisions the agent had to make. (Doc 4)
- Rewards task-specific reasoning and penalizes meaningful mistakes — not
  generic effort. (Doc 4)
- Avoids vague or subjective criteria (e.g. "Agent wrote clean code, +2" is
  too subjective unless "clean" is defined objectively elsewhere). (Doc 4)
- Cumulative score between 10 and 40.
- At least one negative reward line.
- Every line begins with `"Agent"`.
- Every line ends with `", ±N"`.
- Positive values explicitly include a `+` sign.
- Only ±1, ±2, ±3, ±5 are used — **no ±4**.
- Checkbox remains unchecked before submission.
- `rubrics.txt` itself is excluded from the final submission ZIP (see
  NOTES_ON_CONFLICTS.md item 4 for the apparent tension this creates).

## 10. Automated Checks / Local Validation
Expected to pass:
```
stb harbor run -a oracle -p <task-folder>
stb harbor check
```
Difficulty check (do not treat output as ground truth pass rate — use to
sanity-check the claimed tier):
```
stb harbor run -m @openai/gpt-5.6 -p <task-folder> -k 5
stb harbor run -m @anthropic/claude-opus-5 -p <task-folder> -k 5
```
Also confirm (per Doc 1): environment starts successfully, oracle passes,
verifier passes, LLM-as-Judge checks pass, final packaging is clean.

## 11. Self-Check
- Would a first-time reader understand exactly what must be done?
- Can the agent obtain everything it needs from the provided environment
  alone?
- Could an incorrect implementation accidentally pass?
- Are tests validating semantics rather than appearance?
- Is execution deterministic end-to-end?

## 12. Submission
- Contains only the required files (see section 4 manifest).
- Excludes `README.md`.
- Excludes `rubrics.txt`.
- No extra enclosing directory.
- Suitable for upload to the Terminus-3-Prod project.

## 13. Strong Task Principles (new — Doc 3)
Doc 3 ("Task Recovery & Reviewer Response Prompt") adds six deeper,
qualitative principles beyond the mechanical checklist above. A task can
pass sections 1–12 and still be weak against these — they're often what a
terse reviewer comment is actually pointing at. Full detail and a rating
rubric: `reviewer_recovery/strong_task_principles.md`.

- **A. Specification must be inferred** — from environment evidence, not
  handed to the agent as a checklist.
- **B. Output semantics matter** — the artifact must be actually correct,
  not merely shaped like a correct answer.
- **C. Correctness is multidimensional** — functionality, determinism,
  performance, safety, provenance, structural correctness, state
  consistency, hidden evaluation.
- **D. Constraints interact** — not independent checklist items.
- **E. State is part of the problem** — not purely "edit files, run tests."
- **F. Hidden semantic verification** — metamorphic tests, hidden cases,
  structural/semantic validation, anti-hardcoding protections.

## 14. Common Rejection Reasons (new — Doc 3)
Scan list for proactive review or post-rejection triage, cross-referenced
to sections above. Full list with cross-references:
`reviewer_recovery/common_rejection_reasons.md`.

Too easy · ambiguous requirements · similar to existing tasks · reskinned
benchmark · hidden knowledge unavailable to the agent · non-deterministic
behavior · shortcut solutions · oracle leakage · tests that validate
formatting rather than meaning · single-command solution · straight-line
execution · weak verifier · poor novelty.

**Important:** if a task is rejected as "too easy," do not fix it by hiding
requirements, introducing ambiguity, or adding unnecessary steps. Difficulty
must come from reasoning, inference, interacting constraints (§13.D), system
state (§13.E), and semantic verification depth (§13.F).

## 15. Reviewer Recovery Workflow (new — Doc 3)
When a task is rejected or returned with feedback, treat the reviewer
feedback as the highest-priority source of truth and prefer targeted edits
over redesign. Use `reviewer_recovery/reviewer_response_template.md` to
produce the required response format:

Overall Verdict → Root Cause Analysis → Reviewer Feedback Mapping table →
Strong Terminus 3 Evaluation (§13 ratings) → Recovery Plan (priority order)
→ Risk Assessment (Low/Medium/High) → Clarifications Needed.

Never fabricate reviewer intent, never invent pass rates, and always ask
targeted questions when feedback is ambiguous rather than guessing.
