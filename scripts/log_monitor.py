#!/usr/bin/env python3
"""
Log Monitor Agent - Proactive HA Log Monitoring & Auto-Triage

Automatically fetches, parses, and classifies Home Assistant logs at session start.
Routes issues to appropriate agents or creates backlog tasks.

Usage:
    python log_monitor.py --project-path /path/to/home-assistant-config
    python log_monitor.py --project-path ~/ha-config --dry-run
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    IGNORABLE = "Ignorable"


class IssueType(Enum):
    """Types of issues detected in logs"""
    INTEGRATION_FAILURE = "Integration Setup Failed"
    ENTITY_MISSING = "Entity Missing"
    ENTITY_UNAVAILABLE = "Entity Unavailable"
    AUTH_FAILURE = "Authentication Failed"
    CONFIG_ERROR = "Configuration Error"
    COMPONENT_LOAD_FAILURE = "Component Load Failed"
    DEPRECATED_FEATURE = "Deprecated Feature"
    PERFORMANCE_WARNING = "Performance Warning"
    NETWORK_ERROR = "Network Error"
    UNKNOWN = "Unknown Error"


@dataclass
class LogIssue:
    """Represents a detected log issue"""
    timestamp: str
    severity: Severity
    issue_type: IssueType
    message: str
    component: Optional[str]
    log_line: str
    auto_fixable: bool
    fix_suggestion: Optional[str] = None
    user_questions: List[str] = None
    
    def __post_init__(self):
        if self.user_questions is None:
            self.user_questions = []


class LogPatterns:
    """Regex patterns for log parsing"""
    
    # Integration failures
    INTEGRATION_SETUP_FAILED = re.compile(
        r'ERROR.*Setup of (?:integration )?[\'"]?(\w+)[\'"]? failed',
        re.IGNORECASE
    )
    
    INTEGRATION_CONNECT_FAILED = re.compile(
        r'ERROR.*Unable to connect to (\w+)',
        re.IGNORECASE
    )
    
    AUTH_FAILED = re.compile(
        r'ERROR.*Authentication failed.*?(?:for )?[\'"]?(\w+)?[\'"]?',
        re.IGNORECASE
    )
    
    # Entity issues
    ENTITY_NOT_FOUND = re.compile(
        r'(?:WARNING|ERROR).*Entity [\'"]?(\S+)[\'"]? (?:does not exist|not found)',
        re.IGNORECASE
    )
    
    ENTITY_UNAVAILABLE = re.compile(
        r'WARNING.*[\'"]?(\S+)[\'"]? is unavailable',
        re.IGNORECASE
    )
    
    # Configuration errors
    CONFIG_INVALID = re.compile(
        r'ERROR.*Invalid config for [\'"]?(\w+)[\'"]?',
        re.IGNORECASE
    )
    
    CONFIG_PARSE_FAILED = re.compile(
        r'ERROR.*Failed to parse [\'"]?(.+?)[\'"]?',
        re.IGNORECASE
    )
    
    # Component issues
    COMPONENT_LOAD_FAILED = re.compile(
        r'ERROR.*Failed to (?:load|setup) component [\'"]?(\w+)[\'"]?',
        re.IGNORECASE
    )
    
    # Deprecated features
    DEPRECATED = re.compile(
        r'WARNING.*deprecated.*?(\w+)',
        re.IGNORECASE
    )
    
    # Performance warnings
    SLOW_OPERATION = re.compile(
        r'WARNING.*(?:Updating|Executing) [\'"]?(\S+)[\'"]? took (?:longer than )?(\d+\.\d+)',
        re.IGNORECASE
    )
    
    BLOCKING_CALL = re.compile(
        r'WARNING.*Blocking call to [\'"]?(\S+)[\'"]?',
        re.IGNORECASE
    )
    
    # Known ignorable patterns
    IGNORABLE_PATTERNS = [
        re.compile(r'VS\s*Code.*schema', re.IGNORECASE),
        re.compile(r'Updating.*state took', re.IGNORECASE),  # Informational only
        re.compile(r'http.*disconnected', re.IGNORECASE),  # Normal client disconnect
        re.compile(r'Starting Home Assistant', re.IGNORECASE),  # Startup messages
        re.compile(r'ALTS creds ignored', re.IGNORECASE),  # Google Cloud credential warnings (expected)
        re.compile(r'Failed to refresh device state for.*tuya_local', re.IGNORECASE),  # Transient tuya errors
    ]


class LogFetcher:
    """Handles fetching logs from HA server"""
    
    def __init__(self, host: str = "192.168.4.141", user: str = "root"):
        self.host = host
        self.user = user
    
    def fetch_logs(self, lines: int = 200) -> Optional[str]:
        """Fetch recent logs via SSH"""
        try:
            cmd = ['ssh', f'{self.user}@{self.host}', f'ha core logs | tail -n {lines}']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"❌ Failed to fetch logs: {result.stderr}", file=sys.stderr)
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout fetching logs from HA server", file=sys.stderr)
            return None
        except Exception as e:
            print(f"❌ Error fetching logs: {e}", file=sys.stderr)
            return None


class LogParser:
    """Parses logs and classifies issues"""
    
    def __init__(self):
        self.patterns = LogPatterns()
    
    def parse_logs(self, log_content: str) -> List[LogIssue]:
        """Parse log content and extract issues"""
        issues = []
        
        for line in log_content.split('\n'):
            if not line.strip():
                continue
            
            # Check ignorable patterns first
            if self._is_ignorable(line):
                continue
            
            # Extract timestamp if present
            timestamp = self._extract_timestamp(line)
            
            # Check each pattern
            issue = self._classify_line(line, timestamp)
            if issue:
                issues.append(issue)
        
        return issues
    
    def _is_ignorable(self, line: str) -> bool:
        """Check if line matches ignorable patterns"""
        for pattern in self.patterns.IGNORABLE_PATTERNS:
            if pattern.search(line):
                return True
        return False
    
    def _extract_timestamp(self, line: str) -> str:
        """Extract timestamp from log line"""
        # Simple timestamp extraction (HA logs format: YYYY-MM-DD HH:MM:SS)
        ts_match = re.match(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', line)
        if ts_match:
            return ts_match.group(1)
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _classify_line(self, line: str, timestamp: str) -> Optional[LogIssue]:
        """Classify a log line into an issue"""
        
        # Integration setup failure
        match = self.patterns.INTEGRATION_SETUP_FAILED.search(line)
        if match:
            component = match.group(1)
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.HIGH,
                issue_type=IssueType.INTEGRATION_FAILURE,
                message=f"Integration '{component}' failed to setup",
                component=component,
                log_line=line,
                auto_fixable=False,
                user_questions=[
                    f"Have you recently modified {component} configuration?",
                    f"Is {component} service accessible/online?",
                    "Check credentials if authentication-based integration"
                ]
            )
        
        # Authentication failure
        match = self.patterns.AUTH_FAILED.search(line)
        if match:
            component = match.group(1) if match.group(1) else "unknown"
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.HIGH,
                issue_type=IssueType.AUTH_FAILURE,
                message=f"Authentication failed for '{component}'",
                component=component,
                log_line=line,
                auto_fixable=False,
                user_questions=[
                    "Have credentials expired or changed?",
                    "Is 2FA enabled and causing issues?",
                    "Check integration configuration in HA UI"
                ]
            )
        
        # Entity not found
        match = self.patterns.ENTITY_NOT_FOUND.search(line)
        if match:
            entity_id = match.group(1)
            # Check if this might be auto-fixable (entity renamed)
            auto_fixable = 'group' in line.lower() or 'automation' in line.lower()
            fix_suggestion = None
            
            if auto_fixable:
                fix_suggestion = (
                    f"Check if {entity_id} was renamed. "
                    f"Update references in light_groups.yaml or automations."
                )
            
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.MEDIUM,
                issue_type=IssueType.ENTITY_MISSING,
                message=f"Entity '{entity_id}' not found",
                component=entity_id.split('.')[0] if '.' in entity_id else None,
                log_line=line,
                auto_fixable=auto_fixable,
                fix_suggestion=fix_suggestion
            )
        
        # Entity unavailable
        match = self.patterns.ENTITY_UNAVAILABLE.search(line)
        if match:
            entity_id = match.group(1)
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.MEDIUM,
                issue_type=IssueType.ENTITY_UNAVAILABLE,
                message=f"Entity '{entity_id}' is unavailable",
                component=entity_id.split('.')[0] if '.' in entity_id else None,
                log_line=line,
                auto_fixable=False,
                user_questions=[
                    f"Is the {entity_id.split('.')[0]} device powered on?",
                    "Check device connectivity (WiFi, Zigbee, Z-Wave)",
                    "Try restarting the integration"
                ]
            )
        
        # Configuration error
        match = self.patterns.CONFIG_INVALID.search(line)
        if match:
            component = match.group(1)
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.HIGH,
                issue_type=IssueType.CONFIG_ERROR,
                message=f"Invalid configuration for '{component}'",
                component=component,
                log_line=line,
                auto_fixable=False,
                user_questions=[
                    f"Check {component} configuration in configuration.yaml",
                    "Run HA config validation",
                    "Look for YAML syntax errors"
                ]
            )
        
        # Deprecated feature
        match = self.patterns.DEPRECATED.search(line)
        if match:
            feature = match.group(1)
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.LOW,
                issue_type=IssueType.DEPRECATED_FEATURE,
                message=f"Deprecated feature in use: '{feature}'",
                component=feature,
                log_line=line,
                auto_fixable=True,
                fix_suggestion=f"Update to current syntax for {feature}"
            )
        
        # Performance warning
        match = self.patterns.SLOW_OPERATION.search(line)
        if match:
            operation = match.group(1)
            duration = match.group(2)
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.LOW,
                issue_type=IssueType.PERFORMANCE_WARNING,
                message=f"Slow operation: '{operation}' took {duration}s",
                component=operation,
                log_line=line,
                auto_fixable=False
            )
        
        # Generic ERROR/CRITICAL lines
        if re.search(r'\b(ERROR|CRITICAL)\b', line, re.IGNORECASE):
            return LogIssue(
                timestamp=timestamp,
                severity=Severity.MEDIUM,
                issue_type=IssueType.UNKNOWN,
                message="Unclassified error",
                component=None,
                log_line=line,
                auto_fixable=False
            )
        
        return None


class TaskGenerator:
    """Generates tasks for TASKS.md"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.tasks_file = project_path / "TASKS.md"
    
    def create_task(self, issue: LogIssue) -> str:
        """Generate task markdown for an issue"""
        task = f"""
### Fix: {issue.issue_type.value} - {issue.component or 'Unknown'}
**Priority:** {issue.severity.value.upper()}
**Agent:** {"Claude Code" if issue.severity in [Severity.CRITICAL, Severity.HIGH] else "Codex"}
**Source:** Log Monitor Agent (detected: {datetime.now().strftime("%Y-%m-%d %H:%M")})

**Log Context:**
```text
{issue.log_line}
```

**Impact:** {issue.message}

**Timestamp:** {issue.timestamp}

"""
        
        if issue.fix_suggestion:
            task += f"**Suggested Fix:** {issue.fix_suggestion}\n\n"
        
        if issue.user_questions:
            task += "**Questions for User:**\n"
            for q in issue.user_questions:
                task += f"- [ ] {q}\n"
            task += "\n"
        
        return task
    
    def add_tasks_to_backlog(self, issues: List[LogIssue], dry_run: bool = False) -> int:
        """Add issues to TASKS.md backlog"""
        if not self.tasks_file.exists():
            print(f"⚠️  TASKS.md not found at {self.tasks_file}")
            return 0
        
        # Group issues by severity
        high_priority = [i for i in issues if i.severity in [Severity.CRITICAL, Severity.HIGH]]
        medium_priority = [i for i in issues if i.severity == Severity.MEDIUM]
        
        if not high_priority and not medium_priority:
            return 0
        
        tasks_content = self.tasks_file.read_text()
        
        # Find insertion point (after "For Claude Code" or "For Codex" section)
        insertion_marker = "### For Claude Code (Server/Config)"
        
        if insertion_marker not in tasks_content:
            print(f"⚠️  Could not find insertion point in TASKS.md")
            return 0
        
        # Generate task entries
        new_tasks = []
        
        for issue in high_priority:
            if not dry_run:
                new_tasks.append(self.create_task(issue))
        
        for issue in medium_priority:
            if not dry_run:
                new_tasks.append(self.create_task(issue))
        
        if dry_run:
            print("\n📝 Would add these tasks to TASKS.md:")
            for issue in high_priority + medium_priority:
                print(f"   - [{issue.severity.value}] {issue.message}")
            return len(high_priority) + len(medium_priority)
        
        # Insert tasks
        new_section = f"\n#### Log Monitor Detected Issues ({datetime.now().strftime('%Y-%m-%d')})\n"
        new_section += "\n".join(new_tasks)
        
        # Insert after Claude Code section header
        parts = tasks_content.split(insertion_marker, 1)
        if len(parts) == 2:
            updated_content = (
                parts[0] + insertion_marker + new_section + "\n" + parts[1]
            )
            self.tasks_file.write_text(updated_content)
            return len(new_tasks)
        
        return 0


