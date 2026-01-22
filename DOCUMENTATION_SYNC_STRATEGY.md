# Multi-Repo Documentation Sync Strategy

**Purpose:** Ensure documentation evolves with the system and stays synchronized across organization and project levels

**Status:** Design Phase  
**Last Updated:** 2026-01-21

---

## Core Principle

> **"Documentation is a living artifact that evolves with the work."**

As the multi-agent system evolves through real work, patterns emerge, workflows change, and decisions are made. This knowledge **must be captured** at the appropriate level (org-wide or project-specific) and **must stay synchronized**.

---

## Documentation Hierarchy

```
sasankaabey/                          ← Workspace root
├── .github/                          ← ORG-LEVEL DOCS
│   ├── AGENTS.md                     → Agent roles, decision tree
│   ├── MULTI_AGENT_WORKFLOW.md       → Process guide
│   ├── SESSION_ROUTER.md             → Router documentation
│   ├── LOG_MONITOR_AGENT.md          → Health check system
│   ├── GITHUB_ISSUES_INTEGRATION.md  → Integration plan
│   ├── TESTING_LOG.md                → Testing results
│   ├── EVOLUTION_LOG.md              → Lessons learned
│   └── PATTERNS/                     → Reusable templates
│       ├── TASKS_MD_TEMPLATE.md
│       ├── LOCAL_CONTEXT_TEMPLATE.md
│       └── AUTOMATION_PATTERN.md
│
├── home-assistant-config/            ← PROJECT-LEVEL DOCS
│   ├── LOCAL_CONTEXT.md              → "What is this project?"
│   ├── TASKS.md                      → Current work queue
│   ├── DECISIONS.md                  → Project decisions
│   ├── CHANGELOG.md                  → User-facing changes
│   └── HOME_ASSISTANT.md             → HA-specific conventions
│
├── kitlabworks/
│   ├── LOCAL_CONTEXT.md
│   ├── TASKS.md
│   ├── DECISIONS.md
│   └── CHANGELOG.md
│
└── headache-tracker/
    ├── LOCAL_CONTEXT.md
    ├── TASKS.md
    └── CHANGELOG.md
```

---

## Documentation Layers

### Layer 1: Organization-Level (`.github/`)

**Purpose:** Cross-project patterns, agent roles, workflow processes

**When to Update:**
- New agent role added
- Workflow process changes
- New pattern discovered
- Architecture decisions made
- System capabilities change

**Who Updates:**
- Any agent during work (if they discover a pattern)
- Router agent (documents workflow improvements)
- You (manual updates for major changes)

**Examples:**
- Agent role added → Update `AGENTS.md`
- New decomposition pattern → Update `SESSION_ROUTER.md`
- Lesson learned → Add to `EVOLUTION_LOG.md`
- Test results → Append to `TESTING_LOG.md`

---

### Layer 2: Project-Level (each project root)

**Purpose:** Project-specific context, conventions, current work

**When to Update:**
- Feature added/changed → Update `CHANGELOG.md`
- Architecture decision → Add to `DECISIONS.md`
- Convention established → Update `LOCAL_CONTEXT.md`
- Work starts/completes → Update `TASKS.md`

**Who Updates:**
- Agents working on that project
- You (manual updates for major changes)

**Examples:**
- Tuya lights renamed → Document in `CHANGELOG.md`
- Light groups pattern → Add to `DECISIONS.md`
- Entity naming convention → Update `LOCAL_CONTEXT.md`
- Task completed → Mark in `TASKS.md`

---

## Update Triggers

### Automatic Triggers (Future)

```python
# In session_router.py
def on_task_complete(task: Task):
    """Auto-update docs when task completes"""
    
    # Update project CHANGELOG if user-facing
    if is_user_facing_change(task):
        append_to_changelog(task.project, task.name, task.description)
    
    # Update EVOLUTION_LOG if new pattern discovered
    if discovered_new_pattern(task):
        log_pattern_to_evolution(task.pattern_description)
    
    # Update AGENTS.md if workflow changed
    if workflow_changed(task):
        propose_agents_md_update(task.workflow_change)
```

### Manual Triggers (Current)

**Agent Responsibilities:**
```markdown
## When You Complete Work

1. **Always update:**
   - [project]/TASKS.md (mark task complete)
   - Git commit message (clear description)

2. **Update if applicable:**
   - [project]/CHANGELOG.md (user-facing changes)
   - [project]/DECISIONS.md (architecture decisions)
   - .github/EVOLUTION_LOG.md (new patterns learned)

3. **Ask user to update if major:**
   - .github/AGENTS.md (new agent or role change)
   - .github/MULTI_AGENT_WORKFLOW.md (process change)
   - .github/SESSION_ROUTER.md (router behavior change)
```

---

## Sync Mechanisms

### Option 1: Git-Based Sync (Current ✅)

**How it works:**
- Agents commit doc updates with their code changes
- Git commits serve as changelog
- Next agent reads updated docs from git

**Pros:**
- Simple, no extra infrastructure
- Full version history via git log
- Works offline
- Auditable (every change has commit)

**Cons:**
- Manual updates required
- Easy to forget
- No automated enforcement

**Example:**
```bash
# Agent completes Tuya light renaming
git add automations/lighting/*.yaml
git add light_groups.yaml
git add CHANGELOG.md  # ← Remember to update!
git commit -m "Task: Rename Tuya lights - Complete

Renamed 8 Tuya lights to standard convention
Updated light_groups.yaml with new entity IDs
Documented in CHANGELOG.md

Status: Ready for deployment"
```

---

### Option 2: Post-Commit Hook Sync (Future)

**How it works:**
- Git hook detects commit
- Analyzes commit message and changed files
- Auto-updates relevant docs

**Implementation:**
```bash
# .git/hooks/post-commit
#!/bin/bash

COMMIT_MSG=$(git log -1 --pretty=%B)

# If task commit, check for doc updates
if [[ $COMMIT_MSG == Task:* ]]; then
    # Check if CHANGELOG needs update
    if git diff HEAD~1 --name-only | grep -E '\.(yaml|py|ts)$'; then
        if ! git diff HEAD~1 --name-only | grep 'CHANGELOG.md'; then
            echo "⚠️  Warning: Code changed but CHANGELOG.md not updated"
            echo "   Consider updating CHANGELOG.md if user-facing"
        fi
    fi
    
    # Check if new pattern emerged
    if [[ $COMMIT_MSG == *"pattern"* ]]; then
        echo "💡 New pattern detected! Consider updating EVOLUTION_LOG.md"
    fi
fi
```

---

### Option 3: Router-Managed Sync (Future)

**How it works:**
- Router detects completed subtasks
- Prompts agent: "Did you discover a new pattern?"
- Auto-updates docs based on agent response
- Commits docs separately

**Implementation:**
```python
# In prompt_generator.py
def generate_prompt_with_doc_sync(task, subtask):
    prompt = base_prompt(task, subtask)
    
    prompt += """
    
## 📚 Documentation Updates

Before completing this subtask, answer:

1. **Is this a user-facing change?**
   - [ ] Yes → Update [project]/CHANGELOG.md
   - [ ] No → Skip

2. **Did you make an architecture decision?**
   - [ ] Yes → Document in [project]/DECISIONS.md
   - [ ] No → Skip

3. **Did you discover a new pattern/approach?**
   - [ ] Yes → Add to .github/EVOLUTION_LOG.md
   - [ ] No → Skip

4. **Did the workflow process change?**
   - [ ] Yes → Flag for manual review of .github/MULTI_AGENT_WORKFLOW.md
   - [ ] No → Skip

**Router will check these on completion.**
"""
    
    return prompt
```

---

### Option 4: Documentation Agent (Future)

**How it works:**
- Dedicated "Documentation Agent" role
- Reviews completed work
- Updates all relevant docs
- Runs as final step of each task

**Workflow:**
```
Task Complete
     ↓
Documentation Agent reviews:
  - What changed?
  - User-facing?
  - New pattern?
  - Architecture decision?
     ↓
Updates:
  - CHANGELOG.md (if user-facing)
  - DECISIONS.md (if architectural)
  - EVOLUTION_LOG.md (if pattern)
  - LOCAL_CONTEXT.md (if convention)
     ↓
Commits doc updates
     ↓
Hands back to router
```

