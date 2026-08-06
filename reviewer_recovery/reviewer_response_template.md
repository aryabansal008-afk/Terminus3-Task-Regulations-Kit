# Reviewer Recovery Response Template

Source: Doc 3. Use this template when responding to reviewer feedback on a
rejected/flagged task. Fill in every section — do not skip "Clarifications
Needed" if the feedback is ambiguous; ask instead of guessing.

Inputs to gather before starting:
- [ ] Reviewer feedback / rejection reason
- [ ] Requested changes (if itemized separately)
- [ ] Current task files (task.toml, instruction.md, environment/, solution/, tests/)
- [ ] Previous review comments, if this is not the first round

Reviewer feedback is the highest-priority source of truth — do not override
it with your own preferences about the task.

---

## Overall Verdict
Choose exactly one:
- [ ] ✅ Minor Revision
- [ ] ⚠ Major Revision
- [ ] ❌ Rebuild Required

## Root Cause Analysis
(Explain the *real* reason the task was rejected — do not just paraphrase
the reviewer's comment. For each comment, ask: what underlying Terminus 3
guideline does this actually point to, and is it cosmetic, a quality issue,
a verifier issue, an instruction issue, a task-design issue, or a
fundamental design flaw?)

## Reviewer Feedback Mapping

| Reviewer Feedback | Root Cause | Files Affected | Required Fix | Priority |
|---|---|---|---|---|
| | | | | |

## Strong Terminus 3 Evaluation
(See strong_task_principles.md for the full rubric on each.)

| Principle | Rating | Why |
|---|---|---|
| A. Specification Inference | ✅/⚠/❌ | |
| B. Semantic Outputs | ✅/⚠/❌ | |
| C. Multi-dimensional Correctness | ✅/⚠/❌ | |
| D. Interacting Constraints | ✅/⚠/❌ | |
| E. Stateful Reasoning | ✅/⚠/❌ | |
| F. Hidden Semantic Verification | ✅/⚠/❌ | |

## Recovery Plan
(List modifications in execution order, highest to lowest priority. Prefer
targeted edits to instruction.md, verifier, oracle, Docker environment,
hidden tests, or artifacts over redesigning the task itself.)

1. **File(s):**
   **Change:**
   **Reason:**
   **Expected impact:**

## Risk Assessment
Remaining risk of rejection after the proposed fixes:
- [ ] Low
- [ ] Medium
- [ ] High

(Explain what could still cause rejection — and proactively predict what CI,
LLM-as-Judge, Peer Review, GPT-5.6, or Claude Opus 5 evaluation might flag
next even if the current reviewer didn't mention it.)

## Clarifications Needed
(If reviewer feedback is insufficient or ambiguous, list precise questions
here instead of inventing fixes. Leave empty only if genuinely nothing is
ambiguous.)

---

## Critical constraints while filling this out
- Preserve the original task wherever possible.
- Never redesign the task unless it is fundamentally unsalvageable.
- Never introduce ambiguity as a way to increase difficulty.
- Never fabricate reviewer intent or missing information.
- Difficulty must come from domain reasoning, interacting constraints, live
  state, and semantic verification — not obscure wording or hidden
  requirements.