class SessionReporter:
    """Generates session reports"""
    
    def __init__(self):
        self.report_lines = []
    
    def generate_report(self, issues: List[LogIssue], auto_fixed: List[LogIssue]) -> str:
        """Generate comprehensive session report"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Count by severity
        critical = [i for i in issues if i.severity == Severity.CRITICAL]
        high = [i for i in issues if i.severity == Severity.HIGH]
        medium = [i for i in issues if i.severity == Severity.MEDIUM]
        low = [i for i in issues if i.severity == Severity.LOW]
        ignorable = [i for i in issues if i.severity == Severity.IGNORABLE]
        
        report = f"""
## 🔍 Log Monitor Report

**Session:** {now}
**Logs Analyzed:** Last 200 lines

### Summary
"""
        
        if not critical and not high:
            report += "- ✅ No critical issues\n"
        else:
            if critical:
                report += f"- 🚨 {len(critical)} CRITICAL issue(s)\n"
            if high:
                report += f"- ⚠️  {len(high)} HIGH priority issue(s)\n"
        
        if medium:
            report += f"- ⚠️  {len(medium)} medium-priority issue(s) added to backlog\n"
        
        if auto_fixed:
            report += f"- 🔧 {len(auto_fixed)} issue(s) auto-fixed\n"
        
        if low:
            report += f"- 📝 {len(low)} low-priority warning(s) logged\n"
        
        # Auto-fixed issues
        if auto_fixed:
            report += "\n### Auto-Fixed Issues\n"
            for idx, issue in enumerate(auto_fixed, 1):
                report += f"{idx}. **{issue.message}** - {issue.fix_suggestion}\n"
        
        # New tasks added
        tasks_added = [i for i in issues if i.severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM]]
        if tasks_added:
            report += "\n### New Tasks Added\n"
            for idx, issue in enumerate(tasks_added, 1):
                report += f"{idx}. **[{issue.severity.value}] {issue.issue_type.value}** - {issue.message}\n"
                if issue.component:
                    report += f"   - Component: {issue.component}\n"
        
        # Recommendations
        if critical or high:
            report += "\n### 🚨 Immediate Action Required\n"
            for issue in critical + high:
                report += f"- {issue.message}\n"
                if issue.user_questions:
                    for q in issue.user_questions[:2]:  # Show first 2 questions
                        report += f"  - {q}\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Log Monitor Agent - Proactive HA log monitoring"
    )
    parser.add_argument(
        '--project-path',
        type=Path,
        required=True,
        help='Path to home-assistant-config project'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without making changes (report only)'
    )
    parser.add_argument(
        '--host',
        default='192.168.4.141',
        help='HA server hostname/IP (default: 192.168.4.141)'
    )
    parser.add_argument(
        '--lines',
        type=int,
        default=200,
        help='Number of log lines to fetch (default: 200)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Validate project path
    if not args.project_path.exists():
        print(f"❌ Project path does not exist: {args.project_path}", file=sys.stderr)
        return 1
    
    print("🔍 Log Monitor Agent - Starting session analysis...")
    print(f"   Project: {args.project_path}")
    print(f"   HA Server: {args.host}")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}\n")
    
    # Fetch logs
    print("📡 Fetching logs from HA server...")
    fetcher = LogFetcher(host=args.host)
    logs = fetcher.fetch_logs(lines=args.lines)
    
    if not logs:
        print("❌ Failed to fetch logs")
        return 1
    
    print(f"✅ Retrieved {len(logs.splitlines())} lines\n")
    
    # Parse logs
    print("🔬 Analyzing logs...")
    parser_obj = LogParser()
    issues = parser_obj.parse_logs(logs)
    
    print(f"✅ Found {len(issues)} potential issues\n")
    
    # Filter auto-fixable issues (for future implementation)
    auto_fixable = [i for i in issues if i.auto_fixable]
    needs_user_input = [i for i in issues if not i.auto_fixable]
    
    # Generate tasks
    task_gen = TaskGenerator(args.project_path)
    tasks_added = task_gen.add_tasks_to_backlog(needs_user_input, dry_run=args.dry_run)
    
    if tasks_added > 0:
        if args.dry_run:
            print(f"📝 Would add {tasks_added} task(s) to TASKS.md\n")
        else:
            print(f"✅ Added {tasks_added} task(s) to TASKS.md\n")
    
    # Generate report
    reporter = SessionReporter()
    report = reporter.generate_report(issues, [])  # auto_fixed empty for now
    
    if args.json:
        # JSON output
        output = {
            'timestamp': datetime.now().isoformat(),
            'issues_found': len(issues),
            'tasks_created': tasks_added,
            'issues': [
                {
                    'severity': i.severity.value,
                    'type': i.issue_type.value,
                    'message': i.message,
                    'component': i.component,
                    'auto_fixable': i.auto_fixable,
                    'timestamp': i.timestamp
                }
                for i in issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable report
        print(report)
    
    # Exit code based on severity
    if any(i.severity == Severity.CRITICAL for i in issues):
        return 2  # Critical issues found
    elif any(i.severity == Severity.HIGH for i in issues):
        return 1  # High priority issues found
    else:
        return 0  # No critical/high issues


if __name__ == '__main__':
    sys.exit(main())
