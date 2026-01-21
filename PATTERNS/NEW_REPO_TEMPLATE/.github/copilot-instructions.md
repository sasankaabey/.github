# Copilot Instructions — [Project Name]

> **Note:** This file contains project-specific instructions only. For workflow and agent routing, see the [organization-level instructions](https://github.com/sasankaabey/.github).

---

## Quick Links
- **Org-level workflow**: See `sasankaabey/.github/MULTI_AGENT_WORKFLOW.md`
- **Agent routing**: See `sasankaabey/.github/AGENTS.md`
- **Project context**: See `LOCAL_CONTEXT.md` in this repo
- **Current tasks**: See `TASKS.md` in this repo

---

## Project-Specific Context

[Describe what makes this project unique: tech stack, architecture, deployment, constraints, etc.]

Example:
- **Tech stack**: Python 3.11, Home Assistant, YAML configs
- **Deployment**: Raspberry Pi at 192.168.4.141
- **Key constraints**: No breaking changes to existing automations
- **Testing approach**: Validate YAML before deploy, test on staging first

---

## Project-Specific Instructions

[Add any project-specific coding standards, patterns, or gotchas here.]

Example:
- Use snake_case for entity IDs
- Always add comments to complex automations
- Test light groups before referencing in automations
- Check entity registry before creating new entities

---

## Learning Escalation

When you discover a **pattern, pitfall, or improvement** that would help other projects:

1. **Document it locally** in `TASKS.md` or commit message
2. **Escalate to org-level** by creating an issue or updating `sasankaabey/.github/EVOLUTION_LOG.md`:
   - What you learned
   - Why it matters
   - How other projects can apply it

Example escalations:
- "Found a better way to validate YAML before deploy → add to org workflow"
- "Discovered common entity naming conflicts → document in org best practices"
- "New handoff pattern works well → update HANDOFF_TEMPLATE.md"

---

## See Also
- [Organization README](https://github.com/sasankaabey/.github/blob/main/README.md)
- [Multi-Agent Architecture](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_ARCHITECTURE.md)
