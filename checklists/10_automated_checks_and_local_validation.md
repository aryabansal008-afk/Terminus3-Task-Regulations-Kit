# Checklist: Automated Checks / Local Validation
(REGULATIONS.md §10)

- [ ] `stb harbor run -a oracle -p <task-folder>` passes
- [ ] `stb harbor check` passes
- [ ] `stb harbor run -m @openai/gpt-5.6 -p <task-folder> -k 5` run (used to sanity-check difficulty tier — not treated as ground truth)
- [ ] `stb harbor run -m @anthropic/claude-opus-5 -p <task-folder> -k 5` run (same)
- [ ] Environment starts successfully
- [ ] Oracle passes
- [ ] Verifier passes
- [ ] LLM-as-Judge checks pass
- [ ] Final packaging is clean (see 04 + 11)

Rating: ✅ / ⚠ / ❌ — justification:
