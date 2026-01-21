# Log Monitor Agent - Workflow Documentation

The Log Monitor Agent provides **proactive error detection and automated triage** for the Home Assistant project.

---

## Purpose

Continuously monitor HA logs to:

1. **Detect issues early** - Catch errors before they impact users
2. **Auto-triage severity** - Classify issues by impact
3. **Create work items** - Add tasks to backlog with full context
4. **Auto-fix when possible** - Handoff to coding agent for resolution
5. **Track patterns** - Identify recurring issues for root cause analysis

---

## Workflow

### 1. Session Start Trigger

**When:** Every time an HA project session begins (automatic)

**Action:** Fetch and analyze recent logs

```bash
ssh root@192.168.4.141 'ha logs --lines 200'
```

### 2. Log Analysis

**Parse for:**

- Integration setup failures
- Entity registry errors
- Missing/renamed entities
- Configuration validation warnings
- Component load failures
- Deprecated feature usage
- Performance warnings (slow operations)
- Connection timeouts/retries

**Ignore:**

- Known false positives (documented in HOME_ASSISTANT.md § Common Log Errors)
- Debug-level messages
- Informational startup messages

### 3. Severity Classification

| Severity | Impact | Examples | Action |
|----------|--------|----------|--------|
| **Critical** | System non-functional or major feature broken | Core component failed to load, entity registry corruption | Immediate user alert + task creation |
| **High** | Integration offline or automation broken | Cloud integration auth failed, automation trigger error | Task creation, consider auto-fix |
| **Medium** | Feature degraded but functional | Light group missing entity, sensor unavailable | Task creation, low priority |
| **Low** | Cosmetic or minor issue | Deprecated feature warning, slow component | Log only, batch with similar issues |
| **Ignorable** | Known false positive | VS Code schema warnings, expected startup messages | No action |

### 4. Auto-Fix Decision Tree

```
Can the issue be fixed without user input?
│
├─ YES → Is it safe to fix automatically?
│   │
│   ├─ YES → Handoff to Claude Code
│   │        ├─ Fix the issue
│   │        ├─ Test fix
│   │        ├─ Handoff to Codex for documentation
│   │        └─ Handoff to Status Agent for TASKS.md update
│   │
│   └─ NO → Create task with priority, add safety notes
│
└─ NO → Create task with context questions for user
```

**Auto-fixable examples:**

- Entity ID mismatch in light groups (entity renamed, just update reference)
- Deprecated service call (update to new syntax)
- Missing helper entity (create from known pattern)
- Incorrectly formatted YAML (fix indentation/syntax)

**Not auto-fixable examples:**

- Integration authentication failure (needs user credentials)
- Device offline (hardware/network issue)
- Configuration conflict (needs user decision on priority)
- Unknown entity reference (need user to identify correct entity)

### 5. Task Creation

When creating tasks in `TASKS.md`, use this template:

```markdown
### [Issue Description]
**Priority:** [Critical/High/Medium/Low]
**Agent:** [Which agent should handle this]
**Source:** Log Monitor Agent (detected: YYYY-MM-DD HH:MM)
**Log Context:**
```text
[Relevant log excerpt]
```

**Impact:** [How this affects users/system]

**Suggested Fix:** [If known, describe approach]

**Questions for User:** [If user input needed]
- [ ] Question 1
- [ ] Question 2
```

### 6. Agent Handoff Chain

**For auto-fixable issues:**

```
Log Monitor
    ↓
[Creates detailed context doc]
    ↓
Claude Code (Coding Agent)
    ↓
[Implements fix, tests, verifies]
    ↓
Codex (Observer Agent)
    ↓
[Documents in CHANGELOG.md, HOME_ASSISTANT.md if pattern]
    ↓
Codex/ChatGPT (Status Agent)
    ↓
[Updates TASKS.md: "Auto-fixed: [issue]"]
```

**For issues needing user input:**

```
Log Monitor
    ↓
[Creates task in TASKS.md with context]
    ↓
User reviews and provides input
    ↓
Appropriate agent handles based on task type
```

---

## Log Sources & Filters

### Primary Log Sources

**Core logs:**

```bash
ha logs --lines 200
```

