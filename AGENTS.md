# Multi-Agent Task Distribution Guide

This document defines which AI agent handles which type of work in this project. Use this to route tasks efficiently and maintain context focus.

---

## Agent Profiles & Specializations

### 🔧 Claude Code (Premium/High-Token Budget)
**Use For:**
- SSH operations and remote server access
- Entity registry edits (`.storage/core.entity_registry`)
- Live debugging with server logs
- Breaking changes or risky deployments
- Custom component patches
- Python script development and testing
- Complex yaml validation before deployment
- Rollback procedures

**Cost Profile:** High — Use for critical/complex operations only

**Example Task:** "Fix broken light groups by editing entity registry"

---

### 📝 Codex (VS Code, Fast, Included in ChatGPT)
**Use For:**
- YAML automation drafting
- Documentation writing (README, guides, CHANGELOG)
- File refactoring and organization
- Linting and style improvements
- Code review comments
- Blueprint creation
- Config file organization
- Markdown formatting

**Cost Profile:** Included in ChatGPT plan

**Example Task:** "Draft new automation for motion-triggered lights"

---

### 💬 ChatGPT (Quick, General Purpose)
**Use For:**
- Brainstorming and planning
- Quick question answering
- Agent coordination and task routing
- General Home Assistant questions
- Summarizing conversations
- High-level architecture discussions

**Cost Profile:** Included in ChatGPT Plus

**Example Task:** "Should we use a scene or automation for this?"

---

### 🔍 Perplexity Pro (Research, Citations)
**Use For:**
- Finding current HA documentation
- Researching new integrations or components
- Solving unfamiliar problems with citations
- Finding alternatives or best practices
- Deep technical research
- Version compatibility checks

**Cost Profile:** Pro subscription

**Example Task:** "What's the best way to integrate Tesla with latest HA?"

---

### 📊 Gemini / NotebookLM (Long-Form Analysis)
**Use For:**
- Summarizing large codebases or documents
- Analyzing entity audit reports
- Creating visual summaries
- Long document analysis
- Audio summary generation
- Pattern detection across many files

**Cost Profile:** Free for basic, Pro for advanced

**Example Task:** "Analyze the entity_audit_report.md and summarize orphaned entities"

---

### ⚡ Haiku or Fast Models (Syntax Checks)
**Use For:**
- Simple YAML syntax validation
- Quick file format checks
- Small code snippets
- Simple lookups (entity names, file paths)

**Cost Profile:** Very low token cost

**Example Task:** "Check if this YAML is valid"

---

## Decision Tree for Task Routing

```
START: You have a task

├─ Does it require SSH/server access?
│  └─ YES → Claude Code
│
├─ Is it YAML/automation/script drafting?
│  └─ YES → Codex (or Codex → Claude Code for deployment)
│
├─ Is it documentation/markdown/README?
│  └─ YES → Codex
│
├─ Does it need research + citations + current info?
│  └─ YES → Perplexity Pro
│
├─ Is it analyzing a large document/codebase?
│  └─ YES → Gemini/NotebookLM
│
├─ Is it brainstorming/quick question/planning?
│  └─ YES → ChatGPT
│
├─ Is it a simple syntax check?
│  └─ YES → Haiku
│
└─ Not sure? → ChatGPT for routing
```

---

## Handoff Protocol

### When One Agent Hands Off to Another:

1. **Update [TASKS.md](TASKS.md):**
   ```markdown
   ### [Task Name]
   **Status:** In Progress → Complete
   **Agent:** CodexAgent → Claude Code
   **Notes:** [What was done, what's next]
   **Git Commit:** [link to commit]
   ```

