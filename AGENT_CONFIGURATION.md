# Agent Configuration System

> Make the multi-agent system "pliable" — dynamically add, remove, and switch between available AI agents based on your current access

---

## Overview

This system allows you to:
- **Dynamically manage** which AI agents are available for task routing
- **Add custom agents** or services via interactive menu
- **Enable/disable** agents without removing configuration
- **Assign agents by specialty** (documentation, yaml, debugging, research, etc.)
- **Test agent availability** before routing tasks

**Key principle:** The session router uses whatever agents you have configured. No code changes needed when adding/removing agents.

---

## Quick Start

### 1. View Current Agents

```bash
# Interactive menu
~/.github/scripts/agent_config

# Or command line
~/.github/scripts/agent_config list

# Show current config
~/.github/scripts/agent_config read-config
```

### 2. Add a New Agent

```bash
# Interactive add
~/.github/scripts/agent_config add

# Prompts for:
# - Agent ID (e.g., "my-llm")
# - Display name
# - Description
# - Cost (free/low/medium/high)
# - Specialties (comma-separated)
# - API key required? (y/n)
# - Notes
```

### 3. Enable/Disable Agents

```bash
# Enable
~/.github/scripts/agent_config enable chatgpt

# Disable (still in config, won't be assigned)
~/.github/scripts/agent_config disable perplexity
```

### 4. Test Agent Availability

```bash
~/.github/scripts/agent_config test chatgpt

# Output:
# ✓ Agent 'ChatGPT' is available
# ⚠ Agent requires API key in CHATGPT_API_KEY
```

---

## Default Agents (Pre-Configured)

| Agent | Cost | Specialties | Status |
|-------|------|-------------|--------|
| **Claude Code** | High | server-ops, debugging, ssh, ha-deployment | ✓ Enabled |
| **Codex** | Low | documentation, yaml, formatting, review | ✓ Enabled |
| **ChatGPT** | Medium | planning, architecture, review, brainstorm | ✓ Enabled |
| **Perplexity** | Medium | research, docs, external-knowledge | ✓ Enabled |
| **Gemini** | Medium | analysis, summarization, large-docs | ✓ Enabled |

---

## Command Reference

### Agent Management Commands

```bash
# List all agents
agent_config list

# Add new agent (interactive)
agent_config add

# Enable an agent
agent_config enable <agent-id>

# Disable an agent (keeps in config)
agent_config disable <agent-id>

# Remove agent (deletes from config)
agent_config remove <agent-id>

# Test agent availability
agent_config test <agent-id>

# Export configuration as JSON
agent_config export

# Show current config file location
agent_config read-config
```

### Interactive Menu

```bash
agent_config

# Shows numbered menu:
# 1. List agents
# 2. Add agent
# 3. Enable agent
# 4. Disable agent
# 5. Remove agent
# 6. Test agent
# 7. Export config
# 8. Reset to defaults
# 0. Exit
```

---

## Configuration File

**Location:** `~/.config/session-router/agents.json`

**Format:**
```json
{
  "claude-code": {
    "id": "claude-code",
    "name": "Claude (Code Interpreter)",
    "description": "Server operations, SSH, debugging...",
    "enabled": true,
    "cost": "high",
    "specialties": ["server-ops", "debugging", "ssh"],
    "api_key_required": false,
    "endpoint": null,
    "notes": "Expert-level capability..."
  },
  "chatgpt": {
    "id": "chatgpt",
    "name": "ChatGPT",
    "enabled": true,
    "cost": "medium",
    "specialties": ["planning", "architecture", "review"],
    "api_key_required": true,
    ...
  }
}
```

**Edit manually if needed:**
```bash
# View
cat ~/.config/session-router/agents.json | jq

# Edit
nano ~/.config/session-router/agents.json
```

---

## How Session Router Uses This

### 1. **Dynamic Task Assignment**

When session router decomposes a task, it calls:

```python
from agent_config_cli import AgentConfig

config = AgentConfig()

# Get agents with specific specialty
yaml_agents = config.get_enabled_agents(specialty="yaml")

# Get best agent for task type
agent = config.get_agent_by_specialty("documentation")
```

### 2. **Task Decomposition Patterns**

Each pattern now uses **dynamic agent assignment**:

```
Implementation Task:
  Plan (ChatGPT specialty: planning)
  → Implement (Assigned agent specialty: debugging)
  → Review (Codex specialty: review)
  → Test (Claude Code specialty: server-ops)

Documentation Task:
  Research (Perplexity specialty: research)
  → Document (Codex specialty: documentation)
  → Review (ChatGPT specialty: review)

HA Automation Task:
  Draft YAML (Codex specialty: yaml)
  → Review (ChatGPT specialty: review)
  → Deploy (Claude Code specialty: server-ops)
  → Test (Claude Code specialty: server-ops)
```

### 3. **Agent Selection Logic**

Router selects agents in this order:

1. **Specialty match** - Find agent with matching specialty
2. **Enabled filter** - Only use enabled agents
3. **Cost optimization** - Prefer low-cost agents when possible
4. **Fallback** - Default to "claude-code" if no match

---

## Example: Adding Custom Service

Suppose you have access to **Anthropic Claude** (not Claude Code):

### Step 1: Add to Config

```bash
~/.github/scripts/agent_config add
```

**Input:**
```
Agent ID: anthropic-claude
Display name: Claude (via Anthropic)
Description: General-purpose AI for brainstorming, analysis, complex reasoning
Cost: high
Specialties: planning, architecture, analysis, brainstorming
Requires API key? y
Notes: Direct API access, best for complex reasoning
```

