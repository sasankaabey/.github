# Multi-Agent System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                  HOME ASSISTANT CONFIG PROJECT                      │
│                      /Users/ankit/ha-config                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    GIT REPOSITORY (Local)                           │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Commits → TASKS.md → Agents → Commits → TASKS.md (cycle)     │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
       ↓ sync_to_ha.sh ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  HOME ASSISTANT SERVER                              │
│                  192.168.4.141 (minipc)                             │
│                       /config                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Automations • Light Groups • Scripts • Templates • Customs     │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Agent Distribution Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ TASK RECEIVED                                                    │
│ (e.g., "Create motion-triggered lighting automation")           │
└──────────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│ DECISION: Route to Agent                                         │
│ Use AGENTS.md decision tree to select best agent                │
└──────────────────────────────────────────────────────────────────┘
                            ↓
          ┌─────────────────┴─────────────────┐
          ↓                                   ↓
    ┌──────────────┐              ┌──────────────────┐
    │ BRAINSTORM   │              │ YAML DRAFT       │
    │              │              │                  │
    │ ChatGPT      │              │ Codex            │
    │ (5-15 min)   │              │ (10-30 min)      │
    └──────────────┘              └──────────────────┘
                            ↓
    ┌──────────────────────────────────────┐
    │ GIT COMMIT                           │
    │ "Task: X - [Checkpoint/Complete]"   │
    │ UPDATE TASKS.md                      │
    └──────────────────────────────────────┘
                            ↓
          ┌─────────────────┴──────────────────────────┐
          ↓                                            ↓
    ┌─────────────────┐                    ┌──────────────────┐
    │ DEPLOY/TEST     │                    │ RESEARCH         │
    │                 │                    │                  │
    │ Claude Code     │                    │ Perplexity       │
    │ (15-45 min)     │                    │ (10-20 min)      │
    └─────────────────┘                    └──────────────────┘
                            ↓
    ┌──────────────────────────────────────┐
    │ FINAL GIT COMMIT                     │
    │ "Task: X - Complete"                 │
    │ UPDATE TASKS.md: COMPLETE            │
    └──────────────────────────────────────┘
                            ↓
    ┌──────────────────────────────────────┐
    │ TASK COMPLETE ✅                     │
    │ Ready for next task                  │
    └──────────────────────────────────────┘
```

---

## Document Reference Map

```
AGENT STARTING NEW TASK
        ↓
    READ IN ORDER:
        ↓
    ┌─────────────────────┐
    │   CONTEXT.md        │  ← 2 min quick ref
    │                     │    (Entity naming, conventions,
    │ ALL AGENTS          │     critical procedures)
    └─────────────────────┘
        ↓
    ┌─────────────────────┐
    │   AGENTS.md         │  ← 5 min your role
    │                     │    (Task routing decision tree,
    │ ALL AGENTS          │     specializations, examples)
    └─────────────────────┘
        ↓
    ┌─────────────────────┐
    │   TASKS.md          │  ← 2 min your assignment
    │                     │    (Current queue, status,
    │ ALL AGENTS          │     acceptance criteria)
    └─────────────────────┘
        ↓
    ROLE-SPECIFIC DOCS:
        ↓
    ┌──────────────────────────────────────────────┐
    │                                              │
    ├──────────────┬────────────┬─────────────────┤
    │              │            │                 │
    ↓              ↓            ↓                 ↓
┌──────────┐  ┌────────┐  ┌──────────┐  ┌──────────────┐
│ Codex    │  │Claude  │  │ Perpl.   │  │ Gemini/Other │
│          │  │ Code   │  │          │  │              │
│HOME_A... │  │.github/│  │DECISIONS │  │[Document]    │
│DECISIONS │  │copilot │  │ markdown │  │ to analyze   │
└──────────┘  └────────┘  └──────────┘  └──────────────┘
   Draft        Ops       Research       Analysis
   Docs      Deployment    Deep Dive
   YAML                    Citations
