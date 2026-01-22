#!/usr/bin/env python3
"""
Session Router: Intelligent task orchestration for multi-agent workflows.

Architecture:
1. Analyzes all project TASKS.md files
2. Shows user backlog with "pick up where you left off" option
3. User selects task → Router decomposes into subtasks
4. Generates agent-specific prompts with handoff instructions
5. Tracks state → Next agent sees what to do next

Usage:
    ./session_router.py                    # Interactive mode (show backlog)
    ./session_router.py --last             # Auto-select last task
    ./session_router.py --next             # Auto-select next in sequence
"""

import json
import re
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime
import sys

# ============================================================================
# DATA MODELS
# ============================================================================

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    DEFERRED = 5

class Status(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    READY_FOR_REVIEW = "Ready for Review"
    READY_FOR_DEPLOYMENT = "Ready for Deployment"
    COMPLETE = "Complete"

class AgentType(Enum):
    CLAUDE_CODE = "Claude Code"
    CODEX = "Codex"
    CHATGPT = "ChatGPT"
    PERPLEXITY = "Perplexity"
    GEMINI = "Gemini"
    LOG_MONITOR = "Log Monitor"
    ROUTER = "Router (Decision Engine)"

@dataclass
class Subtask:
    """A decomposed unit of work"""
    id: str
    description: str
    agent: AgentType
    estimated_minutes: int
    dependencies: List[str] = field(default_factory=list)  # IDs of subtasks that must complete first
    parallel_ok: bool = True  # Can run in parallel with others
    status: Status = Status.NOT_STARTED
    prompt: str = ""  # Agent-specific prompt for this subtask

@dataclass
class Task:
    """A top-level task from TASKS.md"""
    id: str
    name: str
    project: str  # home-assistant-config, kitlabworks, etc.
    status: Status
    priority: Priority
    estimated_minutes: int
    agent: AgentType
    description: str
    context_files: List[str] = field(default_factory=list)
    blocks_tasks: List[str] = field(default_factory=list)  # Task IDs
    blocked_by: List[str] = field(default_factory=list)  # Task IDs
    subtasks: List[Subtask] = field(default_factory=list)
    current_subtask_index: int = 0  # Track progress through subtasks

@dataclass
class SessionState:
    """Persistent state between router invocations"""
    last_task_id: Optional[str] = None
    last_subtask_id: Optional[str] = None
    last_agent: Optional[str] = None
    last_updated: str = ""
    completed_subtasks: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)

# ============================================================================
# TASK PARSING
# ============================================================================

class TaskParser:
    """Parse TASKS.md files from all projects"""
    
    TASK_PATTERN = re.compile(r'^###\s+(.+)$', re.MULTILINE)
    STATUS_PATTERN = re.compile(r'\*\*Status:\*\*\s+(.+?)(?:\s*\(|$)')
    PRIORITY_PATTERN = re.compile(r'\*\*Priority:\*\*\s+(\w+)')
    AGENT_PATTERN = re.compile(r'\*\*Agent:\*\*\s+(.+?)(?:\s*→|$)')
    TIME_PATTERN = re.compile(r'\*\*Estimated Time:\*\*\s+(.+?)(?:\n|$)')
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        
    def find_all_tasks_files(self) -> List[Path]:
        """Find all TASKS.md files in workspace"""
        tasks_files = []
        for project_dir in self.workspace_root.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                tasks_file = project_dir / "TASKS.md"
                if tasks_file.exists():
                    tasks_files.append(tasks_file)
        return tasks_files
    
    def parse_tasks_file(self, tasks_file: Path) -> List[Task]:
        """Parse a single TASKS.md file"""
        content = tasks_file.read_text()
        project_name = tasks_file.parent.name
        tasks = []
        
        # Split by ### headers
        sections = re.split(r'^###\s+', content, flags=re.MULTILINE)[1:]  # Skip preamble
        
        for section in sections:
            lines = section.split('\n', 1)
            task_name = lines[0].strip()
            body = lines[1] if len(lines) > 1 else ""
            
            # Extract metadata
            status_match = self.STATUS_PATTERN.search(body)
            priority_match = self.PRIORITY_PATTERN.search(body)
            agent_match = self.AGENT_PATTERN.search(body)
            time_match = self.TIME_PATTERN.search(body)
            
            # Parse status
            status = Status.NOT_STARTED
            if status_match:
                status_text = status_match.group(1).strip()
                for s in Status:
                    if s.value in status_text:
                        status = s
                        break
            
            # Parse priority
            priority = Priority.MEDIUM
            if priority_match:
                priority_text = priority_match.group(1).upper()
                try:
                    priority = Priority[priority_text]
                except KeyError:
                    pass
            
            # Parse agent
            agent = AgentType.CODEX
            if agent_match:
                agent_text = agent_match.group(1).strip()
                for a in AgentType:
                    if a.value in agent_text:
                        agent = a
                        break
            
            # Parse time estimate
            estimated_minutes = 30
            if time_match:
                time_text = time_match.group(1)
                # Parse "20-30 minutes" or "1 hour" etc.
                numbers = re.findall(r'\d+', time_text)
                if numbers:
                    estimated_minutes = int(numbers[-1])  # Take last number
                    if 'hour' in time_text.lower():
                        estimated_minutes *= 60
            
            # Extract context files
            context_files = []
            context_match = re.search(r'\*\*Context to Read First:\*\*\s*\n((?:[\s\S]*?)(?=\n\*\*|\n###|\Z))', body)
            if context_match:
                context_text = context_match.group(1)
                # Find file paths (anything with .md, .yaml, .py, etc.)
                context_files = re.findall(r'[\w/.]+\.(?:md|yaml|yml|py|ts|tsx|json)', context_text, re.IGNORECASE)
            
            task_id = f"{project_name}_{task_name.lower().replace(' ', '_')[:30]}"
            
            tasks.append(Task(
                id=task_id,
                name=task_name,
                project=project_name,
                status=status,
                priority=priority,
                estimated_minutes=estimated_minutes,
                agent=agent,
                description=body[:200],  # First 200 chars
                context_files=context_files
            ))
        
        return tasks

    def parse_all_tasks(self) -> List[Task]:
        """Parse all TASKS.md files in workspace"""
        all_tasks = []
        for tasks_file in self.find_all_tasks_files():
            all_tasks.extend(self.parse_tasks_file(tasks_file))
        return all_tasks

# ============================================================================
# GIT CONTEXT
# ============================================================================

