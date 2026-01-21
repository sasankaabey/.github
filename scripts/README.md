# Log Monitor Scripts

Automated log monitoring and triage for Home Assistant projects.

## Scripts

### `log_monitor.py`

Core Python script that fetches, parses, and triages HA logs.

**Features:**
- SSH to HA server and fetch logs
- Parse logs with regex patterns
- Classify issues by severity
- Auto-detect fixable issues
- Create tasks in TASKS.md
- Generate session reports

**Usage:**

```bash
# Standard run
python3 log_monitor.py --project-path ~/home-assistant-config

# Dry run (no changes, report only)
python3 log_monitor.py --project-path ~/home-assistant-config --dry-run

# Custom HA server
python3 log_monitor.py --project-path ~/ha-config --host 192.168.1.100

# Fetch more log lines
python3 log_monitor.py --project-path ~/ha-config --lines 500

# JSON output (for scripting)
python3 log_monitor.py --project-path ~/ha-config --json
```

**Exit Codes:**
- `0` - No critical/high issues (system healthy)
- `1` - High priority issues detected
- `2` - Critical issues detected

### `session_start.sh`

Convenience wrapper for running log monitor at session start.

**Usage:**

```bash
# From .github/scripts directory
./session_start.sh

# From anywhere
~/.github/scripts/session_start.sh

# With options (passed through to log_monitor.py)
./session_start.sh --dry-run
./session_start.sh --lines 300
```

**Output:**
- Colored terminal output
- Session report with issue summary
- Tasks added to TASKS.md (if issues found)

## Setup

### 1. Ensure SSH access to HA server

```bash
# Test SSH connection
ssh root@192.168.4.141 'ha logs --lines 10'
```

If you need to set up SSH keys:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519

# Copy to HA server
ssh-copy-id root@192.168.4.141
```

### 2. Test the script

```bash
cd /Users/ankit/Developer/sasankaabey/.github/scripts

# Dry run to see what it would do
./session_start.sh --dry-run
```

### 3. Add to your workflow

**Option A: Manual invocation**

Run at the start of each HA session:

```bash
~/.github/scripts/session_start.sh
```

**Option B: Shell alias**

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias ha-session='~/.github/scripts/session_start.sh'
```

Then just run:

```bash
ha-session
```

**Option C: VS Code task**

Add to `.vscode/tasks.json`:

```json
{
  "label": "HA Session Start",
  "type": "shell",
  "command": "${workspaceFolder}/../.github/scripts/session_start.sh",
  "problemMatcher": [],
  "group": {
    "kind": "build",
    "isDefault": true
  }
}
```

Run with: `Cmd+Shift+B` (Mac) or `Ctrl+Shift+B` (Windows/Linux)

## Issue Classification

### Severity Levels

| Severity | When to Use | Action |
|----------|-------------|--------|
| **Critical** | System non-functional, core component failed | Immediate alert + task |
| **High** | Integration offline, automation broken | Task creation |
| **Medium** | Feature degraded, entity unavailable | Task creation (lower priority) |
| **Low** | Performance warning, deprecated feature | Log only |
| **Ignorable** | Known false positive, info message | Skip |

### Issue Types Detected

- **Integration Failure** - Integration setup failed
- **Entity Missing** - Entity not found in registry
- **Entity Unavailable** - Device/entity offline
- **Auth Failure** - Authentication failed
- **Config Error** - Invalid configuration
- **Component Load Failure** - Component failed to load
- **Deprecated Feature** - Using deprecated syntax/feature
- **Performance Warning** - Slow operations
- **Network Error** - Connection issues

### Auto-Fixable Issues

Some issues can be automatically fixed (future enhancement):

- Entity ID mismatch in light groups (entity renamed)
- Deprecated service calls (update to new syntax)
- Missing helper entities (create from pattern)
- YAML formatting issues (fix indentation)

**Note:** Auto-fix is designed but not yet implemented. Currently, all issues create tasks for manual review.

## Extending the Script

### Add New Log Patterns

Edit `LogPatterns` class in `log_monitor.py`:

```python
class LogPatterns:
    # Add your pattern
    MY_PATTERN = re.compile(
        r'ERROR.*some pattern here',
        re.IGNORECASE
    )
```

Then handle it in `LogParser._classify_line()`:

```python
match = self.patterns.MY_PATTERN.search(line)
if match:
    return LogIssue(
        timestamp=timestamp,
        severity=Severity.MEDIUM,
        issue_type=IssueType.MY_TYPE,
        message="Description of issue",
        component=match.group(1),
        log_line=line,
        auto_fixable=False
    )
```

### Add New Ignorable Patterns

Edit `LogPatterns.IGNORABLE_PATTERNS` list:

```python
IGNORABLE_PATTERNS = [
    re.compile(r'pattern to ignore', re.IGNORECASE),
    # Add yours here
]
```

### Custom Actions

Override `TaskGenerator.create_task()` to customize task format or add custom actions for specific issue types.

## Troubleshooting

**SSH connection fails:**
- Check SSH access: `ssh root@192.168.4.141`
- Verify HA server IP address
- Ensure SSH keys are set up

**No issues detected but logs have errors:**
- Errors might match ignorable patterns
- Check `LogPatterns.IGNORABLE_PATTERNS`
- Run with `--json` to see raw issue list

**Script fails with Python error:**
- Ensure Python 3.7+ installed: `python3 --version`
- Check script has execute permissions: `chmod +x log_monitor.py`

**Tasks not added to TASKS.md:**
- Verify TASKS.md exists in project
- Check for "### For Claude Code (Server/Config)" section
- Run with `--dry-run` to see what would be added

## Future Enhancements

- [ ] Implement auto-fix for safe issues (entity mismatches, syntax)
- [ ] Add pattern learning (ML for severity prediction)
- [ ] Historical trending (error frequency dashboard)
- [ ] Integration health scores
- [ ] Slack/Discord notifications for critical issues
- [ ] Automated testing after auto-fixes
- [ ] Predictive maintenance (detect patterns before failure)

## Integration with Multi-Agent Workflow

The Log Monitor Agent is designed to run automatically at session start:

1. **User starts HA session** → `session_start.sh` runs
2. **Log Monitor fetches & parses logs** → Issues classified
3. **Auto-fixable issues** → Handed off to Claude Code (future)
4. **Issues needing input** → Added to TASKS.md
5. **Session report** → Shown to user
6. **User decides** → Continue with suggested task or choose different work

See `/.github/LOG_MONITOR_AGENT.md` for complete workflow documentation.