**Integration-specific:**

```bash
ha logs --filter integration --lines 100
```

**Custom components:**

```bash
ha logs | grep custom_components
```

**Errors only:**

```bash
ha logs | grep -E "(ERROR|CRITICAL)"
```

### Log Patterns to Track

**Integration Failures:**

```
ERROR .* Setup of .* failed
ERROR .* Unable to connect to .*
ERROR .* Authentication failed for .*
```

**Entity Issues:**

```
WARNING .* Entity .* does not exist
ERROR .* Entity .* not found in registry
WARNING .* is unavailable because.*
```

**Configuration Problems:**

```
ERROR .* Invalid config for .*
WARNING .* Config validation failed.*
ERROR .* Failed to parse .*
```

**Performance Warnings:**

```
WARNING .* Updating .* took longer than .*
WARNING .* Blocking call to .* took .*
```

---

## Session Report Template

At end of log review, provide user with summary:

```markdown
## 🔍 Log Monitor Report

**Session:** YYYY-MM-DD HH:MM
**Logs Analyzed:** Last 200 lines

### Summary
- ✅ No critical issues
- ⚠️  2 medium-priority issues added to backlog
- 🔧 1 issue auto-fixed (light group entity mismatch)
- 📝 3 ignorable warnings logged

### Auto-Fixed Issues
1. **Light group entity reference** - Updated light_groups.yaml with renamed entity
   - Verified group loads correctly after restart
   - Documented in CHANGELOG.md

### New Tasks Added
1. **[Medium] Tuya integration slow response** - Added to Claude Code backlog
   - Check network latency to Tuya cloud
   - Consider local control migration

### Ignorable Warnings Logged
- VS Code YAML schema false positives (3x) - documented pattern
```

---

## Pattern Tracking

**Goal:** Identify recurring issues for root cause analysis

**Track in session notes:**

- Issue type
- Frequency (how many times in last N sessions)
- Components affected
- Potential root cause

**Example:**

```
Pattern Detected: "Tuya integration timeout" (3x in last 5 sessions)
Root Cause Hypothesis: Network instability or cloud API rate limiting
Recommended Action: Research local control via tuya_local integration
Added to backlog: [Research] Migrate Tuya devices to local control
```

---

## Severity Rules Reference

### Critical

- Core component failed to load (`homeassistant.core` errors)
- Entity registry corruption
- Authentication system failure
- Database connection lost
- Supervisor communication failure

### High

- Cloud integration offline (Alexa, Google, HomeKit)
- Automation trigger failure
- Critical device offline (security, climate control)
- Custom component crash with traceback

### Medium

- Light/switch entity unavailable
- Group contains non-existent entity
- Sensor data stale (>1 hour)
- Deprecated feature in use
- Single automation action failed

### Low

- Slow component update (>5s but <30s)
- Informational warnings
- UI-related errors (lovelace)
- Non-critical integration slow

### Ignorable

- VS Code schema warnings (false positives)
- Expected startup messages
- Debug logging from verbose integrations
- Transient network blips (<3 retries)

---

## Configuration

### Excluded Integrations (Don't Alert)

Some integrations have known noisy logging:

- `recorder` - Database warnings during startup (expected)
- `http` - Client disconnection messages (normal)
- `websocket` - Periodic connection resets (expected)

### Auto-Fix Safeguards

Never auto-fix:

- `.storage/core.entity_registry` edits (high risk)
- Integration authentication credentials
- Network/firewall configurations
- Device pairing/discovery actions
- Anything requiring external service interaction

Always confirm with user before:

- Deleting entities
- Modifying automations that reference external services
- Changes affecting voice assistants
- Bulk entity renaming

---

## Implementation Checklist

- [ ] Create log fetching script (SSH wrapper)
- [ ] Define regex patterns for common error types
- [ ] Build severity classification logic
- [ ] Implement auto-fix decision tree
- [ ] Create TASKS.md task templates
- [ ] Build agent handoff templates
- [ ] Add session report generator
- [ ] Implement pattern tracking database
- [ ] Test with historical logs
- [ ] Document in MULTI_AGENT_WORKFLOW.md

---

## Integration with Existing Workflow

**Update to MULTI_AGENT_WORKFLOW.md:**

Add new "Phase 0" before existing Phase 1:

```markdown
## Phase 0: Session Start (Log Monitor Agent)

1. **Fetch logs automatically:**
   - Run: `ssh root@192.168.4.141 'ha logs --lines 200'`
   - Parse for errors/warnings

2. **Triage and route:**
   - Critical/High + Auto-fixable → Start Phase 1 with Claude Code
   - Critical/High + Needs input → Create task, present to user
   - Medium/Low → Log and track

3. **Present report to user:**
   - Summary of issues found
   - Actions taken (auto-fixes)
   - Tasks added to backlog
   - User input needed (if any)

4. **User decides:**
   - Continue with suggested task
   - Address different task
   - Acknowledge and proceed with planned work
```

---

## Example Scenarios

### Scenario 1: Auto-Fixable Light Group Issue

**Log Entry:**

```
WARNING (MainThread) [homeassistant.components.light.group] 
  Light group 'living_room_lamps' missing entity: light.floor_lamp_3
```

**Log Monitor Actions:**

1. **Classify:** Medium severity (group degraded, still partially functional)
2. **Auto-fix check:** YES - Entity likely renamed, check entity registry
3. **Handoff to Claude Code:**
   - SSH to server
   - Check entity registry for `floor_lamp` entities
   - Find renamed entity: `light.living_room_floor_lamp_3`
   - Update `light_groups.yaml`
   - Restart HA, verify group loads
4. **Handoff to Codex:** Document in CHANGELOG.md
5. **Update TASKS.md:** Mark as "Auto-fixed during session start"

**User sees:**

```
🔧 Auto-fixed: Light group entity mismatch
   - Updated living_room_lamps group with correct entity ID
   - Verified group functional after restart
```

### Scenario 2: Integration Auth Failure (Needs User Input)

**Log Entry:**

```
ERROR (MainThread) [homeassistant.components.tuya] 
  Authentication failed. Check credentials.
```

**Log Monitor Actions:**

1. **Classify:** High severity (cloud integration offline)
2. **Auto-fix check:** NO - Requires user credentials
3. **Create task in TASKS.md:**

```markdown
### Fix Tuya Integration Authentication Failure
**Priority:** HIGH
**Agent:** Claude Code
**Source:** Log Monitor Agent (detected: 2026-01-21 14:32)
**Log Context:**
```text
ERROR (MainThread) [homeassistant.components.tuya] 
  Authentication failed. Check credentials.
```

**Impact:** All Tuya cloud devices (8 lights) offline, voice control unavailable

**Suggested Fix:** 
1. Verify Tuya account credentials in config
2. Check if Tuya developer account API key expired
3. Re-authenticate via HA UI

**Questions for User:**
- [ ] Did you recently change your Tuya account password?
- [ ] Are you using Tuya Smart or Smart Life app?
- [ ] Do you have 2FA enabled on Tuya account?
```

**User sees:**

```
⚠️  HIGH priority issue detected: Tuya integration authentication failure
    → Added to backlog with troubleshooting steps
    → Please review questions in TASKS.md
```

---

## Cost Optimization

**Log Monitor runs automatically but efficiently:**

- Use fast models (Haiku/GPT-4o-mini) for initial parsing
- Only escalate to Claude Code for confirmed auto-fixes
- Batch similar issues into one task
- Cache known ignorable patterns
- Run on session start, not continuously (avoid constant API calls)

**Estimated cost per session:**

- Log fetch + parse: ~$0.01 (fast model)
- Auto-fix (if needed): ~$0.10-0.50 (Claude Code)
- Total: $0.01-0.51 per session start

**Benefit:** Proactive issue detection saves debugging time (typically $1-5 in agent costs)

---

## Future Enhancements

- **Pattern learning:** ML model to predict issue severity
- **Historical trending:** Dashboard showing error frequency over time
- **Integration health scores:** Rate each integration's stability
- **Automated testing:** After auto-fix, run test suite to verify
- **Slack/Discord notifications:** Alert user of critical issues via webhook
- **Predictive maintenance:** Detect patterns indicating impending failure

---

Last updated: 2026-01-21
