# Session Starter Prompt

Use this prompt at the beginning of any coding session with any agent. The agent will guide you through project selection and task planning.

---

## Copy-Paste This Prompt

```
Read my LOCAL_CONTEXT.md if it exists in the current directory, otherwise check for any repos in my workspace.

Then run a session starter:

1. **Show my projects**: List repos you can see, identify which has a TASKS.md
2. **Where we left off**: Read TASKS.md and show:
   - In-progress tasks
   - Recently completed tasks (last 3)
   - Backlog items
3. **Ask me**: 
   - Do I want to continue in-progress work?
   - Pick from backlog?
   - Start something new?
4. **Capture details**: Based on my answer, ask clarifying questions:
   - What specifically needs to be done?
   - What are acceptance criteria?
   - Which agent is best (reference org/.github/AGENTS.md)?
5. **Update TASKS.md**: Add/update tasks based on our conversation
6. **Start work**: Execute the chosen task following org/.github/MULTI_AGENT_WORKFLOW.md

Be conversational and help me think through what to prioritize.
```

---

## How It Works

**You paste this** → Agent reads context → Presents options → You choose → Agent updates TASKS.md → Work begins

**Example conversation:**

**Agent**: "I see 2 repos: ha-config (Home Assistant) and a .github org repo. Your ha-config has these in-progress tasks:
- Update kitchen motion lights
- Document entity registry process

And 3 backlog items:
- Clean up Music Assistant entities
- Fix Tuya light naming
- Add plant watering automation

What would you like to work on today?"

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

- "Session start in ha-config" → Agent runs full session starter
- "Quick check - what's in progress?" → Shows current work only
- "Backlog review" → Shows all backlog items with suggestions
- "New task: [description]" → Agent asks clarifying questions, adds to TASKS.md

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
