# Checklist: Standalone, Internet, Language Compliance
(REGULATIONS.md §1 — new/refined items from Doc 4)

- [ ] Standalone: completes without human interaction after launch
- [ ] All inputs come from files, flags, or environment variables (not stdin prompts mid-run)
- [ ] network_mode = "public" unless offline execution is genuinely required
- [ ] Runtime tests (verifier) never fetch from the network, regardless of network_mode
- [ ] Primary language(s) correctly declared in task.toml `languages`
- [ ] Considered whether a natural multi-language design would strengthen the task (not forced)

Rating: ✅ / ⚠ / ❌ — justification:
