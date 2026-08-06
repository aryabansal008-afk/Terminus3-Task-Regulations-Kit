# Checklist: Environment (Docker)
(REGULATIONS.md §6 — see docker_environment_review/ for full detail)

- [ ] Every FROM image is digest-pinned
- [ ] Sanctioned base image, or justification documented for non-canonical base
- [ ] Package versions pinned
- [ ] Dockerfile builds successfully
- [ ] solution/ never copied into the environment image
- [ ] tests/ never copied into the environment image
- [ ] Secrets/credentials, expected outputs, verifier-only assets never copied into agent image
- [ ] Verifier image contains all required test dependencies
- [ ] Environment is reproducible; no nondeterministic build steps
- [ ] Parent directories for every referenced artifact already exist
- [ ] tmux installed
- [ ] asciinema installed
- [ ] Cache-friendly layer ordering (stable deps before task files)
- [ ] apt operations consolidated; no apt-get upgrade; caches cleaned same layer
- [ ] Multi-stage build used if compilation required
- [ ] No runtime package installation by agent or verifier
- [ ] No oversized bundled files; under size limits
- [ ] Appropriate .dockerignore
- [ ] Resource-aware against THIS task's declared task.toml limits

Rating: ✅ / ⚠ / ❌ — justification:
