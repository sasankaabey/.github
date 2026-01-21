# Session Router: Intelligent Multi-Agent Task Orchestration

**Purpose:** Automatically analyze project state, rank backlog items, decompose tasks, and generate agent-specific prompts with handoff instructions.

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Date:** 2026-01-21

---

## What Is This?

The Session Router is a **decision engine** that sits in your repo and orchestrates work across multiple AI agents. Instead of manually deciding what to work on, the router:

1. **Analyzes your entire workspace** (all projects' TASKS.md files)
2. **Shows ranked backlog** with "pick up where you left off" option
3. **Decomposes selected task** into sequential/parallel subtasks
4. **Generates agent-specific prompts** with context and handoff instructions
5. **Tracks progress** and knows what subtask comes next

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ User runs: ./session_start.sh                           │
└─────────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────────────────────┐
        │   Phase 1: Health Check       │
        │   (Log Monitor - dry-run)     │
        └───────────────────────────────┘
                        ↓
        ┌───────────────────────────────┐
        │   Phase 2: Task Router        │
        │   • Show backlog by project   │
        │   • User selects task         │
        │   • Decompose into subtasks   │
        │   • Generate first prompt     │
        └───────────────────────────────┘
                        ↓
        ┌───────────────────────────────┐
        │ Agent gets prompt with:       │
        │ • Context files to read       │
        │ • Specific instructions       │
        │ • Success criteria            │
        │ • Handoff instructions        │
        └───────────────────────────────┘
                        ↓
        Agent completes work + commits
                        ↓
        User runs: ./session_start.sh --next
                        ↓
        Router generates next subtask prompt
                        ↓
        Repeat until task complete
```

---

## Quick Start

### First Time Setup

1. **Ensure TASKS.md exists in each project:**
   ```bash
   cd ~/Developer/sasankaabey/home-assistant-config
   # Make sure TASKS.md exists with proper format
   ```

2. **Add shell alias (optional but recommended):**
   ```bash
   echo "alias work='~/.github/scripts/session_start.sh'" >> ~/.zshrc
   source ~/.zshrc
   ```

### Daily Workflow

```bash
# Start your session
work

# (Shows backlog with ranked options)
# Select a task by number

# Copy the generated prompt
# Paste into your agent (Claude Code, Codex, ChatGPT, etc.)

# Agent completes work and commits

# Get next subtask
work --next

# Repeat until task complete
```

---

## Usage Examples

### Example 1: Interactive Mode (Default)

```bash
$ ./session_start.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Phase 1: System Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📡 Fetching logs from HA server...
✅ Retrieved 100 lines
🔬 Analyzing logs...
✅ Found 0 potential issues

✅ System healthy - no critical issues detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Phase 2: Task Selection & Agent Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

======================================================================
🎯 SESSION START - Task Backlog
======================================================================

🔄 CONTINUE LAST TASK?

  [0] Continue: Implement Tuya light renaming
      Status: In Progress
      Last worked: 2026-01-21 14:30
      Agent: Codex

----------------------------------------------------------------------

📁 HOME-ASSISTANT-CONFIG

  [1] 🔵 Implement Tuya light renaming ⬆️
      Codex • 30min • In Progress

  [2] ⚪ Add motion-triggered lighting automation 🔥
      Codex • 45min • Not Started
      ⛓️  Blocks 2 other task(s)

  [3] ⚪ Music Assistant entity cleanup
      Codex • 20min • Not Started
      🔒 Blocked by: Tuya light renaming

📁 KITLABWORKS

  [4] ⚪ Implement user authentication
      Claude Code • 60min • Not Started

  [5] ⚪ Add database schema migrations
      Codex • 30min • Not Started

======================================================================
Enter task number (or 0 to continue last task): 0
```

**User selects 0 (continue last task)**, gets this prompt:

```markdown
# AGENT ASSIGNMENT: Codex

## 🎯 Your Task

**Draft YAML for: Implement Tuya light renaming**

**Project:** home-assistant-config
**Estimated Time:** 15 minutes
**Priority:** HIGH

---

## 📖 Context to Read First

1. home-assistant-config/HOME_ASSISTANT.md#entity-naming-conventions
2. home-assistant-config/light_groups.yaml
3. home-assistant-config/DECISIONS.md

---

## 🔨 What You Need to Do

**As Codex, your role is:**
- Documentation writing
- YAML drafting
- Code formatting
- PR reviews

**For this task:**
1. Read the context files listed above
2. Draft YAML for: Implement Tuya light renaming
3. Follow conventions documented in home-assistant-config/LOCAL_CONTEXT.md
4. Commit your work with clear messages

---

## ✅ Success Criteria

- [ ] Task completed: Draft YAML for: Implement Tuya light renaming
- [ ] Code follows project conventions
- [ ] Changes committed to git
- [ ] TASKS.md updated with progress
- [ ] Documentation is clear and complete
- [ ] YAML is valid (if applicable)

---

## 📝 Commit Instructions

When you complete this work:

1. **Commit your changes** with message:
   ```
   Task: Implement Tuya light renaming - Draft YAML for: Implement Tuya light renaming
   
   Completed by Codex
   Part of larger task decomposition
   
   Status: In Progress - Next: Claude Code
   ```

2. **Update TASKS.md** to mark this subtask as complete

3. **Hand off to next agent:**

   Run `./session_start.sh --next` to get the next prompt.
   
   **Next Agent:** Claude Code
   **Next Task:** Validate and deploy: Implement Tuya light renaming

---

## 🔄 Handoff Protocol

**IMPORTANT:** When you finish:
1. Commit your work
2. Push to git
3. Tell the user: "Run `./session_start.sh --next` to continue"

The router will automatically detect your completed work and generate the next prompt.

---
```

### Example 2: Auto-Continue Mode

```bash
# After agent completes work and commits
$ ./session_start.sh --next

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Phase 1: System Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ System healthy - no critical issues detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Phase 2: Task Selection & Agent Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

======================================================================
📋 NEXT TASK PROMPT
======================================================================

# AGENT ASSIGNMENT: Claude Code

## 🎯 Your Task

**Validate and deploy: Implement Tuya light renaming**

**Project:** home-assistant-config
**Estimated Time:** 15 minutes
**Priority:** HIGH

...
[Full prompt for Claude Code with deployment instructions]
```

### Example 3: Health Check Only

```bash
# Just check system health without routing
$ ./session_start.sh --health

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Phase 1: System Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📡 Fetching logs from HA server...
[Full log monitor output]

Exit code: 0 (healthy)
```

---

## Task Decomposition Patterns

The router automatically breaks down tasks based on patterns:

### Pattern 1: Implementation Task
```
Task: "Implement user authentication"
    ↓
Subtasks:
1. Plan implementation (ChatGPT, 10min)
2. Implement code (Assigned Agent, 40min) [depends on #1]
3. Test implementation (Claude Code, 10min) [depends on #2]
```

### Pattern 2: Documentation Task
```
Task: "Document API endpoints"
    ↓
Subtasks:
1. Research endpoints (Perplexity, 15min) [parallel]
2. Write documentation (Codex, 15min) [depends on #1]
```

### Pattern 3: Home Assistant Automation
```
Task: "Add motion-triggered lighting"
    ↓
Subtasks:
1. Draft YAML (Codex, 20min)
2. Validate and deploy (Claude Code, 10min) [depends on #1]
```

### Pattern 4: Simple Task (No Decomposition)
```
Task: "Fix typo in README"
    ↓
Subtask:
1. Fix typo (Codex, 5min) [no decomposition needed]
```

---

## State Management

The router maintains state in `.github/session_state.json`:

```json
{
  "last_task_id": "home-assistant-config_implement_tuya_light_renaming",
  "last_subtask_id": "home-assistant-config_implement_tuya_light_renaming_yaml",
  "last_agent": "Codex",
  "last_updated": "2026-01-21T14:30:00",
  "completed_subtasks": [
    "home-assistant-config_implement_tuya_light_renaming_plan"
  ]
}
```

**How it works:**
- Router checks git log for completed work
- If last subtask ID appears in recent commit → mark as complete
- Automatically moves to next subtask in dependency chain
- Handles both sequential and parallel subtasks

---

## TASKS.md Format Requirements

For the router to work correctly, TASKS.md must follow this format:

```markdown
### Task Name Here

**Status:** Not Started | In Progress | Blocked | Ready for Review | Complete
**Priority:** CRITICAL | HIGH | MEDIUM | LOW | DEFERRED
**Agent:** Codex | Claude Code | ChatGPT | Perplexity | Gemini
**Estimated Time:** 20-30 minutes | 1 hour | etc.
**Context to Read First:**
  1. path/to/file.md
  2. path/to/another.yaml

**Description:**
Brief description of what needs to be done...

**Dependencies:** (optional)
- Blocks: Task Name 1, Task Name 2
- Blocked by: Task Name 3
```

**Example:**

```markdown
### Rename Tuya Lights to Standard Convention

**Status:** In Progress
**Priority:** HIGH
**Agent:** Codex
**Estimated Time:** 20-30 minutes
**Context to Read First:**
  1. HOME_ASSISTANT.md#entity-naming-conventions
  2. light_groups.yaml
  3. DECISIONS.md#tuya-integration

**Description:**
Rename 8 Tuya smart lights to follow standard entity naming convention
(light.{location}_{description}). This unblocks Music Assistant cleanup.

**Dependencies:**
- Blocks: Music Assistant entity cleanup
```

---

## Command Reference

```bash
# Interactive mode (show backlog, user selects)
./session_start.sh

# Auto-continue last task (after agent commits work)
./session_start.sh --next

# Re-show last task prompt (if lost)
./session_start.sh --last

# Health check only (no task routing)
./session_start.sh --health

# Pass options to log monitor
./session_start.sh --health --lines 200
```

---

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success (task selected or system healthy) | Proceed with work |
| 1 | High priority health issues | Review issues, proceed with caution |
| 2 | Critical health issues | Fix critical issues first |
| Other | Router error | Check logs |

---

## Troubleshooting

### "No previous task found"
**Problem:** Running `--next` but no state file exists.  
**Solution:** Run `./session_start.sh` (interactive mode) first to select a task.

### "Could not find task: [ID]"
**Problem:** Task ID in state file doesn't match current TASKS.md.  
**Solution:** Task was deleted or renamed. Run interactive mode to select a new task.

### "Invalid choice"
**Problem:** Entered invalid number in backlog selection.  
**Solution:** Enter a valid option number from the backlog.

### State file out of sync
**Problem:** Router thinks subtask is incomplete but it's actually done.  
**Solution:** Manually edit `.github/session_state.json` to update `completed_subtasks` array.

### Task not decomposing correctly
**Problem:** Router creates wrong subtasks for your task type.  
**Solution:** Edit `TaskDecomposer.decompose_task()` in `session_router.py` to add your pattern.

---

## Customization

### Add New Decomposition Pattern

Edit `session_router.py`, find `TaskDecomposer.decompose_task()`:

```python
# Pattern: Your New Task Type
elif "your_keyword" in task.name.lower():
    subtasks = [
        Subtask(
            id=f"{task.id}_step1",
            description=f"First step: {task.name}",
            agent=AgentType.CHATGPT,
            estimated_minutes=10,
            parallel_ok=False
        ),
        Subtask(
            id=f"{task.id}_step2",
            description=f"Second step: {task.name}",
            agent=AgentType.CODEX,
            estimated_minutes=20,
            dependencies=[f"{task.id}_step1"],
            parallel_ok=False
        )
    ]
```

### Customize Prompt Generation

Edit `PromptGenerator.generate_prompt()` to change prompt format.

### Add New Agent Type

Edit `AgentType` enum in `session_router.py`:

```python
class AgentType(Enum):
    ...
    YOUR_NEW_AGENT = "Your Agent Name"
```

---

## Integration with Other Tools

### With Git Hooks
```bash
# Post-commit hook to suggest next task
echo '#!/bin/bash
if grep -q "Task:" "$(git log -1 --pretty=%B)"; then
    echo ""
    echo "💡 Run: ./session_start.sh --next"
    echo ""
fi' > .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

### With VS Code Tasks
```json
{
  "label": "Start Session",
  "type": "shell",
  "command": "${workspaceFolder}/.github/scripts/session_start.sh",
  "problemMatcher": []
}
```

---

## Roadmap (Future Enhancements)

- [ ] ML-based task priority prediction
- [ ] Automatic detection of blockers from git log
- [ ] Parallel task execution suggestions
- [ ] Integration with GitHub Issues
- [ ] Slack notifications when task ready
- [ ] Time tracking and velocity metrics
- [ ] Auto-assignment based on agent availability

---

## Architecture Decisions

### Why Decompose Tasks?
- **Smaller units of work** = easier to hand off between agents
- **Clear dependencies** = know what can run in parallel
- **Agent specialization** = right tool for the job
- **Progress tracking** = know exactly where you are

### Why State File Instead of Git?
- **Fast reads** = no git parsing needed
- **Atomic updates** = JSON write is atomic
- **Query-friendly** = easy to check completion status
- **Portable** = works across all agents

### Why Prompts Instead of Agent API Calls?
- **Agent-agnostic** = works with any AI (Claude, GPT, Gemini, etc.)
- **Human-in-the-loop** = you control handoffs
- **Transparent** = see exactly what agent will do
- **Flexible** = change prompt before pasting

---

## FAQ

**Q: Can I skip the health check?**  
A: Yes, run `./session_start.sh --skip-health` (not yet implemented—coming soon)

**Q: What if I want to work on a different task mid-way?**  
A: Run interactive mode again: `./session_start.sh` and select a new task

**Q: Can two agents work on same task in parallel?**  
A: Yes! Router marks subtasks as `parallel_ok=True` when safe

**Q: How do I add a task without editing TASKS.md manually?**  
A: Coming soon: `./session_router.py --add-task` command

**Q: Can this work with GitHub Copilot Agent?**  
A: Yes! Copilot can use the generated prompts just like any other agent

**Q: What about non-code tasks (design, meetings, etc.)?**  
A: Add them to TASKS.md with appropriate agent assignments (or use "Manual")

---

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Agent roles and decision tree
- [MULTI_AGENT_WORKFLOW.md](../MULTI_AGENT_WORKFLOW.md) - Workflow process
- [LOG_MONITOR_AGENT.md](../LOG_MONITOR_AGENT.md) - Health check details
- [EVOLUTION_LOG.md](../EVOLUTION_LOG.md) - What we learned

---

**Implementation Date:** 2026-01-21  
**Status:** ✅ Production Ready  
**Maintainer:** Multi-Agent System
