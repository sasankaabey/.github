# Session Starter Prompt

Use this prompt at the beginning of any coding session with any agent. The agent will guide you through project selection and task planning **across all your projects**.

---

## Copy-Paste This Prompt (Cross-Project View)

```
Session start:

1. **Scan workspace**: Look for all repos in ~/[username]/ with a TASKS.md file
2. **Read all TASKS.md**: For each project, identify:
   - What the project is (from LOCAL_CONTEXT.md if it exists)
   - In-progress tasks with who's working on them
   - Recently completed tasks (last 2-3)
   - High-priority backlog items
3. **Present numbered options**: Show me a menu like:
   
   "**IN PROGRESS:**
   [1] Home Assistant: Update kitchen motion lights (Claude Code)
   [2] Data Scripts: Refactor pipeline (Codex)
   
   **HIGH PRIORITY BACKLOG:**
   [3] Home Assistant: Fix Tuya light naming (Claude Code)
   [4] Home Assistant: Clean up Music Assistant entities (Codex)
   [5] Personal Website: Update portfolio section (Codex)
   
   **OTHER OPTIONS:**
   [6] Show full backlog for a specific project
   [7] Start something completely new
   
   **Enter 1-7, or describe what you want to work on:**"

4. **Let me choose by number**: I can respond with:
   - "1" → Continue that in-progress task
   - "3" → Start that backlog item
   - "7" → You ask me what new thing I want to do
   - Or I describe: "I want to add a plant watering automation"
   
5. **Capture details**: Ask clarifying questions about what I want to do

6. **Navigate & update**: 
   - cd to the right repo
   - Update TASKS.md with task details
   - Route to correct agent (reference org/.github/AGENTS.md)
   
7. **Start work**: Execute following org/.github/MULTI_AGENT_WORKFLOW.md

Be conversational and help me prioritize across all my projects.
```

---

## How It Works

**You paste this** → Agent scans ALL your projects → Shows consolidated view → You choose → Agent navigates and starts work

**Example conversation:**

**Agent**: "Found work across 3 projects:

**IN PROGRESS:**
[1] Home Assistant: Update kitchen motion lights (Claude Code)
[2] Data Scripts: Refactor data pipeline (Codex)

**HIGH PRIORITY BACKLOG:**
[3] Home Assistant: Fix Tuya light naming (Claude Code, 30 min)
[4] Home Assistant: Clean Music Assistant entities (Codex, 15 min)
[5] Personal Website: Update portfolio (Codex, 45 min)

**OTHER:**
[6] Show full backlog for a project
[7] Start something new

**Pick 1-7 or describe what you want:**"

**You**: "3"

**Agent**: "✅ Starting: Fix Tuya light naming

This will:
- SSH to HA server
- Edit entity registry
- Update references in light_groups.yaml and automations
- Test naming consistency

Routing to Claude Code. Estimated: 30 minutes.

Proceeding now..."

[Agent navigates to ~/ha-config, updates TASKS.md, starts work]

---

## Enhanced Version (with AI-suggested priorities)

```
Read LOCAL_CONTEXT.md and TASKS.md.

Run session starter:

1. **Context check**: Show repo, in-progress tasks, backlog
2. **Smart suggestions**: Based on:
   - Incomplete dependencies (task A blocks task B)
   - Quick wins (high value, low effort)
   - Urgent items (marked with priority)
   Suggest: "I recommend tackling X because..."
3. **Let me decide**: Present options with your reasoning
4. **Capture & route**: Add to TASKS.md with right agent assignment
5. **Execute**: Start work immediately

Be opinionated but defer to my choices.
```

---

## Quick Start Commands

**For fast sessions, just tell agent:**

- **"Session start"** → Get numbered menu of all options, respond with number
- **"Continue where we left off"** → Shows in-progress tasks only, pick by number
- **"What's high priority?"** → Shows high-priority backlog with numbers
- **"Show backlog for [project]"** → Full numbered list for one project
- Or just pick: **"1"**, **"3"**, **"7"** if you remember the menu

---

## Tips

**First time in a session:**
- Always start with full session starter (see context)

**Mid-session:**
- "Show backlog" → Quick check without full restart
- "Switch tasks: [new task]" → Mark current in-progress, start new one

**End of session:**
- "Mark complete: [task name]" → Agent updates TASKS.md
- "Session end" → Agent summarizes what was done, what's next

---

## Save This Prompt

Bookmark this file or copy the prompt to:
- VS Code snippets
- Text expander
- Alfred workflow
- Or just keep this file open in a tab

**Goal:** Every session starts with clarity, not confusion.