---

## Documentation Standards

### CHANGELOG.md Format

```markdown
# Changelog

All notable user-facing changes to this project.

## [Unreleased]

### Added
- Motion-triggered lighting automation in living room
- Voice command support for "Good Night" scene

### Changed
- Tuya lights renamed to standard convention (light.location_description)
- Light groups now defined in YAML (not UI)

### Fixed
- Laundry notification now handles dryer door sensor correctly

## [2026-01-21]

### Added
- Session Router for intelligent task orchestration
- Log Monitor Agent for proactive health checks
```

### DECISIONS.md Format

```markdown
# Architecture Decisions

## Decision: Use YAML for Light Groups (2026-01-15)

**Context:**
- UI-based groups not version controlled
- Hard to track changes
- Entity IDs must match exactly

**Decision:**
Use `platform: group` in light_groups.yaml instead of UI groups.

**Consequences:**
- ✅ Version controlled via git
- ✅ Clear entity ID mapping
- ❌ Requires HA restart to apply changes
- ❌ Can't use UI to edit

**Alternative Considered:**
UI groups, but rejected due to lack of version control.
```

### EVOLUTION_LOG.md Format

```markdown
# Evolution Log

Patterns and lessons learned as the system evolves.

## 2026-01-21: Task Decomposition Needs Review Step

**What we learned:**
Work can benefit from validation by different agent before deployment.

**Pattern discovered:**
Implement → Review (different agent) → Deploy → Test

**Why it matters:**
- Catches errors before production
- Different perspectives improve quality
- Separates implementation from validation

**Applied to:**
- session_router.py decomposition patterns
- All future implementation tasks

**Related Decisions:**
- Added review subtasks to all patterns
- Codex reviews code quality
- ChatGPT reviews logic
- Claude Code validates functionality
```

---

## Cross-Repo Sync

### Challenge
How to keep org-level docs synchronized when multiple projects contribute to the pattern library?

### Solution: Contribution Flow

```
Project Work (e.g., home-assistant-config)
      ↓
Agent discovers pattern (e.g., "Light groups in YAML")
      ↓
Agent documents in project DECISIONS.md
      ↓
Agent flags: "This could be org-level pattern"
      ↓
You review and decide:
  - Add to .github/PATTERNS/?
  - Update MULTI_AGENT_WORKFLOW.md?
  - Just keep in project?
      ↓
If org-level: Copy pattern to .github/PATTERNS/
      ↓
Other projects can reference org pattern
```

### Pattern Contribution Template

`.github/PATTERNS/PATTERN_TEMPLATE.md`:
```markdown
# Pattern: [Name]

**Source Project:** home-assistant-config  
**Date Discovered:** 2026-01-21  
**Status:** Proven (used successfully 3+ times)

## Problem

What problem does this solve?

## Solution

Describe the pattern.

## When to Use

- Scenario 1
- Scenario 2

## When NOT to Use

- Anti-pattern 1
- Anti-pattern 2

## Example

```yaml
# Example code
```

## Variations

Alternative approaches.

## Related Patterns

- Link to other patterns

## History

- 2026-01-21: Initial discovery
- 2026-01-25: Refined after 3 uses
- 2026-02-01: Added variation for X
```

---

## Enforcement

### Commit Message Linter (Future)

```python
# .github/scripts/check_commit.py

def check_doc_updates(commit):
    """Verify doc updates for task commits"""
    
    if not commit.message.startswith("Task:"):
        return True  # Not a task commit
    
    changed_files = commit.changed_files
    
    # Check 1: Code changed but no CHANGELOG?
    if has_user_facing_code(changed_files):
        if "CHANGELOG.md" not in changed_files:
            warn("Code changed but CHANGELOG.md not updated")
    
    # Check 2: Architecture change but no DECISIONS?
    if has_architectural_change(commit):
        if "DECISIONS.md" not in changed_files:
            warn("Architecture changed but DECISIONS.md not updated")
    
    # Check 3: New pattern but no EVOLUTION_LOG?
    if "pattern" in commit.message.lower():
        if ".github/EVOLUTION_LOG.md" not in changed_files:
            warn("Pattern mentioned but EVOLUTION_LOG.md not updated")
    
    return True  # Don't block, just warn
```