### Step 2: Router Automatically Uses It

Next time session router needs "planning" agent:

```
Old: Assigns ChatGPT (if enabled)
New: Now has choice between ChatGPT OR Anthropic Claude
```

---

## Example: Budget Optimization

You have limited API calls. Disable expensive agents:

```bash
# Disable high-cost agents
agent_config disable chatgpt
agent_config disable gemini
agent_config disable perplexity

# Keep low-cost agents active
# (Claude Code, Codex)

# Router now auto-selects from:
# - Claude Code (when needed)
# - Codex (for docs/yaml)

# Result: $0 API costs
```

---

## Example: Testing Integration

Before deploying:

```bash
# Test all agents
agent_config test claude-code
agent_config test codex
agent_config test chatgpt

# Output:
# ✓ Claude Code is available
# ✓ Codex is available
# ⚠ ChatGPT requires API key in CHATGPT_API_KEY

# If any agent fails, session router will skip it
```

---

## Specialties Reference

Use these specialties when adding custom agents:

- **server-ops** - SSH, deployment, HA administration
- **debugging** - Problem diagnosis, error analysis
- **ssh** - Server access, file manipulation
- **ha-deployment** - Home Assistant specific deployments
- **documentation** - Writing, formatting, examples
- **yaml** - YAML validation, config generation
- **formatting** - Code cleanup, linting
- **review** - Code review, quality checks
- **planning** - Architecture, design, strategy
- **architecture** - System design decisions
- **brainstorm** - Ideation, creative problem-solving
- **research** - External knowledge, citations
- **docs** - Documentation and help
- **external-knowledge** - Access to current web data
- **analysis** - Data analysis, summation
- **summarization** - Condensing large documents
- **large-docs** - Processing big files

---

## Troubleshooting

### "Agent config not found"

```bash
# Initialize default config
python3 ~/.github/scripts/agent_config_cli.py read-config
```

### "Agent requires API key"

```bash
# Set environment variable
export CHATGPT_API_KEY="sk-..."

# Or add to ~/.bash_profile / ~/.zshrc
echo 'export CHATGPT_API_KEY="sk-..."' >> ~/.zshrc
```

### "No enabled agents for specialty"

```bash
# Check which agents have specialty
agent_config list

# Enable an agent
agent_config enable chatgpt

# Or add new agent with that specialty
agent_config add
```

### Reset to Defaults

```bash
# Via menu
agent_config
# Then select option 8

# Or manually
rm ~/.config/session-router/agents.json
agent_config read-config
```

---

## Integration with Session Router

### Current State

```bash
session_start.sh → phase 1: health check → phase 2: task selection
                                                         ↓
                                        (uses available agents from config)
```

### How It Works

1. **Session start** calls `session_router.py`
2. **Session router** loads agent config from `~/.config/session-router/agents.json`
3. **Task parser** identifies what needs doing
4. **Task decomposer** breaks it into subtasks
5. **Agent assignment** uses dynamic agent list
6. **Prompt generator** creates agent-specific instructions
7. **Session state** saved for continuation

### Adding New Workflow

If you want to add **Ollama** (local LLM):

```bash
agent_config add

# Agent ID: ollama-local
# Name: Ollama (Local)
# Description: Local LLM for offline planning and brainstorming
# Cost: free
# Specialties: planning, architecture, brainstorm
# API Key required: n
# Endpoint: http://localhost:11434
```

Then session router **automatically assigns it** to planning tasks!

---

## Best Practices

### 1. **Keep Common Agents Enabled**

Most workflows need:
- Documentation (Codex)
- Planning (ChatGPT)
- Server ops (Claude Code)

### 2. **Use Specialties Correctly**

When adding agents, pick **relevant specialties**:
- ✓ Correct: yaml, documentation, review
- ✗ Incorrect: very-specialized, ultra-advanced

### 3. **Test Before Using**

```bash
agent_config test <new-agent-id>
```

### 4. **Document in Notes**

```bash
agent_config add

# ... when prompted for Notes:
"Integration requires OpenAI account. Set OPENAI_API_KEY env var."
```

### 5. **Version Control**

Track agent config:

```bash
git -C ~/.config/session-router add agents.json
git -C ~/.config/session-router commit -m "Updated agent config"
```

---

## What's Next

### Phase 1 (Current): ✅ Agent Management
- [x] Dynamic agent configuration
- [x] CLI commands (add, remove, enable, disable)
- [x] Agent specialties
- [x] Cost tracking
- [x] API key requirements

### Phase 2 (Coming): Integration with Session Router
- [ ] Task assignment uses agent config
- [ ] Specialty-based routing
- [ ] Cost-optimized task decomposition
- [ ] Agent fallback logic

### Phase 3 (Future): UI/Automation
- [ ] Web dashboard for agent management
- [ ] Auto-detect available agents
- [ ] Performance monitoring
- [ ] Cost tracking dashboard

---

## Files Modified

- **Created:** `agent_config_cli.py` (full CRUD system)
- **Created:** `agent_config` (bash wrapper)
- **Created:** `dynamic_agents.py` (session router integration)
- **Location:** `~/.config/session-router/agents.json` (config file)
- **Updated:** `session_router.py` (TODO: integrate dynamic agents)

---

## See Also

- [SESSION_ROUTER.md](SESSION_ROUTER.md) - Task orchestration system
- [AGENTS.md](AGENTS.md) - Agent roles and routing
- [TESTING_LOG.md](TESTING_LOG.md) - Test results and findings
