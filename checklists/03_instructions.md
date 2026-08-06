# Checklist: instruction.md
(REGULATIONS.md §3)

- [ ] Human-written, avoids AI-generated writing patterns
- [ ] Concise: ~2 short paragraphs or <=20 bullets
- [ ] No canary strings
- [ ] No unnecessary verbosity
- [ ] Contains all explicit requirements
- [ ] Contains all implicit expectations needed for success
- [ ] Does not leak oracle logic
- [ ] Uses absolute filesystem paths (e.g. /app/output.json)
- [ ] Required output files/formats explicitly specified
- [ ] Would survive LLM-as-Judge review
- [ ] Sounds like a real engineer's request, not AI-generated text
- [ ] Describes WHAT must be achieved, not HOW to achieve it
- [ ] No implementation walkthroughs, solution hints, API blueprints, excessive formatting, or highlighted solution details
- [ ] Logical instructions not offloaded into environment docs to dodge length limits
- [ ] Supporting spec files (schemas/RFCs/API contracts/business rules) read like genuine engineering docs, not hidden prompts

Rating: ✅ / ⚠ / ❌ — justification:
