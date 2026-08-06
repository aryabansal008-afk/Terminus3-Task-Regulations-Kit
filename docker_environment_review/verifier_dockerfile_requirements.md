# tests/Dockerfile (Verifier Image) Requirements

Source: Doc 6. Complements REGULATIONS.md §8 (Verifier) — those items are
about the *tests themselves*; these are specifically about the verifier's
*Dockerfile*.

- Builds independently of `environment/Dockerfile` (consistent with
  `environment_mode = "separate"`).
- Every verifier dependency preinstalled at build time — nothing installed
  at test-run time.
- Parent directories exist for every artifact declared in `task.toml`
  `artifacts` — the verifier shouldn't fail on a missing directory it could
  have created at build time.
- Never depends on network access during testing — no package installs,
  no fetching golden data, no external calls at test-run time. Everything
  the verifier needs is baked into the image at build time.
