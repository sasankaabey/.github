# Multi-Agent Workflow Process

A detailed guide for coordinating work across multiple AI agents in this Home Assistant configuration project.

---

## Overview

This project uses a **multi-agent coordination model** to optimize costs, maintain context focus, and leverage each agent's strengths:

- **Codex** for documentation and YAML drafting (fast, low cost)
- **Claude Code** for server operations and complex debugging (high capability)
- **ChatGPT** for brainstorming and planning (general purpose)
- **Perplexity** for research and citations (specialized)
- **Gemini** for large-scale analysis (summarization)
- **Haiku** for quick checks (minimal cost)

---

## Phase 1: Task Planning (You)

### Create Task Definition

1. **Identify what needs to be done:**
   - New feature? Bugfix? Cleanup? Research?
   - Does it require server access? YAML drafting? Documentation?

2. **Create task entry in [TASKS.md](TASKS.md):**
   ```markdown
   ### [Task Name]
   **Status:** Not Started
   **Agent:** [Who should handle this?]
   **Description:** [1-2 sentence summary]
   **Dependencies:** [Any other tasks that must finish first?]
   **Acceptance Criteria:** [How do we know it's done?]
   ```

3. **Commit the task:**
   ```bash
   git add TASKS.md
   git commit -m "Plan: [Task Name] - Added to task queue"
   ```

4. **Route using [AGENTS.md](AGENTS.md) decision tree** (or ask ChatGPT if unsure)

---

## Phase 2: Agent Work (Agent 1)

### Agent Starts Task

1. **Read required context (in order):**
   - [CONTEXT.md](CONTEXT.md) — 2-minute quick ref
   - [AGENTS.md](AGENTS.md) — Understand your role
   - [TASKS.md](TASKS.md) — Your specific assignment
   - Role-specific docs:
     - **Codex:** [HOME_ASSISTANT.md](HOME_ASSISTANT.md) + [DECISIONS.md](DECISIONS.md)
     - **Claude Code:** [.github/copilot-instructions.md](.github/copilot-instructions.md)
     - **Perplexity:** [DECISIONS.md](DECISIONS.md) for architecture context
     - **Gemini:** The document(s) to analyze

2. **Review recent git history for context:**
   ```bash
   git log --oneline -10
   git show [recent-commit-hash]  # Read context from commit messages
   ```

3. **Make starting commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Starting (Agent: [Your Name])"
   ```

### Agent Works

4. **Do focused work in blocks (30-90 minutes):**
   - Make commits every 30 mins or at logical completion points
   - Commit messages: `"Task: [Name] - [Checkpoint description]"`

5. **Update progress in [TASKS.md](TASKS.md) as you go:**
   ```markdown
   ### Motion-Triggered Lights
   **Status:** In Progress (Codex)
   **Progress:** 
   - [x] Drafted automation_motion_lights.yaml
   - [x] Added to automations/lighting/
   - [ ] Validate and test
   - [ ] Document in CHANGELOG
   ```

6. **Commit updates to TASKS.md:**
   ```bash
   git add TASKS.md
   git commit -m "Task: [Name] - Progress update (50% complete)"
   ```

### Agent Completes Work

7. **When done, update [TASKS.md](TASKS.md):**
   ```markdown
   ### Motion-Triggered Lights
   **Status:** Complete (Codex) → Ready for Deployment
   **Agent:** Codex → Claude Code (next)
   **Deliverables:**
   - automations/lighting/motion_sensor.yaml (new)
   - light_groups.yaml (updated with group)
   - CHANGELOG.md (documented feature)
   **Next Steps:** Claude Code to validate and deploy to 192.168.4.141
   ```

8. **Make final commit summarizing work:**
   ```bash
   git add .
   git commit -m "Task: Motion-Triggered Lights - Complete

   Codex completed YAML drafting:
   - Created automations/lighting/motion_sensor.yaml
   - Updated light_groups.yaml with 'Motion Lights' group
   - Documented in CHANGELOG.md
   
   Ready for: Claude Code deployment + validation
   See TASKS.md for details."
   ```

---

## Phase 3: Agent Handoff (Between Agents)

### Receiving Agent (Next Step)

1. **Pull latest code:**
   ```bash
   git pull origin main
   ```

2. **Read handoff context:**
   - [CONTEXT.md](CONTEXT.md) (all agents)
   - [TASKS.md](TASKS.md) (your assignment)
   - **Recent git commits** (especially the handoff commit)

3. **Review the work:**
   - Read the YAML/code created by previous agent
   - Check for any notes in commit messages

4. **Make starting commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Starting deployment (Agent: Claude Code)"
   ```

