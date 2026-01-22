# Specialized Tools Integration Guide

> Leverage your available tools (Canva AI, Adobe CC, Replit, n8n) alongside AI agents for complete workflow automation

---

## Overview

Your agent system now includes **9 agents total**: 5 AI agents + 4 specialized tools.

**New Tools Added:**
- **Canva AI** (Free tier) - Design & visual content
- **Adobe Creative Cloud Premium** - Professional media  
- **Replit** - Rapid prototyping & deployment
- **n8n Starter** - Workflow automation & integrations

This means tasks can now be routed to the **best-fit tool**, not just AI agents.

---

## Available Agents & Tools

### AI Agents (5)

| Agent | Cost | Primary Use | Specialties |
|-------|------|-------------|-------------|
| Claude Code | High | Server ops, debugging, SSH | server-ops, debugging, ssh, ha-deployment |
| Codex | Low | Documentation, YAML | documentation, yaml, formatting, review |
| ChatGPT | Medium | Planning, architecture | planning, architecture, review, brainstorm |
| Perplexity | Medium | Research, citations | research, docs, external-knowledge |
| Gemini | Medium | Analysis, summarization | analysis, summarization, large-docs |

### Specialized Tools (4)

| Tool | Cost | Primary Use | Specialties |
|------|------|-------------|-------------|
| Canva AI | **Free** | Design, graphics, visual content | design, graphics, visual-content, infographics, branding |
| Adobe CC | **Free** | Professional media editing | design, video-editing, photo-editing, publishing, animation |
| Replit | **Free** | Quick prototyping, deployment | prototyping, deployment, testing, collaboration, quick-dev |
| n8n | **Free** | Automation, workflows, integrations | automation, integration, workflow, api-connections, ha-automation |

---

## Use Cases by Tool

### Canva AI
Perfect for:
- Dashboard mockups for Home Assistant UI
- Social media graphics
- Infographics for documentation
- Quick branding materials
- Visual previews

**Example Task:**
```
Create a dashboard mockup for new Home Assistant lighting control panel
Assigned Agent: Canva AI
Output: PNG/PDF mockup, shareable Canva link
```

### Adobe Creative Cloud
Perfect for:
- Professional video tutorials
- Polished documentation graphics
- Photo editing for guides
- Animation for demos
- High-quality exports for presentations

**Example Task:**
```
Create a 5-minute video tutorial for Home Assistant automation setup
Assigned Agent: Adobe CC
Output: MP4 video, Adobe Cloud link
```

### Replit
Perfect for:
- Rapid prototyping of kitlabworks features
- Testing TypeScript/React changes
- Collaborative development
- Live deployment demos
- Quick scripts and POCs

**Example Task:**
```
Prototype new React component for task dashboard
Assigned Agent: Replit
Output: Live Replit URL, working component
```

### n8n Automation
Perfect for:
- Home Assistant complex automations
- Cross-system integrations
- Workflow orchestration
- API connections
- Scheduled tasks

**Example Task:**
```
Create n8n workflow for laundry notifications across Home Assistant, Slack, and mobile
Assigned Agent: n8n
Output: n8n workflow JSON, setup instructions
```

---

## Workflow Examples

### Example 1: Documentation with Visuals

**Task:** Create guide for new Home Assistant automation

**Decomposition:**
1. **Plan** (ChatGPT) - Structure and outline
2. **Write** (Codex) - Draft documentation
3. **Create visuals** (Canva AI) - Infographics & diagrams
4. **Video demo** (Adobe CC) - Screen recording tutorial
5. **Review** (ChatGPT) - Polish and verify
6. **Publish** (Adobe CC) - Final layout & export

**Benefits:**
- AI handles text, structure, review
- Creative tools handle visuals & video
- Result: Professional, multimedia documentation

### Example 2: kitlabworks Feature Development

**Task:** Build new dashboard component

**Decomposition:**
1. **Design** (ChatGPT/Canva AI) - UI mockup
2. **Prototype** (Replit) - Live component
3. **Refine** (Replit) - Collaborative iteration
4. **Testing** (Replit) - Live deployment test
5. **Code review** (Claude Code) - Production readiness
6. **Deploy** (Claude Code) - Push to production

**Benefits:**
- Replit enables rapid iteration
- No local setup needed
- Shareable, live testing URL
- Quick feedback loop

### Example 3: Complex Home Assistant Automation

**Task:** Set up laundry cycle tracking with multi-channel notifications

