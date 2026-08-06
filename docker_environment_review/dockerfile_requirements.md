# Dockerfile Requirements (environment/Dockerfile — agent image)

Source: Doc 6. Note: "Sanctioned" below was actually present in Doc 1 too
but was missed when REGULATIONS.md §6 was first written — fixed now.

- **Reproducible**: every dependency version-pinned; no nondeterministic
  build steps.
- **Digest-pinned**: every `FROM` uses `@sha256:<digest>` — never a
  floating tag.
- **Sanctioned**: the final runtime image uses an approved Terminal-Bench
  base image, or the Dockerfile includes a clear written justification for
  a non-canonical base. (Doc 1 + Doc 6 — previously under-documented in
  this kit, now restored.)
- **Cache-friendly**: layers ordered from stable dependencies →
  frequently-changing task files, so edits to task files don't invalidate
  expensive dependency-install layers.
- **Build-efficient**:
  - consolidate `apt` operations into as few `RUN` layers as practical
  - never `apt-get upgrade` (breaks reproducibility/pinning)
  - clean package caches (`rm -rf /var/lib/apt/lists/*` etc.) in the SAME
    layer as the install, not a later layer (a later layer doesn't shrink
    the image — the deleted files are already in an earlier layer)
  - use multi-stage builds when compilation is required, so build-only
    tooling doesn't ship in the final image
- **Complete**: all task dependencies installed at build time. Neither the
  agent nor the verifier installs packages during execution — no runtime
  `apt-get`/`pip install`/`cargo install`/`go install` inside solve.sh,
  test.sh, or anything the agent is expected to run.
- **Runtime-ready**: `tmux` and `asciinema` installed in the agent image.
- **Isolated**: never copied into the agent image —
  - `solution/`
  - hidden tests
  - secrets / credentials
  - expected outputs / golden values
  - any verifier-only assets
- **Minimal**: no unnecessary build tools, package caches, credentials,
  `.git`, virtual environments, or oversized datasets remain in the final
  image.
- **Resource-aware**: compatible with the specific limits declared in this
  task's `task.toml` (not just the general ~2 CPU/8GB/10GB target — check
  the actual declared values).
