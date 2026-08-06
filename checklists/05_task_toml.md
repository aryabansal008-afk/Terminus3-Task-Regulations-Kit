# Checklist: task.toml
(REGULATIONS.md §5 — see NOTES_ON_CONFLICTS.md item 1 for timeout ambiguity)

Fields:
- [ ] name
- [ ] category
- [ ] subcategory
- [ ] tags (3-6)
- [ ] languages
- [ ] difficulty
- [ ] expert_time_estimate_hours
- [ ] author_name
- [ ] author_email
- [ ] artifacts
- [ ] difficulty_explanation
- [ ] solution_explanation
- [ ] verification_explanation
- [ ] relevant_experience

[agent]:
- [ ] timeout_sec set (confirm current minimum — see conflicts note)
- [ ] appropriate for expected runtime

[verifier]:
- [ ] timeout_sec set
- [ ] environment_mode = "separate"

[environment]:
- [ ] build_timeout_sec set
- [ ] network_mode = "public" unless offline required
- [ ] resource footprint ~2 CPU / 8GB RAM / 10GB storage
- [ ] no GPU dependency

Rating: ✅ / ⚠ / ❌ — justification:
