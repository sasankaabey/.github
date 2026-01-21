# ChatGPT Agent Mode Context

This file gives ChatGPT all the context needed to work across your repos using the multi-agent workflow and keep everything in sync, documented, and accessible from anywhere.

---

## What this setup does
- Consolidates all repos under a single local root: `~/Developer/sasankaabey/`
- Keeps local repos in sync with GitHub using an automated sync script:
  - Script: `/workspaces/.github/scripts/sync_repos.sh` (also exists in the `.github` repo when cloned locally)
  - Behavior: clones new repos, updates existing ones, and regenerates the VS Code multi-root workspace
- Provides a multi-root workspace file:
  - Path (devcontainer): `/workspaces/sasankaabey.code-workspace`
  - Path (Mac local): `~/Developer/sasankaabey/sasankaabey.code-workspace`
- Auto-runs sync on devcontainer start via `postStartCommand`:
  - Config: `.devcontainer/devcontainer.json` in the `.github` repo

---

## Current repository state (Jan 20, 2026)
- GitHub user: `sasankaabey`
- Repos present and consolidated under `~/Developer/sasankaabey/`:
  - `.github` — Organization-level docs, templates, and automation
  - `home-assistant-config` — Home Assistant configuration
  - `kitlabworks` — Private repo (cloned via GitHub CLI)
  - `headache-tracker` — Default branch set to `main`
- Cleanups performed:
  - Removed stray duplicates and empty folders outside `~/Developer/sasankaabey/`
  - Deleted old `imessage-exporter` local clone
- Workspace file regenerated and valid

---

## How ChatGPT should start a working session
1. Ensure repos are up to date and workspace includes all repos:
  - On devcontainer: the sync runs automatically on start
  - Anywhere: run the sync script
    - Devcontainer: `/workspaces/.github/scripts/sync_repos.sh`
    - Mac local: `~/Developer/sasankaabey/.github/scripts/sync_repos.sh`
2. Open the workspace:
  - Devcontainer: `/workspaces/sasankaabey.code-workspace`
  - Mac local: `~/Developer/sasankaabey/sasankaabey.code-workspace`
3. Use the session starter prompt to list tasks across repos:
  - Search for `TASKS.md` and `LOCAL_CONTEXT.md` across the workspace
  - Present options and proceed per `AGENTS.md` roles

---

## File Architecture: Org vs Project Level

### Org-Level (`sasankaabey/.github`) — "How work gets done"
Universal workflow, agent roles, handoff protocols, evolution tracking.

**Files:**
- `AGENTS.md` — Agent roles and task routing
- `MULTI_AGENT_WORKFLOW.md` — Step-by-step execution process
- `MULTI_AGENT_ARCHITECTURE.md` — System design and diagrams
- `EVOLUTION_LOG.md` — Learnings and improvements across all projects
- `HANDOFF_TEMPLATE.md` — Agent-to-agent handoff format
- `CONTEXT.md` — This file (quick reference for agents)
- `copilot-instructions.md` — Copilot-specific workflow instructions

### Project-Level (each repo) — "What work needs to be done"
Project-specific context, tasks, and escalation path to org-level.

**Files:**
- `LOCAL_CONTEXT.md` — What this project is, tech stack, architecture
- `TASKS.md` — Current backlog, in-progress, completed work
- `.github/copilot-instructions.md` — Minimal: reference org + project-specific context

**Learning Escalation:**
When a project-level agent discovers a pattern, pitfall, or improvement that would help other projects:
1. Document it locally in `TASKS.md` or commit message
2. Escalate to org-level by updating `sasankaabey/.github/EVOLUTION_LOG.md`

---

## Agent routing (quick ref)
- Use `AGENTS.md` in this repo to select the right agent per task
- Follow `MULTI_AGENT_WORKFLOW.md` for execution
- Use `HANDOFF_TEMPLATE.md` when handing off between agents

---

## Commands (copy/paste when needed)
- Sync everything and regenerate the workspace:
  - Devcontainer:
    - `/workspaces/.github/scripts/sync_repos.sh`
  - Mac local:
    - `cd ~/Developer/sasankaabey/.github && git pull origin main`
    - `~/Developer/sasankaabey/.github/scripts/sync_repos.sh`
- Open the workspace (Mac):
  - `code ~/Developer/sasankaabey/sasankaabey.code-workspace`

---

## Notes on branches and permissions
- The sync script respects each repo’s default branch. If a repo doesn’t have `origin/main`, it will pull the configured default branch or skip with a warning.
- Private repos are cloned via GitHub CLI (`gh repo clone`). Ensure `gh auth status` shows you are logged in with repo access.

---

## Remaining cleanups (optional)
- Home folder tidy-up: archive loose Python scripts and non-critical dotfolders to `~/Archive/<date>_home_cleanup/` after inventory
- If you add new repos to `sasankaabey`, re-run the sync script to include them automatically

---

## Success criteria for future sessions
- All work happens inside `~/Developer/sasankaabey/`
- `TASKS.md` and `LOCAL_CONTEXT.md` are present in active repos
- Sync script runs clean (no missing branch warnings), and workspace opens with all repos loaded
- Commits are pushed to GitHub with clear messages and agent handoffs documented

---

## Quick troubleshooting
- If a repo warns “No remote branch origin/main”, set its default branch on GitHub or create/push `main` locally
- If cloning private repos fails, re-authenticate `gh` with `repo` scope: `gh auth login`

---

## Links
- Organization: https://github.com/sasankaabey
- This repo: https://github.com/sasankaabey/.github