# Failure Analysis Before Recalibration

Source: Doc 5. New process step — not present in Docs 1-4. Applies when
actual model evaluation logs or pass rates ARE available (if not
available, skip this file and use tier_qualitative_definitions.md's
qualitative reasoning instead).

## The rule
Never recalibrate a task's declared difficulty tier directly off a raw
pass rate. First separate *why* the model failed:

| Failure cause | What it means | Action |
|---|---|---|
| Genuine task difficulty | Model understood the task, attempted the right approach, and still failed on the engineering challenge itself | This is real signal — use it to inform tier |
| Unclear instructions | Model misunderstood what was being asked | Fix instruction.md first — do NOT recalibrate tier off this data point |
| Verifier bugs | Model may have actually solved the task but the verifier incorrectly failed it (or a broken solution incorrectly passed) | Fix the verifier first — this data point is not usable for calibration until fixed |
| Environment issues | Model failed due to a broken/misconfigured environment, not the task itself | Fix the environment first — not usable for calibration until fixed |
| Flaky behavior | Model's pass/fail was inconsistent across repeated runs of the same solution | Fix determinism first (REGULATIONS.md §8) — flaky results cannot calibrate a tier |

## Process
1. For each failed (or passed) run, classify it into one of the five rows
   above before drawing any conclusion about difficulty.
2. If a meaningful fraction of failures are NOT genuine-task-difficulty
   failures, fix those root causes first, then re-run evaluation.
3. Only recalibrate the declared tier using the genuine-difficulty subset
   of results.
4. Still never assert a specific pass rate as fact if you (the reviewer)
   didn't personally observe the eval logs — describe what the logs show,
   don't extrapolate beyond them.
