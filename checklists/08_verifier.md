# Checklist: Verifier (tests/)
(REGULATIONS.md §8)

- [ ] environment_mode = "separate"
- [ ] Never relies on hidden oracle artifacts
- [ ] Deterministic: no wall-clock dependence
- [ ] Deterministic: no network dependence
- [ ] Deterministic: no unseeded randomness
- [ ] Does not assert raw environment-dependent values (addresses/PIDs/loader IDs/etc.) — checks invariants or compares against golden values from the same pinned mechanism instead
- [ ] Validates semantics, not superficial formatting
- [ ] Every requirement in instruction.md is tested
- [ ] Edge cases covered
- [ ] Tests cannot be trivially hardcoded/gamed
- [ ] A plausible-but-incorrect implementation fails
- [ ] No oracle leakage
- [ ] pytest-driven (tests/test_outputs.py)

Rating: ✅ / ⚠ / ❌ — justification:
