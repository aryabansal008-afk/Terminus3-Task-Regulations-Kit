# Common Terminus 3 Rejection Reasons

Source: Doc 3. Use this as a scan list when a task has been rejected, or
proactively before submission. Each item cross-references the relevant
REGULATIONS.md section so a detected issue maps back to a concrete fix.

For each, when actually reviewing: explain why it applies, estimate
severity (Low / Medium / High), and propose the smallest fix — don't
redesign the task to fix it unless nothing smaller will work.

| Rejection reason | Cross-reference |
|---|---|
| Too easy | REGULATIONS.md §2 Difficulty; §1 Task Design |
| Ambiguous requirements | REGULATIONS.md §3 Instructions; Principle A (specification must be inferred, but *discoverable*, not ambiguous) |
| Similar to existing tasks | REGULATIONS.md §1 Novelty |
| Reskinned benchmark | REGULATIONS.md §1 Novelty |
| Hidden knowledge unavailable to the agent | REGULATIONS.md §3 Instructions ("every requirement inferable from provided materials") |
| Non-deterministic behavior | REGULATIONS.md §7 Oracle, §8 Verifier |
| Shortcut solutions | REGULATIONS.md §7 Oracle ("does not shortcut the task") |
| Oracle leakage | REGULATIONS.md §8 Verifier |
| Tests validate formatting rather than meaning | Principle B (Output semantics matter); REGULATIONS.md §8 Verifier |
| Single-command solution | REGULATIONS.md §1 Task Design |
| Straight-line execution | REGULATIONS.md §1 Task Design; Principle E (state is part of the problem) |
| Weak verifier | REGULATIONS.md §8 Verifier; Principle F (hidden semantic verification) |
| Poor novelty | REGULATIONS.md §1 Novelty |

## Important framing (Doc 3, "Preserve Difficulty")

If a task is rejected as "too easy," the fix is **not** to make it harder by:
- hiding requirements from the agent
- introducing ambiguity
- adding unnecessary steps

Difficulty should instead come from:
- reasoning
- inference
- interacting constraints (Principle D)
- system/state behavior (Principle E)
- semantic verification depth (Principle F)

A task made harder by obscuring information is a different kind of failure,
not a fix — flag this distinction explicitly if you see it being proposed
as a "fix."