**Decomposition:**
1. **Design workflow** (ChatGPT) - Plan automation logic
2. **Create n8n flow** (n8n) - Multi-step automation
3. **HA integrations** (Claude Code) - Connect to Home Assistant
4. **Design alerts** (Canva AI) - Create notification templates
5. **Test** (Claude Code) - End-to-end validation
6. **Deploy** (Claude Code) - Push to production

**Benefits:**
- n8n handles complex orchestration
- Visual workflow builder reduces errors
- Cross-system integration simplified
- AI handles HA-specific details

### Example 4: Complete Project Launch

**Task:** Launch new feature with full documentation and demo

**Decomposition:**
1. **Research** (Perplexity) - Find best practices
2. **Architecture** (ChatGPT) - Design system
3. **Prototype** (Replit) - Build MVP
4. **Documentation** (Codex) - Write guides
5. **Visuals** (Canva AI) - Create diagrams & mockups
6. **Video** (Adobe CC) - Record tutorial
7. **Automation** (n8n) - Set up deployment workflow
8. **Review & Deploy** (Claude Code) - Final validation & go-live

**Result:** Professional launch with documentation, video, automation

---

## Task Assignment Logic

When session router receives a task, it considers:

```
Task Type → Best-fit Tool Selection

"Design dashboard"
  → Specialty: "design"
  → Best agents: Canva AI, Adobe CC
  → Choose: Canva AI (faster, free)

"Create video tutorial"
  → Specialty: "video-editing"
  → Best agents: Adobe CC
  → Choose: Adobe CC (required)

"Build component"
  → Specialty: "prototyping"
  → Best agents: Replit, Claude Code
  → Choose: Replit (collaborative, live)

"Complex HA workflow"
  → Specialty: "automation"
  → Best agents: n8n, Claude Code
  → Choose: n8n (workflow builder)

"Write documentation"
  → Specialty: "documentation"
  → Best agents: Codex, ChatGPT
  → Choose: Codex (low cost)
```

---

## Managing Tool Access

### View All Tools

```bash
agent_config list
```

Output shows all 9 agents including tools with FREE cost.

### Disable a Tool (if temporarily unavailable)

```bash
# Adobe subscription expired?
agent_config disable adobe-cc

# n8n plan ended?
agent_config disable n8n

# Re-enable when back
agent_config enable adobe-cc
```

### Add Custom Tool

```bash
agent_config add

# Example: Add Figma if you get it
# Agent ID: figma
# Name: Figma
# Description: Collaborative design and prototyping
# Cost: free
# Specialties: design, prototyping, collaboration
# API key required: n
# Notes: Available with Pro plan
```

---

## Integration with Session Router

### Current (Phase 2)

When session router decomposes tasks:

```python
# OLD: Hard-coded agents
subtask = Subtask(
    agent=AgentType.CODEX,  # Always Codex for docs
)

# NEW: Dynamic specialty routing
subtask = Subtask(
    agent=config.get_agent_by_specialty("design"),  # Could be Canva, Adobe, etc.
)
```

### Coming (Phase 2 Integration)

Session router will automatically select:
- **Canva AI** for "design" tasks
- **Adobe CC** for "video-editing" or "photo-editing"
- **Replit** for "prototyping" tasks
- **n8n** for "automation" or "integration" tasks
- **AI agents** for traditional coding/writing

---

## Specialty Reference

### New Specialties (From Tools)

**Design & Visual:**
- `design` - General design work
- `graphics` - Graphics creation
- `visual-content` - Visual asset creation
- `infographics` - Data visualization
- `branding` - Brand/logo work
- `video-editing` - Video post-production
- `photo-editing` - Photo manipulation
- `animation` - Motion graphics

**Automation & Integration:**
- `automation` - Workflow automation
- `integration` - System integration
- `workflow` - Process automation
- `api-connections` - API integration
- `ha-automation` - Home Assistant automations

**Development & Prototyping:**
- `prototyping` - Quick prototyping
- `deployment` - Live deployment
- `collaboration` - Collaborative work
- `quick-dev` - Fast development

---

## Budget Optimization Scenarios

### Scenario 1: Maximum Quality (Use All)

```bash
# Keep everything enabled
agent_config enable adobe-cc canva-ai replit n8n
agent_config enable chatgpt perplexity gemini claude-code codex

# Use best tool for each task
# Cost: All premium/free tiers active
# Quality: Maximum
```

### Scenario 2: Free Tools Only

