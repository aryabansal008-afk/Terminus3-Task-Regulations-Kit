# Difficulty Evaluation Response Template

Source: Doc 5. Use this when calibrating a task's declared difficulty.

Constraints while filling this out:
- Never invent GPT-5.6 or Claude Opus 5 pass rates.
- Treat measured evaluation results as authoritative when provided —
  otherwise, reason qualitatively (see tier_qualitative_definitions.md)
  and say so explicitly.
- Preserve the original task objective; recommend only the smallest
  changes needed to reach the intended tier.
- If a declared tier isn't available (task.toml wasn't provided), say so
  and skip only section 6 rather than guessing.

---

## 1. Expected Difficulty Tier
(Frontier / Advanced / Core / Base — state your best assessment.)

## 2. Reasoning
(Why this tier — tie back to the qualitative definitions and, if
available, the pass-rate band.)

## 3. Strengths Contributing to Difficulty
(Which legitimate difficulty sources — see
legitimate_vs_artificial_difficulty.md — are actually present.)

## 4. Artificial Difficulty or Weaknesses
(Any of the artificial-difficulty sources present, or open questions that
can't be assessed without more materials — flag rather than assume.)

## 5. Recommended Improvements (if any)
(Only legitimate escalation levers: stronger specification inference,
interacting constraints, richer semantic verification, additional hidden
correctness dimensions. Never recommend ambiguity, unnecessary
requirements, or longer instructions as a way to raise difficulty.)

## 6. Difficulty Consistency Check
(Does task.toml's declared difficulty match the expected/measured tier?
Skip with a note if the declared tier wasn't provided.)
