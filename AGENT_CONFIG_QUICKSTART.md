# Agent Configuration Quick Start

Use this guide to quickly set up and test the agent configuration system.

---

## 1. Initialize Default Agents (30 seconds)

```bash
# Run the config tool to auto-create defaults
python3 ~/.github/scripts/agent_config_cli.py read-config

# Output shows:
# ✓ Created default config at ~/.config/session-router/agents.json
# Config file: /Users/ankit/.config/session-router/agents.json
# Enabled agents: 5/5
```

**That's it!** 5 agents are now configured and ready.

---

## 2. View Your Agents (1 minute)

```bash
# Option A: Interactive menu
~/.github/scripts/agent_config
# Choose: 1. List agents

# Option B: Command line
~/.github/scripts/agent_config list

# Shows:
# ID                   Name                      Cost       Status
# ════════════════════════════════════════════════════════════════════
# chatgpt              ChatGPT                   medium     ✓ Enabled
# claude-code          Claude (Code Interpreter) high       ✓ Enabled
# codex                Codex                     low        ✓ Enabled
# gemini               Gemini                    medium     ✓ Enabled
# perplexity           Perplexity                medium     ✓ Enabled
```

---

## 3. Add Your Own Agent (2 minutes)

```bash
~/.github/scripts/agent_config add

# Interactive prompts:
# Agent ID: my-custom-llm
# Display name: My Custom LLM
# Description: My personal LLM for planning
# Cost [free/low/medium/high]: free
# Specialties (comma-separated): planning, brainstorm
# Requires API key? (y/n) [n]: n
# Notes (optional): Test agent

# Result:
# ✓ Added agent 'my-custom-llm'
```

Now your custom agent is available to the router!

---

## 4. Manage Agents

### Enable/Disable (No Deletion)

```bash
# Disable an agent (keeps config, just marks inactive)
~/.github/scripts/agent_config disable chatgpt

# Enable it again
~/.github/scripts/agent_config enable chatgpt

# Agent stays in config, just toggled on/off
```

### Remove Agent

```bash
# Delete from config entirely
~/.github/scripts/agent_config remove my-custom-llm

# Will prompt for confirmation:
# Remove agent 'My Custom LLM'? (y/n): y
# ✓ Removed agent 'my-custom-llm'
```

### Test Agent

```bash
~/.github/scripts/agent_config test chatgpt

# Output:
# ✓ Agent 'ChatGPT' is available
# OR
# ⚠ Agent requires API key in CHATGPT_API_KEY
```

---

## 5. Budget Optimization (Real Example)

You only have **Codex API access** (low cost):

```bash
# Disable expensive agents
~/.github/scripts/agent_config disable chatgpt
~/.github/scripts/agent_config disable perplexity
~/.github/scripts/agent_config disable gemini

# Keep free/accessible ones
~/.github/scripts/agent_config enable claude-code  # free
~/.github/scripts/agent_config enable codex        # cheap

# Verify
~/.github/scripts/agent_config list

# Result: Only claude-code and codex are active
# Cost: $0 for this session
```

---

## 6. Export Configuration

```bash
# Save as JSON
~/.github/scripts/agent_config export > my_agents.json

# Share with team
cat my_agents.json | jq '.codex'

# Result: Full agent configuration ready to inspect
```

---

## 7. View Config File Directly

```bash
# Show entire config
cat ~/.config/session-router/agents.json | jq

# Show one agent
cat ~/.config/session-router/agents.json | jq '.claude-code'

# Show all specialties
cat ~/.config/session-router/agents.json | jq '.. | .specialties?' | sort -u

# Show enabled agents
cat ~/.config/session-router/agents.json | jq 'to_entries | .[] | select(.value.enabled) | .key'
```

---

## 8. Reset to Defaults

```bash
# Via interactive menu
~/.github/scripts/agent_config
# Choose: 8. Reset to defaults
# Confirm: y

# Or manually
rm ~/.config/session-router/agents.json
~/.github/scripts/agent_config_cli.py read-config

# Result: All 5 default agents restored
```

---

## Common Workflows

### Scenario A: "I have ChatGPT API access"

```bash
# Enable only ChatGPT
~/.github/scripts/agent_config disable claude-code
~/.github/scripts/agent_config disable codex
~/.github/scripts/agent_config disable perplexity
~/.github/scripts/agent_config disable gemini

~/.github/scripts/agent_config enable chatgpt

# Router now uses ChatGPT for everything
```

### Scenario B: "I want local-only agents"

```bash
# Disable all cloud agents
for agent in chatgpt perplexity gemini claude-code; do
  ~/.github/scripts/agent_config disable $agent
done

# Enable only local Codex
~/.github/scripts/agent_config enable codex

# Add local LLM
~/.github/scripts/agent_config add
# Agent ID: ollama
# Specialties: planning, brainstorm, architecture
# Cost: free
# API key required: n

# Result: Offline-only setup
```

### Scenario C: "I need research + coding capability"

```bash
# Ensure these are enabled
~/.github/scripts/agent_config enable perplexity   # for research
~/.github/scripts/agent_config enable claude-code  # for coding

# Disable planning/documentation agents if needed
~/.github/scripts/agent_config disable chatgpt
~/.github/scripts/agent_config disable codex

# Verify
~/.github/scripts/agent_config list
```

---

## Troubleshooting

### "Config file not found"

```bash
# Initialize it
~/.github/scripts/agent_config_cli.py read-config

# Or just run any command, it auto-creates if missing
```

### "Agent not available" error

```bash
# Test agent
~/.github/scripts/agent_config test <agent-id>

# Check if API key needed
echo $CHATGPT_API_KEY  # should not be empty

# If empty, set it
export CHATGPT_API_KEY="sk-..."
```

### "All agents disabled"

```bash
# You've accidentally disabled everything
# Re-enable at least one

~/.github/scripts/agent_config enable claude-code
~/.github/scripts/agent_config enable codex

# Or reset completely
rm ~/.config/session-router/agents.json
~/.github/scripts/agent_config_cli.py read-config
```

### Want to restore backup

```bash
# If you saved a backup:
cp my_agents.json ~/.config/session-router/agents.json

# Or reset and reconfigure
```

---

## Next Steps

Once you've configured your agents, the **session router** will use them automatically:

```bash
# Run session start
~/.github/scripts/session_start.sh

# It will:
# 1. Health check via log monitor
# 2. Load your agent config
# 3. Decompose tasks using available agents
# 4. Create prompts for each agent
# 5. Save session state
# 6. Output ready-to-use prompts
```

---

## Reference

- **Full guide:** [AGENT_CONFIGURATION.md](AGENT_CONFIGURATION.md)
- **Implementation details:** [AGENT_CONFIG_IMPLEMENTATION.md](AGENT_CONFIG_IMPLEMENTATION.md)
- **Session router:** [SESSION_ROUTER.md](SESSION_ROUTER.md)
- **Agent roles:** [AGENTS.md](AGENTS.md)

---

## Commands at a Glance

```bash
# Menu
~/.github/scripts/agent_config

# List
~/.github/scripts/agent_config list

# Add
~/.github/scripts/agent_config add

# Enable/Disable
~/.github/scripts/agent_config enable <id>
~/.github/scripts/agent_config disable <id>

# Remove
~/.github/scripts/agent_config remove <id>

# Test
~/.github/scripts/agent_config test <id>

# Export
~/.github/scripts/agent_config export

# Show config
~/.github/scripts/agent_config read-config

# Reset
rm ~/.config/session-router/agents.json
~/.github/scripts/agent_config_cli.py read-config
```

---

**That's it!** You now have a dynamic agent system. 🚀