2. **Make a Git Commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Ready for Claude Code deployment"
   ```

3. **Include Context in Commit Message:**
   ```
   Task: Deploy motion-triggered lighting automation
   
   Codex drafted automation/lighting/motion_sensor.yaml
   Next: Claude Code to validate and deploy to 192.168.4.141
   
   Changes:
   - automations/lighting/motion_sensor.yaml (new)
   - light_groups.yaml (updated)
   
   See TASKS.md for full context.
   ```

4. **Update TASKS.md with Next Agent:**
   ```markdown
   ### Motion-Triggered Lighting
   **Status:** Ready for Deployment
   **Agent:** Claude Code (next)
   **Assigned To:** @claude-code
   ```

---

## Context Preservation Strategy

### Per-Agent Context Files

**For all agents:** Start with [CONTEXT.md](CONTEXT.md) (1-page quick ref)

**For Codex:** Focus on [HOME_ASSISTANT.md](HOME_ASSISTANT.md) (documentation foundation)

**For Claude Code:** Focus on [copilot-instructions.md](.github/copilot-instructions.md) (ops procedures)

**For Perplexity:** Keep [DECISIONS.md](DECISIONS.md) for context on prior choices

**For Gemini:** Point to analysis files like `entity_audit_report.md`

---

## Example Workflows

### Workflow: Add New Automation

**Step 1 - Brainstorm (ChatGPT)**
```
"I want an automation that dims lights at sunset. 
Should I use triggers or conditions? Automation or script?"
```

**Step 2 - Draft (Codex)**
```
"Draft an automation for dimming lights at sunset using hue lights.
Store in automations/lighting/sunset_dimming.yaml"
```

**Step 3 - Validate & Deploy (Claude Code)**
```
"Validate and deploy automations/lighting/sunset_dimming.yaml to 192.168.4.141"
```

**Step 4 - Update Docs (Codex)**
```
"Update CHANGELOG.md with new sunset dimming automation feature"
```

---

### Workflow: Fix Entity Registry Issue

**Step 1 - Diagnose (Claude Code)**
```
"SSH to 192.168.4.141 and check if light.living_room_ceiling exists in entity registry"
```

**Step 2 - Research (Perplexity)**
```
"Why might a light entity disappear from Home Assistant registry? 
What's the best way to recover it?"
```

**Step 3 - Fix (Claude Code)**
```
"Use ha core stop/start to edit entity registry and restore the light entity"
```

**Step 4 - Document (Codex)**
```
"Write a troubleshooting guide for entity registry issues in HOME_ASSISTANT.md"
```

---

### Workflow: Analyze Bloat & Cleanup

**Step 1 - Analyze (Gemini/NotebookLM)**
```
"Summarize entity_audit_report.md — how many orphaned/duplicate entities?"
```

**Step 2 - Plan (ChatGPT)**
```
"Should we clean up orphaned entities? What's the safest approach?"
```

**Step 3 - Execute (Claude Code)**
```
"Run ha_registry_cleanup.py to remove orphaned entities"
```

**Step 4 - Update Docs (Codex)**
```
"Document the cleanup in CHANGELOG.md and CLEANUP_LOG.md"
```

---

## Task Status Labels

Use these in [TASKS.md](TASKS.md) to track progress:

- **Not Started** — Task queued, no work begun
- **In Progress** — Agent actively working
- **Ready for Review** — Completed by agent, waiting for another agent
- **Review In Progress** — Second agent reviewing
- **Complete** — Deployed and verified
- **Blocked** — Waiting on external resource or decision
- **Deferred** — Deprioritized but not abandoned

---

## Best Practices

### For You (Project Owner)

1. **Keep [TASKS.md](TASKS.md) as source of truth** for what needs to happen
2. **Make commits between agent handoffs** — Gives agents clear checkpoints
3. **Use commit messages for context** — Agents can read git log to understand decisions
4. **Review agent work before deployment** — Final safety check before pushing to server
5. **Update [DECISIONS.md](DECISIONS.md)** when major architectural choices are made

### For Agents

1. **Always read [CONTEXT.md](CONTEXT.md) first** — 2-minute quick ref
2. **Check [TASKS.md](TASKS.md)** for your assignment
3. **Reference [copilot-instructions.md](.github/copilot-instructions.md)** for project-specific practices
4. **Update [TASKS.md](TASKS.md) when starting/finishing**
5. **Make small, focused commits** — Easier for next agent to review
6. **Leave notes in task updates** — Explain context for handoff

---

## Quick Agent Selection Cheat Sheet

| Task Type | Agent | Time Estimate |
|-----------|-------|----------------|
| Brainstorm feature | ChatGPT | 5 min |
| Draft YAML automation | Codex | 10-20 min |
| Validate & deploy | Claude Code | 15-30 min |
| Research best practice | Perplexity | 10-15 min |
| Analyze large document | Gemini | 10 min |
| Fix SSH/server issue | Claude Code | 15-45 min |
| Write documentation | Codex | 20-30 min |
| Simple syntax check | Haiku | 2 min |

---

## Getting Started

1. Read [CONTEXT.md](CONTEXT.md) (1 min)
2. Check [TASKS.md](TASKS.md) for your assignment (2 min)
3. Review relevant docs:
   - Codex: [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
   - Claude Code: [copilot-instructions.md](.github/copilot-instructions.md)
   - Perplexity: [DECISIONS.md](DECISIONS.md)
4. Make a commit when starting: `git commit -m "Task: [name] - Starting"`
5. Work in focused blocks (30-60 min)
6. Commit when done: `git commit -m "Task: [name] - Complete"`
7. Update [TASKS.md](TASKS.md) with results
8. If handing off, update task with "Ready for [Next Agent]"