```bash
# Disable paid AI agents
agent_config disable chatgpt perplexity gemini claude-code

# Keep free tools + low-cost Codex
agent_config enable canva-ai adobe-cc replit n8n codex

# Use: Codex for AI work, tools for specialties
# Cost: $0 (everything free or owned)
# Quality: Good, limited by Codex alone
```

### Scenario 3: Fast Development Focus

```bash
# Optimize for kitlabworks development
agent_config enable replit claude-code codex
agent_config disable canva-ai adobe-cc gemini  # Not needed for backend work

# Use: Claude Code + Replit for dev
# Cost: Low (mostly free)
# Speed: Maximum (Replit collaboration)
```

### Scenario 4: Home Automation Focus

```bash
# Optimize for Home Assistant
agent_config enable n8n claude-code canva-ai
agent_config disable chatgpt perplexity gemini  # Less useful for HA

# Use: Claude for HA specifics, n8n for workflows, Canva for dashboards
# Cost: Low (free tools dominate)
# Focus: Home automation excellence
```

---

## Workflow Examples with Tools

### Example: Create HA Dashboard + Automation

```
Task: "Redesign laundry dashboard with new automation notifications"

Decomposition:
1. Design dashboard mockup
   Agent: Canva AI
   Output: Interactive mockup, shareable link
   
2. Create automation workflow
   Agent: n8n
   Output: n8n workflow, setup guide
   
3. Write YAML config
   Agent: Codex
   Output: automation_laundry_notifications.yaml
   
4. Test end-to-end
   Agent: Claude Code
   Output: Tested, deployed to HA
   
5. Create video tutorial
   Agent: Adobe CC
   Output: 2-minute demo video
   
6. Document everything
   Agent: Codex
   Output: README with all assets linked

Total time: ~3-4 hours (parallel where possible)
Quality: Professional, documented, tested
Cost: ~$5 (mostly free, slight ChatGPT if planning needed)
```

---

## Tips for Best Results

### 1. **Use Tools for Their Strengths**

- Canva: Fast iteration, visual design, no coding
- Adobe: Professional output, complex editing, high quality
- Replit: Live collaboration, instant deployment, feedback
- n8n: Visual automation, complex logic, integrations

### 2. **Combine Tools + AI**

- Use Canva to design, Claude to review/refine
- Use Replit to prototype, Codex to document
- Use n8n to automate, Claude to debug

### 3. **Leverage Replit for Quick Feedback**

Instead of local development:
```
1. Write code locally
2. Push to Replit
3. Share shareable URL
4. Get live feedback
5. Iterate instantly
```

### 4. **Use n8n for HA Workflows**

Instead of complex YAML:
```
1. Design workflow in n8n visual editor
2. Test with live HA connection
3. Export as JSON
4. Document in GitHub
5. Deploy with Claude Code
```

### 5. **Create Asset Libraries**

- Canva: Design templates for dashboards
- Adobe: Video templates for tutorials
- n8n: Workflow templates for automations
- Replit: Component templates for kitlabworks

---

## Next Steps

### Phase 2 (This Week)
- [ ] Integrate tool specialties into session router
- [ ] Test task assignment with Canva, Adobe, Replit, n8n
- [ ] Create example workflows using tools

### Phase 3 (Next Month)
- [ ] GitHub Issues integration (tools as assignees)
- [ ] Performance tracking per tool
- [ ] Cost dashboard showing tool usage

### Long-term Ideas
- Auto-detect which tools to use based on task type
- Create task templates for common workflows
- Build asset library across all tools
- Integrate tool outputs into documentation

---

## See Also

- [AGENT_CONFIGURATION.md](AGENT_CONFIGURATION.md) - Full agent management guide
- [SESSION_ROUTER.md](SESSION_ROUTER.md) - Task routing system
- [SYSTEM_COMPLETE.md](SYSTEM_COMPLETE.md) - Complete system overview

---

## Tool Access & Verification

All tools are **currently active and available**:

| Tool | Status | Expires | Access |
|------|--------|---------|--------|
| Canva AI | ✅ Active | — | canva.com |
| Adobe CC Premium | ✅ Active | — | adobe.com |
| Replit | ✅ Active | — | replit.com |
| n8n Starter | ✅ Active | 1 year | n8n.cloud |

To verify tool access:
```bash
agent_config test canva-ai
agent_config test adobe-cc
agent_config test replit
agent_config test n8n
```

---

**You now have a complete toolkit combining AI agents with specialized professional tools.** 🎨🚀🤖
