# Dockerfile Review Response Template

Source: Doc 6. Use when reviewing/improving/generating a Terminus 3 task's
Dockerfile(s).

Constraints while filling this out:
- Preserve the existing Dockerfile unless a change is required.
- Never invent image digests or package versions — use an explicit
  placeholder (e.g. `@sha256:<REPLACE_WITH_DIGEST>`) and flag it as
  something the author must fill in, rather than guessing a real-looking
  value.
- Never recommend runtime package installation as a fix for anything.
- Prioritize determinism, reproducibility, cacheability, security, and full
  Terminus 3 compliance, in roughly that order when trade-offs arise.

---

## 1. Overall Status
- [ ] ✅ Ready
- [ ] ⚠ Needs Minor Changes
- [ ] ❌ Not Compliant

## 2. Issues Found

| Location | Problem | Why it violates Terminus 3 | Minimal fix |
|---|---|---|---|
| | | | |

## 3. Optimization Suggestions
- **Build reproducibility:**
- **Layer ordering:**
- **Image size:**
- **Security:**
- **Cache efficiency:**

## 4. Compliance Checklist

| Item | Rating |
|---|---|
| Base image | ✅/⚠/❌ |
| Digest pinning | ✅/⚠/❌ |
| Dependency pinning | ✅/⚠/❌ |
| Layer structure | ✅/⚠/❌ |
| Apt usage | ✅/⚠/❌ |
| Multi-stage build | ✅/⚠/❌ |
| Runtime dependencies | ✅/⚠/❌ |
| Agent/verifier isolation | ✅/⚠/❌ |
| .dockerignore | ✅/⚠/❌ |
| COPY strategy | ✅/⚠/❌ |
| Image hygiene | ✅/⚠/❌ |
| Lazy-pull friendliness | ✅/⚠/❌ |
| Resource compatibility | ✅/⚠/❌ |
| OCI metadata labels | ✅/⚠/❌ |
