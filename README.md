# Organization-Wide Multi-Agent Coordination

This repository contains the centralized coordination system for all projects under the `sasankaabey` organization.

---

## 📚 **What's Here**

### Core Documentation (Read First)

- **[AGENTS.md](AGENTS.md)** — Which agent handles which type of work + decision tree
- **[MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)** — Step-by-step process for executing tasks
- **[MULTI_AGENT_ARCHITECTURE.md](MULTI_AGENT_ARCHITECTURE.md)** — System design and visual diagrams
- **[HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md)** — Template for agent-to-agent handoffs

### Evolution & Learning

- **[EVOLUTION_LOG.md](EVOLUTION_LOG.md)** — What we learned, what improved, when and why

### Templates & Patterns

- **[PATTERNS/](PATTERNS/)** — Reusable templates for new repos, automation patterns, checklists

---

## 🎯 **How This Works**

### For Project-Specific Work

Each repo has its own:
- `LOCAL_CONTEXT.md` — What this project is about
- `TASKS.md` — Current task queue for this project
- `CHANGELOG.md` — What changed in this project
- `DECISIONS.md` — Project-specific architecture decisions

### For Workflow & Process

All repos reference these organization-level docs:
- Agent roles → [AGENTS.md](AGENTS.md)
- Workflow process → [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)
- System design → [MULTI_AGENT_ARCHITECTURE.md](MULTI_AGENT_ARCHITECTURE.md)
- Improvements → [EVOLUTION_LOG.md](EVOLUTION_LOG.md)

---

## 🚀 **Quick Start for Agents**

### Starting Work on Any Repo

1. **Clone the repo** you're assigned to
2. **Read `LOCAL_CONTEXT.md`** (2 min) — Understand the project
3. **Check `TASKS.md`** (2 min) — See your assignment
4. **Reference [AGENTS.md](AGENTS.md)** — Confirm your role
5. **Follow [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)** — Execute the task
6. **Update repo's `TASKS.md`** — Mark progress
7. **If you improved something** — Document in [EVOLUTION_LOG.md](EVOLUTION_LOG.md)

### Creating a New Repo

1. **Copy template** from [PATTERNS/NEW_REPO_TEMPLATE/](PATTERNS/NEW_REPO_TEMPLATE/)
2. **Customize `LOCAL_CONTEXT.md`** for your project
3. **Start adding tasks** to `TASKS.md`
4. **Link to org/.github** in your repo's README
5. **Agents automatically use these workflows**

---

## 📊 **What Lives Where**

```
Organization .github (THIS REPO)
├── AGENTS.md                      ← Central: Agent roles
├── MULTI_AGENT_WORKFLOW.md        ← Central: Process
├── MULTI_AGENT_ARCHITECTURE.md    ← Central: Design
├── EVOLUTION_LOG.md               ← Central: Improvements
├── HANDOFF_TEMPLATE.md            ← Central: Handoff process
└── PATTERNS/
    ├── NEW_REPO_TEMPLATE/         ← Template for new repos
    ├── automation_pattern.yaml    ← Reusable automation
    └── deployment_checklist.md    ← Reusable checklist

Each Project Repo
├── LOCAL_CONTEXT.md               ← Local: What is this project?
├── TASKS.md                       ← Local: What to work on?
├── CHANGELOG.md                   ← Local: What changed?
├── DECISIONS.md                   ← Local: Project decisions
├── .vscode/                       ← Local: Editor config
└── README.md                      ← Link to org/.github
```

---

## 💡 **Key Principles**

### Centralize Process, Localize Context

- **Process (how things get done)** → Centralized in org/.github
- **Context (what this project is)** → Local in each repo

### Update Once, Apply Everywhere

- Improve [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md) → All repos benefit
- Discover better pattern → Document in [EVOLUTION_LOG.md](EVOLUTION_LOG.md) → Next agent uses it
- No manual sync across repos

### Transparent Learning

- Agents document improvements in [EVOLUTION_LOG.md](EVOLUTION_LOG.md)
- System gets better over time
- Knowledge accumulates, doesn't disappear

### Minimal Maintenance

- You maintain ONE place (this repo)
- Agents work in N repos
- Zero ongoing maintenance per repo

---

## 🎓 **Agent Roles Quick Reference**

| Agent | Best For | Cost | Time |
|-------|----------|------|------|
| **Codex** | YAML drafting, documentation | 2x | 10-30 min |
| **Claude Code** | SSH, deployment, debugging | 10x | 15-45 min |
| **ChatGPT** | Brainstorming, planning | 1x | 5-15 min |
| **Perplexity** | Research, citations | 5x | 10-20 min |
| **Gemini** | Large doc analysis | 3x | 10 min |
| **Haiku** | Quick syntax checks | 1x | 1-2 min |

**Full details:** [AGENTS.md](AGENTS.md)

---

## 📈 **Evolution Tracking**

When you discover something that works better:

1. **Document it** in [EVOLUTION_LOG.md](EVOLUTION_LOG.md)
2. **Update process docs** if needed (AGENTS.md, WORKFLOW.md)
3. **Next agent benefits immediately** (they reference these docs)

Example improvements to track:
- Better commit message format
- New deployment pattern
- Faster debugging technique
- Agent coordination improvement
- Cost optimization strategy

---

## 🔗 **Links**

- **Organization:** https://github.com/sasankaabey
- **This Repo:** https://github.com/sasankaabey/.github
- **All Repos:** https://github.com/orgs/sasankaabey/repositories

---

## 📞 **Questions?**

**"How do I start work on a repo?"**
→ Read that repo's `LOCAL_CONTEXT.md`, then follow [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)

**"How do I know which agent should do what?"**
→ Use the decision tree in [AGENTS.md](AGENTS.md)

**"Where do I track improvements?"**
→ [EVOLUTION_LOG.md](EVOLUTION_LOG.md)

**"How do I create a new repo?"**
→ Copy template from [PATTERNS/NEW_REPO_TEMPLATE/](PATTERNS/NEW_REPO_TEMPLATE/)

---

**All repos benefit from improvements made to these docs. Update once, apply everywhere.** 🚀
