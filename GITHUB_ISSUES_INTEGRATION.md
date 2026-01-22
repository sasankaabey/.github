# GitHub Issues Integration Plan

**Purpose:** Sync TASKS.md with GitHub Issues for cross-repo visibility and tracking

**Status:** Planned (Not Yet Implemented)  
**Priority:** After core router is stable  
**Estimated Time:** 4-6 hours implementation

---

## Why GitHub Issues?

### Current State (TASKS.md only)
- ✅ Version controlled
- ✅ Simple markdown format
- ✅ Git-based workflow
- ❌ No cross-repo visibility
- ❌ No web UI for non-technical users
- ❌ No notifications
- ❌ Hard to track dependencies across projects

### Future State (TASKS.md + GitHub Issues)
- ✅ Everything from current state
- ✅ Cross-repo dashboard
- ✅ Web UI for stakeholders
- ✅ Email/Slack notifications
- ✅ Dependency tracking via issue links
- ✅ Milestone/project board integration
- ✅ Searchable history

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│ TASKS.md (Source of Truth)                      │
│ - Local files in each project                   │
│ - Git version controlled                        │
│ - Human-readable markdown                       │
└────────────────┬────────────────────────────────┘
                 │
                 │ Sync via router
                 ↓
┌─────────────────────────────────────────────────┐
│ GitHub Issues (External View)                   │
│ - Cross-repo visibility                         │
│ - Web UI for stakeholders                       │
│ - Notifications and tracking                    │
└─────────────────────────────────────────────────┘
```

### Design Principle
**TASKS.md remains the source of truth.** GitHub Issues are a synchronized external view, not the primary storage.

**Why?**
- Git commits provide full history
- Markdown is easier to edit locally
- Works offline
- No GitHub API rate limits for reading
- Can switch to different issue tracker later

---

## Implementation Phases

### Phase 1: Read-Only Sync (2 hours)
**Goal:** Create GitHub issues automatically from TASKS.md

**Features:**
- When router detects new task in TASKS.md → create GitHub issue
- Issue body contains task description, context files, acceptance criteria
- Labels: priority, agent, project, status
- Assignees: mapped from agent type

**No Changes Back to TASKS.md Yet** (one-way sync only)

**Tools:**
- GitHub REST API via `mcp_io_github_git` tools
- Parse TASKS.md to detect new tasks
- Create issue with proper formatting

**Code Location:** `.github/scripts/github_sync.py`

---

### Phase 2: Bidirectional Sync (2-3 hours)
**Goal:** Update TASKS.md when issues change, and vice versa

**Features:**
- Update GitHub issue status when TASKS.md changes
- Update GitHub issue comments when subtasks complete
- Close issue when task marked complete in TASKS.md
- **Optionally:** Import changes from GitHub back to TASKS.md

**Conflict Resolution:**
- TASKS.md wins in case of conflict
- Issue changes trigger review workflow
- Merge conflicts logged for manual resolution

**Tools:**
- GitHub webhooks (for real-time updates)
- Or: Polling during session start
- Git commits track all changes

---

### Phase 3: Issue-First Workflow (1 hour)
**Goal:** Allow creating tasks via GitHub Issues

**Features:**
- User creates GitHub issue with template
- Router imports issue to TASKS.md
- Router generates first prompt
- Status syncs bidirectionally

**Use Case:**
- Stakeholders without git access
- Mobile issue creation
- Integration with other tools

---

## Technical Design

### Data Model

**GitHub Issue Structure:**
```yaml
Title: "[project] Task Name"
Body: |
  **Status:** Not Started
  **Priority:** HIGH
  **Agent:** Codex
  **Estimated Time:** 30 minutes
  
  **Description:**
  Task description here...
  
  **Context Files:**
  - path/to/file1.md
  - path/to/file2.yaml
  
  **Acceptance Criteria:**
  - [ ] Criterion 1
  - [ ] Criterion 2
  
  **Subtasks:**
  - [ ] Subtask 1 (Agent: ChatGPT)
  - [ ] Subtask 2 (Agent: Codex)
  - [ ] Subtask 3 (Agent: Claude Code)
  
Labels:
  - priority:high
  - agent:codex
  - project:home-assistant-config
  - status:not-started
  
