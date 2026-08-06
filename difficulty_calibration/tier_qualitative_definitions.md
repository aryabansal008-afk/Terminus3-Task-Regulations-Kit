# Difficulty Tier Definitions — Qualitative + Quantitative

Two complementary views of the same four tiers now exist in the source
prompts. They are consistent with each other (not conflicting) — use both
together: the qualitative description tells you *what kind* of task
belongs in a tier; the pass-rate band tells you *how often* a frontier
model should be expected to solve it.

| Tier | Qualitative description (Doc 5) | Expected pass rate (Doc 2) |
|---|---|---|
| **Frontier** | Specification inference, interacting correctness axes, semantic artifacts, deep domain reasoning | <20% |
| **Advanced** | Clear goal but difficult execution, interacting constraints, stateful reasoning | 20–50% |
| **Core** | Well-specified multi-step task with meaningful edge cases | 50–80% |
| **Base** | Non-trivial but readily solvable by a competent frontier model | 80–100% |

## How to use this when calibrating a task

1. Never invent or assert a specific pass rate as fact.
2. If actual evaluation logs/results from GPT-5.6 or Claude Opus 5 are
   available, treat them as the source of truth over any qualitative
   reasoning below.
3. Otherwise, reason qualitatively: which row's *description* best matches
   the task's actual design? That's your best-guess tier — state it as
   reasoning, not as a measured fact.
4. The single biggest lever between Advanced and Frontier is usually
   **specification inference**: does the agent have to discover the
   relevant decomposition of the problem itself, or is it handed to them
   explicitly in instruction.md? A task whose instructions already spell
   out the exact subsystems/axes involved is pulled toward Advanced/Core
   even if the underlying engineering is hard; a task that only describes
   symptoms and requires the agent to find the decomposition itself is
   pulled toward Frontier.
