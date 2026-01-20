# Session Closeout Protocol

Every agent should end their work session by updating TASKS.md with progress notes. This ensures continuity across agent handoffs.

---

## When to Update Progress

**During work:**
- Mark task as "In Progress" when you start
- Add notes to task if you discover blockers or questions

**When done (or pausing):**
- Mark task as "Completed" if fully done
- Mark as "Blocked" if stuck (explain why)
- Mark as "In Progress" with notes if partially done

---

## How to Document Progress

### Format in TASKS.md

```markdown
### Fix Tuya Light Naming
**Status:** In Progress
**Agent:** Claude Code
**Started:** 2026-01-20
**Description:** Standardize all Tuya lights to location_description pattern

**Progress Notes:**
- ✅ Completed: SSH'd to server, backed up entity registry
- ✅ Completed: Renamed 12 lights in entity registry
- 🔄 In Progress: Updating light_groups.yaml references
- ⏸️ Next: Update automation files, test on server

**Blockers:** None

**Acceptance Criteria:**
- [x] Backup entity registry
- [x] Rename lights in registry (stop/start procedure)
- [ ] Update light_groups.yaml
- [ ] Update automation files
- [ ] Test all lights respond correctly
- [ ] Commit changes
```

### If Task is Complete

```markdown
### Fix Tuya Light Naming
**Status:** Completed
**Agent:** Claude Code
**Completed:** 2026-01-20 3:45pm
**Description:** Standardize all Tuya lights to location_description pattern

**What Was Done:**
- Renamed 12 Tuya lights using location_description pattern
- Updated references in light_groups.yaml
- Updated references in 3 automation files
- Tested all lights via HA UI - all responding correctly
- Committed changes: "Entity: Standardize Tuya light naming"

**Files Changed:**
- .storage/core.entity_registry (via SSH)
- light_groups.yaml
- automations/lighting/sensor_lights_living_room.yaml

**Deployment:** Changes synced to HA server, core restarted

**Notes for Future:** Entity renames require stop/start (not restart). Documented in LOCAL_CONTEXT.md.
```

### If Task is Blocked

```markdown
### Fix Tuya Light Naming
**Status:** Blocked
**Agent:** Claude Code
**Last Updated:** 2026-01-20
**Description:** Standardize all Tuya lights to location_description pattern

**Progress:**
- ✅ Backed up entity registry
- ✅ Renamed 12 lights
- ⚠️ BLOCKED: Cannot SSH to HA server (connection timeout)

**Blocker Details:**
- SSH connection to 192.168.4.141 timing out
- May be temporary network issue
- Need user to verify: `ssh root@192.168.4.141`

**Next Steps (when unblocked):**
1. Verify SSH access
2. Complete light_groups.yaml updates
3. Test and deploy

**Estimated time remaining:** 15 minutes once SSH works
```

---

## Git Commits as Progress Log

Your git commit history IS your progress log. Each commit should document what was done:

**Good commit messages:**
```
Entity: Rename 12 Tuya lights to location_description pattern

Changes:
- living_room_floor_lamp_1/2 → living_room_lamp_left/right
- bedroom_light_1/2/3 → bedroom_ceiling/nightstand_left/nightstand_right
- Updated light_groups.yaml with new IDs
- Updated 3 automation files

Tested: All lights responding in HA UI
Deployed: Synced to server, core restarted
```

**Then next agent can:**
```bash
git log --oneline -5  # See what was done
git show HEAD        # See exact changes
```

---

## Session End Checklist

Before closing your agent session:

- [ ] Update TASKS.md with current status
- [ ] Mark task as Completed/In Progress/Blocked
- [ ] Add progress notes (what's done, what's left)
- [ ] Commit your changes with detailed message
- [ ] Push to GitHub
- [ ] If blocked, clearly state blocker and next steps

---

## Example: Next Agent Picking Up

**New agent starts:**
> "Session start"

**Agent reads TASKS.md:**
```
[1] Home Assistant: Fix Tuya light naming
    Status: In Progress (50% done)
    Last agent: Claude Code
    Notes: Renamed lights, need to update automations
    Next: Update automation files, test, deploy
```

**Agent knows exactly:**
- What's done (lights renamed)
- What's left (automations)
- How to continue (test and deploy)
- No wasted time redoing work

---

## Template: Progress Note Format

```markdown
**Progress Notes:**
- ✅ Done: [specific thing]
- ✅ Done: [specific thing]
- 🔄 Current: [what you're working on now]
- ⏸️ Next: [what needs to happen next]

**Files Changed:**
- file1.yaml
- file2.py

**Blockers:** [None / Description of blocker]

**Time Remaining:** [estimate]
```

---

## Why This Matters

**Without progress notes:**
- Next agent rereads entire codebase
- May redo work already done
- Wastes time and money
- Risks breaking working code

**With progress notes:**
- Next agent continues exactly where you left off
- No duplicate effort
- Clear handoff
- Maintains momentum

---

## Quick Commands for Agents

**At task start:**
> "Mark task [name] as In Progress in TASKS.md"

**During work (hit blocker):**
> "Update TASKS.md: Blocked on [reason], next steps are [steps]"

**At task end:**
> "Mark task [name] as Completed in TASKS.md with summary of what was done"

**Before closing session:**
> "Session closeout: Update TASKS.md with current progress, commit, and push"

---

## Integration with Session Start

When you say "Session start", the agent will:
1. Read TASKS.md
2. See progress notes
3. Present options including:
   - "[1] Continue: Fix Tuya naming (50% done - update automations)"
4. If you pick it, agent picks up exactly where last agent left off

**This is how context survives across agent sessions!**
