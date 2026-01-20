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
3. **Present options**: Show me a summary like:
   
   "You have 3 active projects:
   
   **Home Assistant** (ha-config)
   - In progress: Update kitchen motion lights (Claude Code)
   - Last completed: Migrated to org-level coordination
   - Backlog: 8 items (3 high priority)
   
   **Project 2** (repo-name)
   - In progress: None
   - Last completed: [task]
   - Backlog: X items
   
   **Project 3**
   - ...
   
   What would you like to work on?"

4. **Let me choose**: 
   - Continue in-progress work?
   - Pick something from backlog?
   - Start something new on any project?
   
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

**Agent**: "I found 3 projects with active work:

**Home Assistant** (~/ha-config)
- In progress: Update kitchen motion lights (Claude Code)
- Last done: Migrated to org coordination
- Backlog: 8 items including Tuya light naming (high priority)

**Personal Website** (~/my-site)  
- In progress: None
- Last done: Fixed mobile nav
- Backlog: 2 items

**Data Analysis** (~/analysis-scripts)
- In progress: Refactor data pipeline
- Last done: Added logging
- Backlog: 5 items

Where would you like to continue? Or start something new?"

**You**: "Let's tackle the Tuya light naming"

**Agent**: "Got it. Tell me more - do you want to:
1. Rename them in the entity registry?
2. Update references in automations/groups?
3. Both?

What's the end goal?"

**You**: "Both. I want consistent naming: location_description pattern"

**Agent**: "Perfect. I'll route this to Claude Code (needs SSH + entity registry). Adding to TASKS.md... Starting work now."

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

- **"Session start"** → Agent scans all projects, shows consolidated view
- **"Continue where we left off"** → Shows in-progress tasks across all projects, asks which to continue
- **"Show all my projects"** → Lists all repos with TASKS.md
- **"What's high priority?"** → Shows high-priority backlog items across all projects
- **"Quick check on [project name]"** → Deep dive into one project
- **"New task: [description]"** → Agent asks which project, adds to TASKS.md

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
