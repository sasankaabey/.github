# Task Queue

This file tracks the current task queue for this project.

---

## Agent Allocation

For agent roles and routing, see: [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md)

For workflow process, see: [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)

---

## Task Status Labels

- **Not Started** — Task queued, no work begun
- **In Progress** — Agent actively working
- **Ready for Review** — Completed by agent, waiting for another agent
- **Ready for Deployment** — Code complete, waiting for deployment
- **Complete** — Deployed and verified
- **Blocked** — Waiting on external resource or decision
- **Deferred** — Deprioritized but tracked for later

---

## Current Tasks

### [Task Name]

**Status:** Not Started  
**Agent:** [Who should handle this? See org/.github/AGENTS.md]  
**Description:** [1-2 sentence summary of what needs to be done]

**Dependencies:** [Any other tasks that must finish first?]

**Acceptance Criteria:**
- [ ] [How do we know it's done? Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Notes:** [Any additional context, links, or gotchas]

---

### [Task Name 2]

**Status:** In Progress  
**Agent:** Codex  
**Description:** Draft automation for motion-triggered lights

**Progress:**
- [x] Created automation file
- [x] Added to light_groups.yaml
- [ ] Validate and test
- [ ] Document in CHANGELOG

**Next Steps:** Claude Code to validate and deploy

---

## Completed Tasks (Last 10)

### [Completed Task Name]

**Status:** Complete  
**Agent:** Claude Code  
**Completed:** 2026-01-20  
**Deliverables:** [What was produced]  
**Notes:** [Any follow-up or lessons learned]

---

## Backlog (Future Work)

Ideas and tasks for future consideration:

- [ ] [Future task 1]
- [ ] [Future task 2]
- [ ] [Future task 3]

---

## Notes

**Adding a new task?**
1. Use template format above
2. Assign to appropriate agent using [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md) decision tree
3. Set acceptance criteria
4. Commit with message: `Plan: [Task Name] - Added to queue`

**Completing a task?**
1. Move to "Completed Tasks" section
2. Add deliverables and notes
3. Commit with message: `Task: [Task Name] - Complete`
4. If process improved, update [org/.github/EVOLUTION_LOG.md](https://github.com/sasankaabey/.github/blob/main/EVOLUTION_LOG.md)