5. **Do your work** (same as Phase 2 above)

---

## Phase 4: Deployment (Claude Code)

### Validate & Deploy

1. **Validate YAML before touching server:**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('automations/lighting/motion_sensor.yaml'))"
   ```

2. **Sync to server:**
   ```bash
   ./sync_to_ha.sh
   ```

3. **Restart HA:**
   ```bash
   ssh root@192.168.4.141
   ha core restart
   # Wait for restart
   ha logs follow  # Check for errors
   ```

4. **Test functionality:**
   - Check UI for new entities
   - Test via voice command (Alexa, Siri, Google)
   - Verify logs show automation triggering

5. **Document & commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Deployed and tested successfully

   Changes synced to 192.168.4.141:
   - Motion sensor automation now active
   - Tested with Alexa: 'Alexa, turn on motion lights'
   - Verified in logs: automation triggering correctly
   
   Status: LIVE"
   ```

6. **Update [TASKS.md](TASKS.md):**
   ```markdown
   ### Motion-Triggered Lights
   **Status:** Complete (Deployed)
   **Agent:** Claude Code
   **Deployed:** 2026-01-20
   **Testing:** Verified via Alexa and HA logs
   **Live:** YES
   ```

---

## Example: End-to-End Workflow

### Day 1 — Planning (You)

```bash
# Add task to queue
edit TASKS.md
git commit -m "Plan: Add sunset dimming automation"
```

### Day 1 — Drafting (Codex)

```bash
# Codex reads CONTEXT.md, TASKS.md, HOME_ASSISTANT.md
git commit -m "Task: Sunset dimming - Starting"

# Draft the automation
create automations/lighting/sunset_dimming.yaml

git commit -m "Task: Sunset dimming - Automation drafted"

# Update TASKS.md
edit TASKS.md  # Mark as "Ready for Claude Code"
git commit -m "Task: Sunset dimming - Ready for deployment

Codex created automations/lighting/sunset_dimming.yaml
Next: Claude Code to validate and deploy to 192.168.4.141"
```

### Day 2 — Deployment (Claude Code)

```bash
git pull origin main

# Claude Code reads CONTEXT.md, TASKS.md, copilot-instructions.md
git commit -m "Task: Sunset dimming - Starting deployment"

# Validate
python3 -c "import yaml; yaml.safe_load(open('automations/lighting/sunset_dimming.yaml'))"

# Deploy
./sync_to_ha.sh
ssh root@192.168.4.141 'ha core restart'

# Test
# Verify in HA UI and logs

git commit -m "Task: Sunset dimming - Deployed successfully

Validated and synced automations/lighting/sunset_dimming.yaml
Tested at sunset: Lights dimmed correctly
Status: LIVE"

edit TASKS.md  # Mark as "Complete"
git commit -m "Task: Sunset dimming - Complete"
```

### Day 2 — Documentation (Codex)

```bash
git pull origin main

git commit -m "Task: Sunset dimming docs - Starting"

# Update CHANGELOG.md
edit CHANGELOG.md  # Add feature under "New Automations"

# Update HOME_ASSISTANT.md
edit HOME_ASSISTANT.md  # Add sunset dimming to feature list

git commit -m "Task: Sunset dimming docs - Complete

Updated CHANGELOG.md and HOME_ASSISTANT.md
Feature documented and ready for users"
```

---

## Handoff Checklist (Between Agents)

### Outgoing Agent
- [ ] Task marked as "Complete" or "Ready for [Next Agent]" in TASKS.md
- [ ] All files committed to git
- [ ] Commit message includes clear context for next agent
- [ ] Test results documented (if applicable)
- [ ] Dependencies noted (what other tasks must finish first?)

### Incoming Agent
- [ ] Latest code pulled: `git pull origin main`
- [ ] CONTEXT.md read (2 minutes)
- [ ] AGENTS.md read for role clarification
- [ ] TASKS.md checked for assignment
- [ ] Recent git log reviewed for context
- [ ] Starting commit made with clear intention
- [ ] Role-specific docs skimmed (HOME_ASSISTANT.md, copilot-instructions.md, etc.)