Assignee: @codex-agent (if using GitHub Apps)
```

### Sync Algorithm

```python
def sync_tasks_to_github(project_path: Path):
    """One-way sync: TASKS.md → GitHub Issues"""
    
    # 1. Parse TASKS.md
    tasks = parse_tasks_file(project_path / "TASKS.md")
    
    # 2. Get existing issues
    existing_issues = list_github_issues(
        owner="ankit",
        repo="sasankaabey",
        labels=[f"project:{project_path.name}"]
    )
    
    # 3. Create mapping (task ID → issue number)
    task_issue_map = load_mapping(".github/task_issue_map.json")
    
    # 4. For each task:
    for task in tasks:
        if task.id not in task_issue_map:
            # New task → create issue
            issue = create_github_issue(
                title=f"[{task.project}] {task.name}",
                body=format_issue_body(task),
                labels=get_labels(task)
            )
            task_issue_map[task.id] = issue.number
            
        else:
            # Existing task → update if changed
            issue_num = task_issue_map[task.id]
            if task_changed_since_last_sync(task):
                update_github_issue(
                    issue_num,
                    body=format_issue_body(task),
                    labels=get_labels(task)
                )
    
    # 5. Save mapping
    save_mapping(task_issue_map, ".github/task_issue_map.json")
```

### Mapping File

```json
{
  "home-assistant-config_implement_tuya_lights": 123,
  "home-assistant-config_motion_lighting": 124,
  "kitlabworks_user_auth": 125,
  "sync_metadata": {
    "last_sync": "2026-01-21T19:30:00Z",
    "sync_count": 15
  }
}
```

---

## Integration Points

### With Session Router

**On Session Start:**
```python
# In session_start.sh after health check
if [ "$GITHUB_SYNC_ENABLED" = "true" ]; then
    python3 .github/scripts/github_sync.py --sync-to-github
fi
```

**On Task Completion:**
```python
# In session_router.py when subtask completes
if task_complete:
    update_github_issue_status(task.id, "complete")
    add_github_issue_comment(task.id, "✅ Completed by {agent}")
```

**On Issue Creation (Webhook):**
```python
# GitHub webhook endpoint
@app.post("/webhook/github/issues")
def handle_issue_created(payload):
    if payload["action"] == "opened":
        import_issue_to_tasks_md(payload["issue"])
        trigger_router_for_new_task()
```

---

## Labels Strategy

### Priority Labels
- `priority:critical` 🔴
- `priority:high` 🟠
- `priority:medium` 🟡
- `priority:low` 🟢

### Agent Labels
- `agent:codex` 📝
- `agent:claude-code` 🖥️
- `agent:chatgpt` 💬
- `agent:perplexity` 🔍
- `agent:gemini` 🤖

### Project Labels
- `project:home-assistant-config` 🏠
- `project:kitlabworks` 💼
- `project:headache-tracker` 🩺

### Status Labels
- `status:not-started` ⚪
- `status:in-progress` 🔵
- `status:blocked` 🔴
- `status:ready-for-review` 🟡
- `status:complete` 🟢

### Type Labels
- `type:bug` 🐛
- `type:feature` ✨
- `type:docs` 📚
- `type:automation` 🤖
- `type:cleanup` 🧹

---

## Issue Templates

### Task Template

`.github/ISSUE_TEMPLATE/task.md`:
```markdown
---
name: Task
about: Create a new task for the multi-agent system
labels: status:not-started
---

## Task Description

Brief description of what needs to be done.

## Priority

- [ ] CRITICAL
- [ ] HIGH
- [x] MEDIUM
- [ ] LOW

## Assigned Agent

- [ ] Codex (documentation, YAML)
- [ ] Claude Code (server ops, deployment)
- [ ] ChatGPT (planning, architecture)
- [ ] Perplexity (research)
- [ ] Gemini (analysis)

## Project

- [ ] home-assistant-config
- [ ] kitlabworks
- [ ] headache-tracker

## Estimated Time

_e.g., 30 minutes, 1 hour, 2 hours_

## Context Files

List files that should be read first:
- 
- 

## Acceptance Criteria

- [ ] 
- [ ] 
- [ ] 

## Dependencies

Blocks:
- 

Blocked by:
- 

## Additional Context

