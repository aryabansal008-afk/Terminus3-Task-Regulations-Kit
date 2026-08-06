# tools/

Automated, dependency-free helpers that complement `checklists/` — they
catch objective, mechanical violations so human/LLM-as-Judge review time
goes to the judgment calls (novelty, difficulty legitimacy, verifier depth,
instruction tone) that can't be scripted.

## validate_task.py

```
python3 tools/validate_task.py /path/to/task-folder
python3 tools/validate_task.py /path/to/task-folder --strict
```

Requires Python 3.11+ (stdlib only — uses `tomllib` to parse `task.toml`).

For each `REGULATIONS.md` section, prints one of:

- `PASS` — mechanically verified.
- `WARN` — a soft signal worth a human glance (e.g. a heuristic that can
  false-positive, or a reminder about packaging-time file exclusion).
- `FAIL` — a concrete rule violation.
- `MANUAL` — out of scope for automation on purpose; points to the exact
  `checklists/` file that covers it.
- `SKIP` — nothing found to check (e.g. no rubric draft in this folder).

Exit code is non-zero if any `FAIL` was found (or any `WARN` too, with
`--strict`), so it can be dropped into a pre-submission script or CI step
without extra glue.

### What it deliberately does NOT do

- Run `stb harbor ...` — that needs the real Terminus 3 CLI/environment,
  which this kit doesn't assume is installed. See
  `checklists/10_automated_checks_and_local_validation.md` for the manual
  commands to run yourself.
- Judge novelty, difficulty legitimacy, verifier semantic depth, or
  instruction tone — these require actually understanding the task's
  domain and are covered by `checklists/`, `reviewer_recovery/`, and
  `difficulty_calibration/` instead.
- Auto-fix anything. It only reports.

### Adding a new check

Each `REGULATIONS.md` section has a matching `check_*` function in
`validate_task.py`. When a new rule is added to `REGULATIONS.md` (see
"Extending this kit" in the top-level `README.md`):

1. If the rule is objectively checkable (a required field, a forbidden
   string, a syntax pattern), add a check to the matching function — or a
   new one, if it's a genuinely new section.
2. If it requires judgment, add it as a `MANUAL` item pointing at the
   relevant `checklists/` file instead of skipping it silently — the goal
   is that every `REGULATIONS.md` item shows up *somewhere* in the report,
   either as an automated check or an explicit manual pointer.