---

## Merge Conflicts (If Multiple Agents Work in Parallel)

### Prevention
- Different agents work on **different features** (not same files)
- Commit frequently (every 30 min)
- Pull before starting: `git pull origin main`
- Push after finishing each feature

### Resolution (If Conflict Occurs)
1. **Pull latest:** `git pull origin main`
2. **Identify conflicts:** VS Code will highlight them
3. **Resolve manually:** Look at both versions, pick correct one
4. **Test thoroughly:** Make sure resolution doesn't break anything
5. **Commit merge:** `git commit -m "Merge: Resolved conflict in [file]"`

---

## Cost Optimization Tips

### Use Cheaper Agents When Possible
- **Haiku** for quick syntax checks (50x cheaper than Claude)
- **Codex** for documentation (included in ChatGPT plan)
- **Claude Code** only for critical/complex server work
- **Perplexity** for research (not general coding)

### Batch Operations
- Multiple YAML changes → One Codex session
- Multiple SSH operations → One Claude Code session
- Multiple small commits → One larger commit with detailed message

### Parallel Work
- While Codex drafts automation, Claude Code can fix bugs in separate file
- Perplexity researches while you review Codex's work
- Different agents on different features (not same files)

---

## Status Labels in TASKS.md

- **Not Started** — Task created, waiting to begin
- **In Progress** — Agent actively working
- **Ready for [Next Agent]** — Current agent done, next agent can start
- **Ready for Deployment** — Code complete, waiting for Claude Code to deploy
- **In Deployment** — Claude Code syncing and testing
- **Complete** — Deployed and verified
- **Blocked** — Waiting on external factor (server downtime, missing info, etc.)
- **Deferred** — Deprioritized but tracked for later

---

## Git Commit Message Format

### Standard Format
```
Task: [Name] - [Action/Status]

[Optional detailed explanation of what was done, why, and what's next]

See TASKS.md for full context.
```

### Examples

**Start a task:**
```
Task: Sunset dimming automation - Starting

Codex will draft automations/lighting/sunset_dimming.yaml
See TASKS.md for acceptance criteria.
```

**Complete a task:**
```
Task: Sunset dimming automation - Ready for deployment

Codex completed:
- automations/lighting/sunset_dimming.yaml (new)
- Updated light_groups.yaml with sunset_lights group
- Validated YAML structure

Next: Claude Code to sync and test on 192.168.4.141
See TASKS.md for details.
```

**Deploy a task:**
```
Task: Sunset dimming automation - Deployed

Claude Code:
- Synced to 192.168.4.141 via sync_to_ha.sh
- Restarted HA and verified logs
- Tested via Alexa: automation triggered correctly
- Status: LIVE

Task complete and verified.
```

---

## FAQ

**Q: What if I'm mid-task and need to hand off?**  
A: Update TASKS.md with current progress, make a commit, and note "Next agent: [Name]" in the task entry.

**Q: Can two agents work on the same file?**  
A: Avoid it. Use git pull/push to coordinate. If unavoidable, merge via git conflict resolution.

**Q: How long should each agent session be?**  
A: 30-90 minutes ideally. Longer = harder to hand off. Shorter = overhead from context reading.

**Q: Should I deploy immediately after drafting?**  
A: No. Hand off to Claude Code for validation and deployment. This provides a safety gate.

**Q: What if deployment breaks something?**  
A: Claude Code can quickly rollback using previous git commit. Always test before pushing to main.

**Q: How do I track which agent did what?**  
A: Git commit messages + TASKS.md. Git blame can show line-by-line history.

**Q: Can we work in parallel?**  
A: Yes, on **different files**. Commit frequently to minimize merge conflicts.

---

## Reference Quick Links

- [TASKS.md](TASKS.md) — Current task queue and assignments
- [AGENTS.md](AGENTS.md) — Which agent handles what + decision tree
- [CONTEXT.md](CONTEXT.md) — 2-minute quick ref for all agents
- [HOME_ASSISTANT.md](HOME_ASSISTANT.md) — HA-specific conventions and setup
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — Deployment and server ops
- [DECISIONS.md](DECISIONS.md) — Architecture decisions and rationale
