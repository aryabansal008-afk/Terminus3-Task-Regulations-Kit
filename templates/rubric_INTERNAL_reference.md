# INTERNAL ONLY — do not include in the submission ZIP

REGULATIONS.md §9 requires a rubric to exist AND requires `rubrics.txt` to
be excluded from the final submission archive (see NOTES_ON_CONFLICTS.md
item 4 for the apparent tension this creates — confirm with your team
exactly where the rubric is meant to live, e.g. inline in task.toml, in a
separate internal review system, etc.).

This file is a scratch template for drafting the rubric content under the
required syntax rules, kept here for your own reference only.

## Rules
- Cumulative score across all lines: between 10 and 40
- At least one line must be a negative reward
- Every line begins with the literal word "Agent"
- Every line ends with ", ±N"
- Positive values must explicitly include "+" (e.g. "+3", not "3")
- Only these magnitudes are allowed: 1, 2, 3, 5 (as ±1/±2/±3/±5)
- ±4 is never allowed, in either direction
- The submission checkbox must remain unchecked until final review

## Draft lines (example structure — replace with real content)

```
Agent <did the correct thing>, +N
Agent <did the correct thing>, +N
Agent <made this specific mistake>, -N
```

Remember: this file itself must NOT end up in the final ZIP as
`rubrics.txt`.
