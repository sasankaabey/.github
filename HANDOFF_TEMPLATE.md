# Agent Handoff Template

Use this template when handing off a task from one agent to another. Copy, fill in, and commit as part of the handoff.

---

## Task Handoff: [Task Name]

**Date:** YYYY-MM-DD  
**From Agent:** [Agent finishing work]  
**To Agent:** [Agent starting work]  

---

## What Was Completed

### Files Created/Modified

- [ ] File 1 (path/to/file.yaml)
- [ ] File 2 (path/to/file.py)
- [ ] File 3 (CHANGELOG.md update)

### Work Summary

Brief description of what was accomplished:
- Drafted automation for X
- Updated light groups with Y
- Tested on staging environment

### Git Commits

Link to recent commits:
```
commit abc123 - Task: Example - Drafted automation
commit def456 - Task: Example - Ready for validation
```

View with: `git log --oneline -5`

---

## What Needs to Happen Next

### Action Items for Next Agent

1. **[Action]** — Details
   - Sub-task A
   - Sub-task B
2. **[Action]** — Details

### Success Criteria

How will we know this task is complete?

- [ ] YAML validates without errors
- [ ] Synced to 192.168.4.141
- [ ] HA restarted successfully
- [ ] Automation triggered correctly in logs
- [ ] Tested via voice command

### Testing Notes

Any test results from previous agent:

```
Tested locally:
- YAML validation: PASSED
- Syntax check: PASSED
- Light group entity IDs verified: PASSED

What still needs testing:
- Live server validation
- End-to-end automation trigger
- Voice command test
```

---

## Context for Next Agent

### Key Files to Review

1. **[CONTEXT.md](../CONTEXT.md)** — 2-minute quick ref
2. **[TASKS.md](../TASKS.md)** — Your specific assignment
3. **Role-specific docs:**
   - If Codex: [HOME_ASSISTANT.md](../HOME_ASSISTANT.md)
   - If Claude Code: [.github/copilot-instructions.md](../.github/copilot-instructions.md)
4. **Recent git commits:** `git log --oneline -10`

### Important Notes

Things the next agent should know:

- Entity IDs in light_groups.yaml MUST match registry exactly
- Tuya devices are auto-discovered from cloud config
- Notify groups require mobile app service names (slugified)
- [Include other gotchas or warnings]

### Dependencies

Does this task depend on other work?

- [ ] Blocked by [other task]
- [ ] Requires [permission/access/resource]
- [ ] Waiting on [external factor]

**If blocked:** Explain what's needed before proceeding.

---

## Questions for Next Agent?

Any uncertainties or design decisions needing input:

- Should we use automation or script for X?
- Need guidance on entity naming?
- Questions about light group configuration?

---

## Deployment Checklist (For Claude Code)

If this is being handed to Claude Code for deployment:

- [ ] Validate YAML: `python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"`
- [ ] Run `./sync_to_ha.sh` to copy to server
- [ ] Restart HA via `ha core restart`
- [ ] Check logs for errors: `ha logs follow`
- [ ] Test functionality on server
- [ ] Update [TASKS.md](../TASKS.md) with results
- [ ] Make final commit: `git commit -m "Task: [Name] - Deployed and tested"`

---

## Quick Reference

**Git commands for quick context:**
```bash
git show HEAD              # See last commit
git log --oneline -10     # Recent commits
git diff HEAD~1           # What changed since last commit
git status                # Current state
```

**Server connection:**
```bash
ssh root@192.168.4.141 'ha core status'  # Check HA
ssh root@192.168.4.141 'ha logs follow'  # Live logs
```

---

**Next Agent:** Start by reading [CONTEXT.md](../CONTEXT.md) (takes 2 minutes), then check [TASKS.md](../TASKS.md) for your assignment.
