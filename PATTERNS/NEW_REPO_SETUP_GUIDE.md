# New Repo Setup Guide

Follow these steps to create a new repo in the sasankaabey organization with the multi-agent coordination system pre-configured.

---

## Step 1: Create Repository on GitHub

1. Go to: <https://github.com/orgs/sasankaabey/repositories>
2. Click "New repository"
3. Name your repo
4. Choose public/private
5. Initialize with README
6. Create repository

---

## Step 2: Clone and Add Template Files

```bash
# Clone your new repo
git clone git@github.com:sasankaabey/[repo-name].git
cd [repo-name]

# Copy template files from org/.github
# (Assuming you have org/.github cloned at ~/ level)
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/LOCAL_CONTEXT_TEMPLATE.md ./LOCAL_CONTEXT.md
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/TASKS_TEMPLATE.md ./TASKS.md

# Create .vscode directory
mkdir .vscode

# Copy .vscode config from ha-config (or create new)
# Option 1: Copy from ha-config
cp /Users/ankit/ha-config/.vscode/settings.json .vscode/
cp /Users/ankit/ha-config/.vscode/extensions.json .vscode/
cp /Users/ankit/ha-config/.vscode/tasks.json .vscode/

# Option 2: Create minimal .vscode/README.md
echo "# VS Code Configuration

See organization-level workflows: https://github.com/sasankaabey/.github

Customize .vscode/settings.json for this project's specific needs." > .vscode/README.md
```

---

## Step 3: Customize LOCAL_CONTEXT.md

Edit `LOCAL_CONTEXT.md` with your project specifics:

```bash
code LOCAL_CONTEXT.md
```

**Fill in:**
- What is this project?
- Tech stack
- Key files and folders
- Project-specific conventions
- Development/deployment process
- Common gotchas

**Time:** ~10 minutes

---

## Step 4: Add Initial Tasks

Edit `TASKS.md`:

```bash
code TASKS.md
```

Add your first few tasks using the template format.

---

## Step 5: Update README.md

Add links to org-level docs in your README:

```markdown
# [Project Name]

[Project description]

## Quick Start

See [LOCAL_CONTEXT.md](LOCAL_CONTEXT.md) for project overview and setup.

## Workflow

This project uses the organization-wide multi-agent coordination system:

- **Agent Roles:** [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md)
- **Workflow:** [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)
- **Current Tasks:** [TASKS.md](TASKS.md)

## For Agents

1. Read [LOCAL_CONTEXT.md](LOCAL_CONTEXT.md) (10 min)
2. Check [TASKS.md](TASKS.md) for assignment
3. Follow [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)
```

---

## Step 6: Commit and Push

```bash
git add .
git commit -m "Setup: Initialize multi-agent coordination system

Added:
- LOCAL_CONTEXT.md (project overview)
- TASKS.md (task queue)
- .vscode/ (editor config)
- Links to org/.github workflows

Ready for agents to start work."

git push origin main
```

---

## Step 7: Verify Setup

**Check these files exist:**
- [x] LOCAL_CONTEXT.md
- [x] TASKS.md
- [x] README.md (with links to org/.github)
- [x] .vscode/ (optional but recommended)

**Test workflow:**
1. Agent clones repo
2. Reads LOCAL_CONTEXT.md → understands project
3. Reads TASKS.md → sees assignment
4. Follows link to org/.github/AGENTS.md → knows process
5. Gets to work!

---

## What You Get

### Local to This Repo (Project-Specific)
- ✅ LOCAL_CONTEXT.md — What this project is
- ✅ TASKS.md — What to work on
- ✅ .vscode/ — Editor config
- ✅ README.md — Project overview

### Referenced from org/.github (Shared)
- ✅ AGENTS.md — Agent roles and routing
- ✅ MULTI_AGENT_WORKFLOW.md — Process
- ✅ MULTI_AGENT_ARCHITECTURE.md — Design
- ✅ EVOLUTION_LOG.md — Improvements over time

---

## Maintenance

**Ongoing (per repo):**
- Update TASKS.md as work progresses
- Update LOCAL_CONTEXT.md if project changes
- Add CHANGELOG.md for user-facing changes
- Add DECISIONS.md for architecture decisions

**Ongoing (once for all repos):**
- Update org/.github docs when process improves
- Document improvements in EVOLUTION_LOG.md
- All repos benefit automatically (they link to it)

**Time investment:**
- Setup new repo: ~15 minutes
- Ongoing maintenance: ~0 minutes (links to central docs)

---

## Optional: Add More Files

Depending on your project, you may want:

```bash
# Changelog
touch CHANGELOG.md
echo "# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial project setup" > CHANGELOG.md

# Decisions
touch DECISIONS.md
echo "# Architecture Decisions

Record of significant decisions for this project.

See org/.github/DECISIONS_TEMPLATE.md for format." > DECISIONS.md

# .gitignore
touch .gitignore
echo "# Project-specific ignores
node_modules/
.env
*.pyc
__pycache__/
.DS_Store" > .gitignore
```

---

## Done!

Your repo is now configured for multi-agent coordination. Agents can:

1. Clone and immediately understand the project (LOCAL_CONTEXT.md)
2. See what needs to be done (TASKS.md)
3. Follow consistent workflows (org/.github docs)
4. Contribute improvements (EVOLUTION_LOG.md)

**Next:** Start adding tasks to TASKS.md and assign agents using org/.github/AGENTS.md decision tree!