class GitAnalyzer:
    """Analyze git history to understand recent work"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
    
    def get_last_commit_info(self) -> Dict:
        """Get info about most recent commit"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%s|%an|%ar'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split('|')
                return {
                    'hash': parts[0],
                    'message': parts[1],
                    'author': parts[2],
                    'time_ago': parts[3]
                }
        except Exception as e:
            print(f"Warning: Could not get git info: {e}")
        return {}
    
    def get_recent_commits(self, n=10) -> List[Dict]:
        """Get recent commits"""
        try:
            result = subprocess.run(
                ['git', 'log', f'-{n}', '--format=%H|%s'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            commits = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    hash_val, message = line.split('|', 1)
                    commits.append({'hash': hash_val, 'message': message})
            return commits
        except Exception:
            return []
    
    def infer_last_task_from_commits(self, tasks: List[Task]) -> Optional[str]:
        """Try to infer what task was last worked on"""
        commits = self.get_recent_commits(5)
        for commit in commits:
            message = commit['message'].lower()
            # Look for "Task: [Name]" pattern
            task_match = re.search(r'task:\s*(.+?)\s*-', message, re.IGNORECASE)
            if task_match:
                task_name = task_match.group(1).strip()
                # Find matching task
                for task in tasks:
                    if task_name.lower() in task.name.lower() or task.name.lower() in task_name.lower():
                        return task.id
        return None

# ============================================================================
# TASK DECOMPOSITION ENGINE
# ============================================================================

class TaskDecomposer:
    """Break down high-level tasks into agent-specific subtasks"""
    
    def decompose_task(self, task: Task) -> List[Subtask]:
        """Decompose task based on its type and agent requirements"""
        
        # Example decomposition patterns
        subtasks = []
        
        # Pattern 1: Documentation + Implementation + Deployment (with review)
        if "implement" in task.name.lower() or "create" in task.name.lower():
            subtasks = [
                Subtask(
                    id=f"{task.id}_plan",
                    description=f"Plan implementation for: {task.name}",
                    agent=AgentType.CHATGPT,
                    estimated_minutes=10,
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_implement",
                    description=f"Implement: {task.name}",
                    agent=task.agent,
                    estimated_minutes=task.estimated_minutes - 30,
                    dependencies=[f"{task.id}_plan"],
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_review",
                    description=f"Review implementation: {task.name}",
                    agent=AgentType.CODEX,  # Codex reviews code quality, docs, conventions
                    estimated_minutes=10,
                    dependencies=[f"{task.id}_implement"],
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_test",
                    description=f"Test and validate: {task.name}",
                    agent=AgentType.CLAUDE_CODE,
                    estimated_minutes=10,
                    dependencies=[f"{task.id}_review"],
                    parallel_ok=False
                )
            ]
        
        # Pattern 2: Research + Documentation (with review)
        elif "document" in task.name.lower() or "research" in task.name.lower():
            subtasks = [
                Subtask(
                    id=f"{task.id}_research",
                    description=f"Research: {task.name}",
                    agent=AgentType.PERPLEXITY,
                    estimated_minutes=task.estimated_minutes // 3,
                    parallel_ok=True
                ),
                Subtask(
                    id=f"{task.id}_document",
                    description=f"Document findings: {task.name}",
                    agent=AgentType.CODEX,
                    estimated_minutes=task.estimated_minutes // 3,
                    dependencies=[f"{task.id}_research"],
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_review",
                    description=f"Review documentation: {task.name}",
                    agent=AgentType.CHATGPT,  # ChatGPT reviews clarity, completeness
                    estimated_minutes=task.estimated_minutes // 3,
                    dependencies=[f"{task.id}_document"],
                    parallel_ok=False
                )
            ]
        
        # Pattern 3: Home Assistant automation (YAML + Review + Deployment + Validation)
        elif task.project == "home-assistant-config":
            subtasks = [
                Subtask(
                    id=f"{task.id}_yaml",
                    description=f"Draft YAML for: {task.name}",
                    agent=AgentType.CODEX,
                    estimated_minutes=int(task.estimated_minutes * 0.4),
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_review",
                    description=f"Review YAML structure and conventions: {task.name}",
                    agent=AgentType.CHATGPT,  # ChatGPT reviews for logic, edge cases
                    estimated_minutes=int(task.estimated_minutes * 0.2),
                    dependencies=[f"{task.id}_yaml"],
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_validate",
                    description=f"Validate syntax and deploy: {task.name}",
                    agent=AgentType.CLAUDE_CODE,
                    estimated_minutes=int(task.estimated_minutes * 0.2),
                    dependencies=[f"{task.id}_review"],
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_test",
                    description=f"Test automation on server: {task.name}",
                    agent=AgentType.CLAUDE_CODE,
                    estimated_minutes=int(task.estimated_minutes * 0.2),
                    dependencies=[f"{task.id}_validate"],
                    parallel_ok=False
                )
            ]
        
        # Pattern 4: Bug fix or cleanup (implementation + validation)
        elif "fix" in task.name.lower() or "cleanup" in task.name.lower() or "refactor" in task.name.lower():
            subtasks = [
                Subtask(
                    id=f"{task.id}_fix",
                    description=f"Fix/cleanup: {task.name}",
                    agent=task.agent,
                    estimated_minutes=int(task.estimated_minutes * 0.7),
                    parallel_ok=False
                ),
                Subtask(
                    id=f"{task.id}_verify",
                    description=f"Verify fix: {task.name}",
                    agent=AgentType.CLAUDE_CODE,  # Claude Code tests the fix
                    estimated_minutes=int(task.estimated_minutes * 0.3),
                    dependencies=[f"{task.id}_fix"],
                    parallel_ok=False
                )
            ]
        
        # Default: Single subtask (no decomposition)
        else:
            subtasks = [
                Subtask(
                    id=f"{task.id}_complete",
                    description=task.name,
                    agent=task.agent,
                    estimated_minutes=task.estimated_minutes,
                    parallel_ok=False
                )
            ]
        
        return subtasks

# ============================================================================
# PROMPT GENERATION
# ============================================================================

class PromptGenerator:
    """Generate agent-specific prompts with handoff instructions"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
    
    def generate_prompt(self, task: Task, subtask: Subtask, session_state: SessionState) -> str:
        """Generate a complete prompt for an agent"""
        
        # Determine next subtask in sequence
        next_subtask = self._find_next_subtask(task, subtask)
        
        prompt = f"""# AGENT ASSIGNMENT: {subtask.agent.value}

## 🎯 Your Task

**{subtask.description}**

**Project:** {task.project}
**Estimated Time:** {subtask.estimated_minutes} minutes
**Priority:** {task.priority.name}

---

## 📖 Context to Read First

"""
        
        # Add context files
        if task.context_files:
            for ctx_file in task.context_files:
                prompt += f"1. {ctx_file}\n"
        else:
            prompt += f"1. {task.project}/LOCAL_CONTEXT.md (2 min overview)\n"
            prompt += f"2. {task.project}/TASKS.md (check your assignment)\n"
            prompt += f"3. .github/AGENTS.md (understand your role)\n"
        
        prompt += f"""
---

## 🔨 What You Need to Do

{self._get_task_specific_instructions(task, subtask)}

---

## ✅ Success Criteria

"""
        
        # Generate checklist
        prompt += self._generate_success_criteria(task, subtask)
        
        prompt += f"""
---

## 📝 Commit Instructions

When you complete this work:

1. **Commit your changes** with message:
   ```
   Task: {task.name} - {subtask.description}
   
   Completed by {subtask.agent.value}
   Part of larger task decomposition
   
   Status: {self._get_completion_status(task, subtask)}
   ```

2. **Update TASKS.md** to mark this subtask as complete

3. **Hand off to next agent:**
"""
        
        # Add handoff instructions
        if next_subtask:
            prompt += f"""
   Run `./session_router.py --next` to get the next prompt.
   
   **Next Agent:** {next_subtask.agent.value}
   **Next Task:** {next_subtask.description}
"""
        else:
            prompt += f"""
   This is the FINAL subtask for "{task.name}".
   
   Run `./session_router.py --next` to mark task complete and pick next work.
"""
        
        prompt += """
---

## 🔄 Handoff Protocol

**IMPORTANT:** When you finish:
1. Commit your work
2. Push to git
3. Tell the user: "Run `./session_router.py --next` to continue"

The router will automatically detect your completed work and generate the next prompt.

---

"""
        
        return prompt
    
    def _find_next_subtask(self, task: Task, current_subtask: Subtask) -> Optional[Subtask]:
        """Find the next subtask in the dependency chain"""
        if not task.subtasks:
            return None
        
        try:
            current_index = task.subtasks.index(current_subtask)
            if current_index + 1 < len(task.subtasks):
                return task.subtasks[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def _get_task_specific_instructions(self, task: Task, subtask: Subtask) -> str:
        """Generate specific instructions based on task type"""
        
        # Check if this is a review/validation subtask
        is_review = "review" in subtask.id or "verify" in subtask.id
        
        if is_review and subtask.agent == AgentType.CODEX:
            return f"""
**As Codex (Reviewer), your role is:**
- Review code quality and conventions
- Check documentation completeness
- Verify YAML syntax and structure
- Ensure consistency with existing patterns

**For this review task:**
1. Read the work done by previous agent (check git log)
2. Review against conventions in {task.project}/LOCAL_CONTEXT.md
3. Check for:
   - Code follows style guide
   - Documentation is clear
   - No obvious bugs or issues
   - Naming conventions followed
4. If issues found:
   - Document them clearly
   - Suggest fixes (or fix them yourself if minor)
5. If all good:
   - Approve and document what was validated
   - Hand off to next agent
"""
        
        elif is_review and subtask.agent == AgentType.CHATGPT:
            return f"""
**As ChatGPT (Reviewer), your role is:**
- Review logic and design decisions
- Check for edge cases and potential issues
- Validate completeness
- Suggest improvements

**For this review task:**
1. Read the work done by previous agent (check git log)
2. Analyze for:
   - Logic correctness
   - Edge cases covered
   - User experience considerations
   - Potential failure modes
3. If concerns found:
   - Document them with examples
   - Suggest alternatives
4. If approved:
   - Document what was validated
   - Note any future enhancements
"""
        
        elif is_review and subtask.agent == AgentType.CLAUDE_CODE:
            return f"""
**As Claude Code (Validator), your role is:**
- Test functionality
- Verify deployment works
- Check server-side behavior
- Validate real-world operation

**For this validation task:**
1. Review previous agent's work (check git log)
2. Test the implementation:
   - Run on actual server (if HA project)
   - Check logs for errors
   - Verify expected behavior
3. If issues found:
   - Debug and fix them
   - Document what was wrong
4. If working:
   - Document test results
   - Confirm ready for production
"""
        
        elif subtask.agent == AgentType.CODEX:
            return f"""
**As Codex, your role is:**
- Documentation writing
- YAML drafting
- Code formatting
- PR reviews

**For this task:**
1. Read the context files listed above
2. {subtask.description}
3. Follow conventions documented in {task.project}/LOCAL_CONTEXT.md
4. Commit your work with clear messages
"""
        
        elif subtask.agent == AgentType.CLAUDE_CODE:
            return f"""
**As Claude Code, your role is:**
- Server operations (SSH)
- Deployment and validation
- Complex debugging
- Entity registry edits

**For this task:**
1. Verify work from previous agent (check git log)
2. {subtask.description}
3. If deployment: Use sync_to_ha.sh and test on 192.168.4.141
4. Confirm everything works before committing
"""
        
        elif subtask.agent == AgentType.CHATGPT:
            return f"""
**As ChatGPT, your role is:**
- Planning and brainstorming
- Breaking down complex problems
- Architecture decisions
- Coordinating workflows

**For this task:**
1. {subtask.description}
2. Document your decisions clearly
3. Create actionable next steps for implementation agents
"""
        
        else:
            return f"{subtask.description}\n\nFollow the conventions in {task.project}/LOCAL_CONTEXT.md"
    
    def _generate_success_criteria(self, task: Task, subtask: Subtask) -> str:
        """Generate success checklist"""
        
        # Check if this is a review/validation subtask
        is_review = "review" in subtask.id or "verify" in subtask.id
        
        if is_review:
            criteria = f"""
- [ ] Reviewed previous agent's work (checked git log)
- [ ] Verified against project conventions
- [ ] Checked for logic errors or edge cases
- [ ] Tested functionality (if applicable)
"""
            
            if subtask.agent == AgentType.CLAUDE_CODE:
                criteria += "- [ ] Tested on server (if HA project)\n"
                criteria += "- [ ] No errors in logs\n"
            
            criteria += """- [ ] Documented review findings
- [ ] Either: Approved and ready for next step
- [ ] Or: Issues documented with clear fixes needed
- [ ] Changes committed to git
"""
        else:
            criteria = f"""
- [ ] Task completed: {subtask.description}
- [ ] Code follows project conventions
- [ ] Changes committed to git
- [ ] TASKS.md updated with progress
"""
        
            if subtask.agent == AgentType.CLAUDE_CODE and not is_review:
                criteria += "- [ ] Tested on server (if applicable)\n"
                criteria += "- [ ] No errors in logs\n"
            
            if subtask.agent == AgentType.CODEX:
                criteria += "- [ ] Documentation is clear and complete\n"
                criteria += "- [ ] YAML is valid (if applicable)\n"
        
        return criteria
    
    def _get_completion_status(self, task: Task, subtask: Subtask) -> str:
        """Get status text for commit message"""
        next_subtask = self._find_next_subtask(task, subtask)
        if next_subtask:
            return f"In Progress - Next: {next_subtask.agent.value}"
        else:
            return "Complete - Ready for next task"

# ============================================================================
# SESSION ROUTER (Main Orchestrator)
# ============================================================================

class SessionRouter:
    """Main orchestration engine"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.state_file = workspace_root / ".github" / "session_state.json"
        self.parser = TaskParser(workspace_root)
        self.git_analyzer = GitAnalyzer(workspace_root)
        self.decomposer = TaskDecomposer()
        self.prompt_generator = PromptGenerator(workspace_root)
        self.state = self._load_state()
    
    def _load_state(self) -> SessionState:
        """Load persistent session state"""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                return SessionState(**data)
            except Exception:
                pass
        return SessionState()
    
    def _save_state(self):
        """Save session state"""
        self.state_file.parent.mkdir(exist_ok=True)
        self.state.last_updated = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(self.state.to_dict(), indent=2))
    
    def show_backlog(self, tasks: List[Task]) -> str:
        """Display backlog with last task highlighted"""
        
        # Group by project
        by_project = {}
        for task in tasks:
            if task.status not in [Status.COMPLETE]:
                if task.project not in by_project:
                    by_project[task.project] = []
                by_project[task.project].append(task)
        
        # Rank tasks
        for project_tasks in by_project.values():
            project_tasks.sort(key=lambda t: (
                t.status != Status.IN_PROGRESS,  # In progress first
                t.priority.value,  # Then by priority
                len(t.blocks_tasks),  # Then by how many tasks it blocks
                t.estimated_minutes  # Then by time (shorter first)
            ))
        
        output = "\n" + "="*70 + "\n"
        output += "🎯 SESSION START - Task Backlog\n"
        output += "="*70 + "\n\n"
        
        # Show "pick up where you left off" option
        if self.state.last_task_id:
            last_task = next((t for t in tasks if t.id == self.state.last_task_id), None)
            if last_task and last_task.status != Status.COMPLETE:
                output += "🔄 CONTINUE LAST TASK?\n\n"
                output += f"  [0] Continue: {last_task.name}\n"
                output += f"      Status: {last_task.status.value}\n"
                output += f"      Last worked: {self.state.last_updated[:16] if self.state.last_updated else 'Unknown'}\n"
                output += f"      Agent: {self.state.last_agent or last_task.agent.value}\n"
                output += "\n" + "-"*70 + "\n\n"
        
        # Show backlog by project
        option_num = 1
        task_map = {}  # option -> task
        
        for project, project_tasks in sorted(by_project.items()):
            output += f"📁 {project.upper()}\n\n"
            
            for task in project_tasks:
                status_emoji = {
                    Status.NOT_STARTED: "⚪",
                    Status.IN_PROGRESS: "🔵",
                    Status.BLOCKED: "🔴",
                    Status.READY_FOR_REVIEW: "🟡",
                    Status.READY_FOR_DEPLOYMENT: "🟢"
                }.get(task.status, "⚪")
                
                priority_indicator = "🔥" if task.priority == Priority.CRITICAL else \
                                   "⬆️" if task.priority == Priority.HIGH else ""
                
                output += f"  [{option_num}] {status_emoji} {task.name} {priority_indicator}\n"
                output += f"      {task.agent.value} • {task.estimated_minutes}min • {task.status.value}\n"
                
                if task.blocked_by:
                    output += f"      🔒 Blocked by: {', '.join(task.blocked_by)}\n"
                if task.blocks_tasks:
                    output += f"      ⛓️  Blocks {len(task.blocks_tasks)} other task(s)\n"
                
                output += "\n"
                
                task_map[option_num] = task
                option_num += 1
            
            output += "\n"
        
        output += "="*70 + "\n"
        output += "Enter task number (or 0 to continue last task): "
        
        return output, task_map
    
    def select_task_interactive(self) -> Optional[Task]:
        """Show backlog and let user select"""
        tasks = self.parser.parse_all_tasks()
        
        # Infer last task if not in state
        if not self.state.last_task_id:
            inferred_id = self.git_analyzer.infer_last_task_from_commits(tasks)
            if inferred_id:
                self.state.last_task_id = inferred_id
                self._save_state()
        
        backlog_text, task_map = self.show_backlog(tasks)
        print(backlog_text, end='')
        
        try:
            choice = input().strip()
            
            if choice == '0' and self.state.last_task_id:
                # Continue last task
                return next((t for t in tasks if t.id == self.state.last_task_id), None)
            
            choice_num = int(choice)
            if choice_num in task_map:
                return task_map[choice_num]
            
        except (ValueError, KeyboardInterrupt):
            print("\nAborted.")
            return None
        
        print("Invalid choice.")
        return None
    
    def process_task(self, task: Task) -> str:
        """Process selected task - decompose and generate first prompt"""
        
        # Decompose if not already done
        if not task.subtasks:
            task.subtasks = self.decomposer.decompose_task(task)
        
        # Find next subtask to work on
        next_subtask = self._find_next_incomplete_subtask(task)
        
        if not next_subtask:
            print(f"\n✅ Task '{task.name}' is already complete!")
            return ""
        
        # Generate prompt
        prompt = self.prompt_generator.generate_prompt(task, next_subtask, self.state)
        
        # Update state
        self.state.last_task_id = task.id
        self.state.last_subtask_id = next_subtask.id
        self.state.last_agent = next_subtask.agent.value
        self._save_state()
        
        return prompt
    
    def _find_next_incomplete_subtask(self, task: Task) -> Optional[Subtask]:
        """Find next subtask that needs work"""
        for subtask in task.subtasks:
            if subtask.id not in self.state.completed_subtasks:
                # Check dependencies
                deps_met = all(dep in self.state.completed_subtasks for dep in subtask.dependencies)
                if deps_met:
                    return subtask
        return None
    
    def continue_last_task(self) -> Optional[str]:
        """Auto-continue last task (for --next flag)"""
        if not self.state.last_task_id:
            print("No previous task found. Run without --next to select a task.")
            return None
        
        tasks = self.parser.parse_all_tasks()
        task = next((t for t in tasks if t.id == self.state.last_task_id), None)
        
        if not task:
            print(f"Could not find task: {self.state.last_task_id}")
            return None
        
        # Check if last subtask was completed (look at git commits)
        if self._check_subtask_completed():
            if self.state.last_subtask_id:
                self.state.completed_subtasks.append(self.state.last_subtask_id)
                self._save_state()
        
        return self.process_task(task)
    
    def _check_subtask_completed(self) -> bool:
        """Check git log to see if subtask was completed"""
        last_commit = self.git_analyzer.get_last_commit_info()
        if not last_commit:
            return False
        
        # Look for subtask ID in commit message
        if self.state.last_subtask_id and self.state.last_subtask_id in last_commit['message']:
            return True
        
        return False

# ============================================================================
# CLI
# ============================================================================

def main():
    workspace_root = Path.cwd()
    
    # Check if we're in a valid workspace
    github_dir = workspace_root / ".github"
    if not github_dir.exists():
        print("Error: Not in a valid workspace (no .github/ directory found)")
        sys.exit(1)
    
    router = SessionRouter(workspace_root)
    
    # Parse CLI flags
    if len(sys.argv) > 1:
        if sys.argv[1] == '--next':
            # Auto-continue workflow
            prompt = router.continue_last_task()
            if prompt:
                print("\n" + "="*70)
                print("📋 NEXT TASK PROMPT")
                print("="*70 + "\n")
                print(prompt)
            sys.exit(0)
        
        elif sys.argv[1] == '--last':
            # Auto-select last task
            tasks = router.parser.parse_all_tasks()
            if router.state.last_task_id:
                task = next((t for t in tasks if t.id == router.state.last_task_id), None)
                if task:
                    prompt = router.process_task(task)
                    print("\n" + "="*70)
                    print("📋 TASK PROMPT")
                    print("="*70 + "\n")
                    print(prompt)
                    sys.exit(0)
            print("No previous task found.")
            sys.exit(1)
    
    # Interactive mode
    task = router.select_task_interactive()
    
    if task:
        prompt = router.process_task(task)
        
        print("\n" + "="*70)
        print("📋 TASK PROMPT (Copy & Paste into Agent)")
        print("="*70 + "\n")
        print(prompt)
        print("\n" + "="*70)
        print("💡 TIP: Copy the prompt above and paste into your chosen agent")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