```

---

## Commit Message Flow

```
┌─────────────────────────────────────────────────────────┐
│ PLANNING (You)                                          │
│ git commit -m "Plan: Task - Added to queue"            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT 1 STARTS                                          │
│ git commit -m "Task: Name - Starting (Agent: Codex)"   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT 1 WORKS (30-90 min)                              │
│ Multiple commits for checkpoints:                      │
│ - git commit -m "Task: Name - Drafted automation"      │
│ - git commit -m "Task: Name - Updated light groups"    │
│ - git commit -m "Task: Name - Ready for Claude Code"   │
│                                                         │
│ After each commit: Update TASKS.md progress            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT 1 COMPLETE                                        │
│ git commit -m "Task: Name - Ready for deployment       │
│                                                         │
│ Codex created:                                         │
│ - automations/lighting/example.yaml                    │
│ - Updated CHANGELOG.md                                │
│                                                         │
│ Next: Claude Code to validate and deploy"              │
│                                                         │
│ Update TASKS.md:                                       │
│ Status: Ready for Claude Code                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT 2 STARTS                                          │
│ git pull origin main                                   │
│ git commit -m "Task: Name - Starting (Agent: Claude)"  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT 2 DEPLOYS                                         │
│ Validate YAML, run sync_to_ha.sh, test                │
│ git commit -m "Task: Name - Deployed and tested        │
│                                                         │
│ Synced to 192.168.4.141:                               │
│ - automations/lighting/example.yaml                    │
│ - Verified in HA UI and logs                          │
│ - Status: LIVE"                                        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ TASK COMPLETE                                           │
│ Update TASKS.md: Status: Complete ✅                    │
│ Ready for next task                                    │
└─────────────────────────────────────────────────────────┘
```

---

## File Structure with Purposes

```
/Users/ankit/ha-config/
│
├── .vscode/                          ← VS Code configuration
│   ├── settings.json                 ← Editor formatting rules
│   ├── extensions.json               ← Recommended extensions
│   ├── launch.json                   ← SSH remote connection
│   └── tasks.json                    ← Quick launch tasks
│
├── .editorconfig                     ← Consistent formatting
│
├── .github/
│   ├── copilot-instructions.md       ← SSH ops + deployment (Claude Code)
│   └── pull_request_template.md      ← PR template for code review
│
├── CONTEXT.md                        ← 2-min quick ref (ALL AGENTS START)
├── AGENTS.md                         ← Agent roles + decision tree
├── MULTI_AGENT_WORKFLOW.md           ← Detailed workflow + examples
├── WORKSPACE_SETUP.md                ← VS Code features + troubleshooting
├── HANDOFF_TEMPLATE.md               ← Template for agent handoffs
├── MULTI_AGENT_SETUP_SUMMARY.md      ← This setup overview
├── SETUP_COMPLETE.md                 ← What was created + next steps
│
├── TASKS.md                          ← Current task queue (SOURCE OF TRUTH)
├── DECISIONS.md                      ← Architecture decisions (Perplexity ref)
├── CHANGELOG.md                      ← Recent changes + features
├── HOME_ASSISTANT.md                 ← HA conventions (Codex ref)
│
├── automations/                      ← YAML automations
│   ├── automation_*.yaml
│   └── lighting/
│       └── *.yaml
│
├── scripts.yaml                      ← HA scripts
├── scenes.yaml                       ← HA scenes
├── template.yaml                     ← HA templates
├── light_groups.yaml                 ← Custom light groups
│
└── [other HA config files...]
```

---

## Cost Optimization Strategy

```
COST PER TASK (Relative Scale)

┌─────────────────────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓ Claude Code (High)   10x       │  Use for: SSH, deploy, debug
│  ▓▓▓▓▓ Perplexity (Medium)      5x        │  Use for: Research
│  ▓▓▓ Codex (Low)                2x        │  Use for: Draft YAML, docs
│  ▓ Haiku (Very Low)             1x        │  Use for: Syntax checks
└─────────────────────────────────────────────┘

OPTIMIZATION:
1. Use Codex for drafting (cheap)
2. Use Haiku for validation (very cheap)
3. Use Claude Code only for critical operations (expensive)
4. Use Perplexity for deep research (research value > cost)
5. Batch operations (multiple YAML changes in one Codex session)
```

---

## Parallel Work Example

```
TWO AGENTS WORKING IN PARALLEL:

Day 1:
┌─────────────────────────┐    ┌──────────────────────┐
│ Agent 1 (Codex)         │    │ Agent 2 (Claude)     │
│ Drafting Automation     │    │ Fixing Bug           │
│ automations/lighting/.. │    │ custom_components/.. │
│ (different files)       │    │ (different files)    │
└─────────────────────────┘    └──────────────────────┘
         ↓                               ↓
  git commit A                    git commit B
         ↓                               ↓
┌─────────────────────────────────────────────┐
│ Agent 1 Pushes: git push origin feature-1   │
│ Agent 2 Pushes: git push origin bugfix-2    │
│                                             │
│ NO CONFLICTS (different files)              │
└─────────────────────────────────────────────┘
         ↓
    Both agents complete
    Merge both features
```

---

## Quick Reference Dashboard

```
┌──────────────────────────────────────────────────────────┐
│  MULTI-AGENT QUICK REFERENCE                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ START: Read CONTEXT.md (2 min)                          │
│        ↓                                                 │
│ ROUTE: Use AGENTS.md decision tree                      │
│        ↓                                                 │
│ READ: TASKS.md (check assignment)                       │
│        ↓                                                 │
│ WORK: Follow MULTI_AGENT_WORKFLOW.md                    │
│        ↓                                                 │
│ COMMIT: Clear message + update TASKS.md                 │
│        ↓                                                 │
│ HANDOFF: Use HANDOFF_TEMPLATE.md if needed              │
│        ↓                                                 │
│ NEXT AGENT: Pull, read context, start work              │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ KEY COMMANDS:                                            │
│                                                          │
│ git pull origin main      - Get latest code             │
│ git commit -m "..."       - Commit with context         │
│ git log --oneline -10     - See recent work             │
│ ssh root@192.168.4.141... - Connect to HA server        │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ KEYBOARD SHORTCUTS (VS Code):                           │
│                                                          │
│ Cmd+Shift+P  - Command palette (tasks, etc.)           │
│ Cmd+P        - Quick file search                       │
│ Cmd+Shift+F  - Find in files                           │
│ Cmd+Shift+G  - Git source control                      │
│ Ctrl+`       - Open terminal                            │
│ Shift+Opt+F  - Format document                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Getting Help

```
PROBLEM AREA          WHERE TO LOOK
─────────────────────────────────────────────────────────
"How do I...?"        → CONTEXT.md (quick ref section)
"Who handles X?"      → AGENTS.md (decision tree)
"What's the process?" → MULTI_AGENT_WORKFLOW.md
"VS Code isn't..."    → WORKSPACE_SETUP.md (features + troubleshooting)
"How do I deploy?"    → .github/copilot-instructions.md
"Why was X chosen?"   → DECISIONS.md
"What changed?"       → CHANGELOG.md
"What's my task?"     → TASKS.md
```

---

**This system is designed for maximum efficiency and minimal context loss. Each agent knows exactly what to do and where to find answers.**
