# Legitimate vs. Artificial Difficulty

Source: Doc 5 ("Difficulty Evaluation & Calibration Prompt"). Largely
reinforces reviewer_recovery/strong_task_principles.md and
REGULATIONS.md §14 (Common Rejection Reasons) — cross-referenced below
rather than duplicated wholesale.

## Difficulty SHOULD come from
| Legitimate source | Cross-reference |
|---|---|
| Inferring the problem/contract from realistic domain evidence | Strong Task Principle A |
| Multi-step reasoning with intermediate state, branching, or recovery | REGULATIONS.md §1 |
| Multiple interacting correctness constraints | Strong Task Principle D |
| Producing a semantically correct artifact, not superficial matching | Strong Task Principle B |
| Hidden semantic verification testing understanding, not memorization | Strong Task Principle F |

## Difficulty should NOT come from
| Artificial source | Cross-reference | Notes |
|---|---|---|
| Ambiguous or incomplete instructions | REGULATIONS.md §3, §14 | |
| Excessive independent requirements | Strong Task Principle D | the tell: requirements that can each be satisfied one at a time without regard to the others |
| Obscure trivia | new term (Doc 5) | knowledge so narrow/unusual it can't reasonably be inferred from the environment or common engineering knowledge — different from "deep domain reasoning," which Doc 5 treats as *legitimate* |
| Environment defects | REGULATIONS.md §6 | e.g. a broken Dockerfile that happens to make the task harder is not real difficulty |
| Flaky or non-deterministic tests | REGULATIONS.md §8 | |
| Artificially long workflows | REGULATIONS.md §14 ("Preserve Difficulty") | padding step count without adding reasoning |

## The "obscure trivia vs. deep domain reasoning" distinction
This is the subtlest line in Doc 5 and worth calling out on its own: a task
requiring genuinely deep, narrow domain knowledge is *legitimately* hard
(Frontier-tier material) as long as the agent can reconstruct or discover
that knowledge from evidence available in the task's environment (source
code, comments, fixture behavior, documentation-like spec files). The same
knowledge requirement becomes *artificial* difficulty if the agent is
expected to already know it cold with no way to derive it from what's
provided. When reviewing a deep-domain task, always ask: "if the agent
didn't already know this, could it figure it out from what's here?" If no,
that's a real risk to flag — even though the domain content itself is
legitimate.