Add any other context here.
```

---

## Benefits

### For You (Primary User)
1. **Cross-repo dashboard** - See all work across projects
2. **Progress tracking** - Visual representation of task flow
3. **Dependency visualization** - See what blocks what
4. **Historical search** - Find old tasks and decisions
5. **Mobile access** - Check status on phone

### For Stakeholders
1. **Web UI** - No git knowledge needed
2. **Notifications** - Email updates on task progress
3. **Comments** - Provide feedback on tasks
4. **Transparency** - See what agents are working on

### For AI Agents
1. **Standardized API** - GitHub REST API well-documented
2. **Rich context** - Issues can link to commits, PRs
3. **Automation** - GitHub Actions for workflows
4. **Integration** - Connect with other tools (Slack, etc.)

---

## Challenges & Solutions

### Challenge 1: API Rate Limits
**Problem:** GitHub API has rate limits (5000 requests/hour)

**Solution:**
- Cache issue data locally
- Batch updates
- Only sync on session start (not every git commit)
- Use conditional requests (If-Modified-Since headers)

### Challenge 2: Conflict Resolution
**Problem:** User edits issue on GitHub, agent edits TASKS.md

**Solution:**
- TASKS.md always wins
- GitHub changes trigger notification
- Manual merge for conflicts
- Lock issues during active work

### Challenge 3: Subtask Tracking
**Problem:** Subtasks generated by router, not in TASKS.md

**Solution:**
- Add subtasks as checklist in issue body
- Update checklist as subtasks complete
- Or: Create child issues (more complex)

### Challenge 4: Sensitive Information
**Problem:** TASKS.md might contain server IPs, keys, etc.

**Solution:**
- Sanitize issue bodies before sync
- Keep sensitive info in separate file
- Use GitHub private repos
- Or: Disable sync for sensitive projects

---

## Rollout Plan

### Week 1: Phase 1 Implementation
- [ ] Implement read-only sync
- [ ] Test with home-assistant-config project
- [ ] Create 5-10 test issues
- [ ] Verify labels and formatting

### Week 2: Phase 2 Implementation
- [ ] Add bidirectional sync
- [ ] Test status updates
- [ ] Test subtask completion comments
- [ ] Verify conflict handling

### Week 3: Phase 3 Implementation
- [ ] Add issue-first workflow
- [ ] Create issue templates
- [ ] Test end-to-end (issue → TASKS.md → prompt)
- [ ] Document for stakeholders

### Week 4: Polish & Documentation
- [ ] Add visual dashboard
- [ ] Create user guide
- [ ] Set up notifications
- [ ] Train stakeholders

---

## Configuration

### Enable/Disable Sync

`.github/config.json`:
```json
{
  "github_sync": {
    "enabled": true,
    "repo": "ankit/sasankaabey",
    "sync_interval": "on_session_start",
    "projects": [
      "home-assistant-config",
      "kitlabworks"
    ],
    "excluded_tasks": [
      "*SECRET*",
      "*PRIVATE*"
    ]
  }
}
```

### Environment Variables

```bash
# .env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
GITHUB_REPO=ankit/sasankaabey
GITHUB_SYNC_ENABLED=true
```

---

## Future Enhancements

### Milestone Tracking
- Map task phases to GitHub milestones
- Track sprint progress
- Burndown charts

### Project Boards
- Kanban view of all tasks
- Drag-and-drop status updates
- Cross-project boards

### GitHub Actions
- Auto-label based on content
- Auto-assign based on agent
- Auto-close stale tasks

### Copilot Integration
- Assign Copilot agent to issues
- Copilot creates PR to close issue
- Full automation loop

---

## Success Metrics

- [ ] 100% of TASKS.md tasks synced to GitHub
- [ ] <5 second sync time
- [ ] 0 sync conflicts in first month
- [ ] Stakeholders using web UI weekly
- [ ] Issue-first workflow functional

---

**Next Steps:**
1. ✅ Document plan (this file)
2. ⏳ Test and stabilize core router
3. ⏳ Implement Phase 1 (read-only sync)
4. ⏳ Test Phase 1 thoroughly
5. ⏳ Implement Phase 2 (bidirectional)
6. ⏳ Deploy to production

**Status:** Ready to implement after router is stable