### Router Checklist (Current)

**In every prompt:**
```markdown
## 📝 Commit Instructions

When you complete this work:

1. **Commit your changes** with message:
   [Standard commit message format]

2. **Update documentation:**
   - [ ] TASKS.md (mark subtask complete)
   - [ ] CHANGELOG.md (if user-facing change)
   - [ ] DECISIONS.md (if architecture decision)
   - [ ] EVOLUTION_LOG.md (if new pattern discovered)

3. **Hand off to next agent:**
   [Handoff instructions]
```

---

## Success Metrics

### Short-term (1 month)
- [ ] 100% of tasks have TASKS.md updates
- [ ] 80% of user-facing changes have CHANGELOG entries
- [ ] 50% of architecture decisions documented in DECISIONS.md
- [ ] 5+ patterns captured in EVOLUTION_LOG.md

### Medium-term (3 months)
- [ ] 0 undocumented patterns
- [ ] .github/ docs referenced in 50% of task prompts
- [ ] PROJECT-level docs up-to-date for all projects
- [ ] Onboarding time reduced (measured via new agent performance)

### Long-term (6 months)
- [ ] Automated doc sync working
- [ ] Pattern library with 20+ proven patterns
- [ ] Cross-repo patterns reused successfully
- [ ] New project can bootstrap from templates in minutes

---

## Maintenance Schedule

### Daily (via session router)
- Check TASKS.md updates
- Verify commit messages reference docs

### Weekly (manual review)
- Review EVOLUTION_LOG for patterns to promote to .github/PATTERNS/
- Check for outdated org-level docs
- Sync any project-specific patterns up to org level

### Monthly (comprehensive audit)
- Review all .github/ docs for accuracy
- Check for duplicate documentation
- Merge redundant patterns
- Archive obsolete information

---

## Future Automation Ideas

### 1. Doc Coverage Report
```python
def generate_doc_coverage_report():
    """Check which tasks have documentation"""
    
    tasks = parse_all_tasks()
    
    for task in tasks:
        if task.status == "Complete":
            coverage = {
                "has_changelog": check_changelog(task),
                "has_decision": check_decisions(task),
                "has_pattern": check_evolution_log(task)
            }
            
            if not all(coverage.values()):
                warn(f"Task {task.name} missing docs: {coverage}")
```

### 2. Auto-Generated Index
```python
def generate_doc_index():
    """Create index of all documentation"""
    
    index = {
        "org_level": scan_github_dir(),
        "project_level": {
            project: scan_project_docs(project)
            for project in get_all_projects()
        },
        "patterns": scan_patterns_dir()
    }
    
    write_index(".github/DOC_INDEX.md", index)
```

### 3. Documentation Consistency Checker
```python
def check_doc_consistency():
    """Find contradictions across docs"""
    
    # Check for conflicting information
    # Check for outdated references
    # Check for broken links
    # Report issues
```

---

## Rollout Plan

### Week 1: Standards ✅ DONE
- [x] Define documentation hierarchy
- [x] Create templates (PATTERN_TEMPLATE, etc.)
- [x] Document sync strategy (this file)

### Week 2: Manual Process
- [ ] Train agents on doc update requirements
- [ ] Add doc checklists to all prompts
- [ ] Review 10 task completions for compliance

### Week 3: Automated Checks
- [ ] Implement commit message linter
- [ ] Add doc coverage report
- [ ] Set up weekly review automation

### Week 4: Full Automation
- [ ] Enable post-commit hooks
- [ ] Auto-generate doc indices
- [ ] Documentation Agent role activated

---

**Next Actions:**
1. ✅ Document the strategy (this file)
2. ⏳ Fix critical router issues (TESTING_LOG.md)
3. ⏳ Test doc updates in real workflow
4. ⏳ Refine based on usage
5. ⏳ Implement automation

**Status:** Design complete, ready for implementation after router is stable
