# Strong Terminus 3 Task Principles (A–F)

Source: Doc 3 ("Task Recovery & Reviewer Response Prompt"). These are
deeper, qualitative criteria — use them alongside REGULATIONS.md section 1
(Task Design), not instead of it. A task can pass every mechanical checklist
item and still be weak against these principles; that's usually what a
reviewer is actually reacting to even when their comment reads as cosmetic.

For each principle, mark ✅ Strong / ⚠ Needs Improvement / ❌ Missing and
write a one-line justification when actually reviewing a task.

## A. Specification must be inferred
Can the agent reconstruct the problem from evidence in the environment
rather than follow an explicit checklist handed to it in instruction.md?
- If the instructions read like a numbered to-do list the agent just
  executes step by step, this is weak.
- Improvement direction: give the agent a situation (broken state, a bug
  report, an ambiguous but discoverable goal) and let it infer the concrete
  requirements from the environment, not from the prompt text.

## B. Output semantics matter
Does the task require producing a semantically correct artifact, or could a
superficially-correct-looking output pass?
- If verification only checks shape/format (file exists, right file
  extension, contains a keyword), this is weak.
- Improvement direction: verifier should check that the artifact actually
  does what it claims to do, not just that it resembles a correct answer.

## C. Correctness is multidimensional
Does correctness depend on multiple interacting properties simultaneously,
e.g.:
- functionality
- determinism
- performance
- safety
- provenance
- structural correctness
- state consistency
- hidden evaluation

A task that only checks one of these (usually "does it run and produce the
right value") is weaker than one that checks several at once.

## D. Constraints interact
Do the task's constraints influence each other, or are they independent
checklist items that can be satisfied one at a time without regard to the
others?
- Weak: "must use Python 3.11" + "must handle nulls" + "must log errors" as
  three unrelated boxes to tick.
- Strong: constraints that trade off against each other, so satisfying one
  makes another harder, forcing genuine judgment calls.

## E. State is part of the problem
Does the task require reasoning about existing runtime state, intermediate
state, or how the system evolves over the course of the interaction — or is
it purely "edit files, run tests, done"?
- If purely static edit-and-test, consider whether the task can be
  strengthened with state the agent must discover, track, or reconcile.

## F. Hidden semantic verification
Does the verifier test genuine understanding rather than memorization or
formatting? Look for:
- metamorphic tests (same semantic input, different surface form, same
  expected behavior)
- hidden test cases the agent can't see or infer from instruction.md
- structural validation (not just output-value checks)
- semantic equivalence checks (not string/byte equality)
- explicit anti-hardcoding protections (tests that would fail a solution
  that special-cased the visible examples)
