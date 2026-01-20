# Evolution Log

This document tracks improvements, learnings, and pattern evolution across all projects in the sasankaabey organization.

---

## Purpose

**What is this?**
A living record of what we learned from building products across multiple repos, and how the multi-agent workflow improved over time.

**Why track this?**
- Capture improvements so they benefit all future work
- Make workflow evolution transparent
- Help agents learn from past experiences
- Avoid repeating mistakes across repos

---

## Format

```markdown
### [Date] - [Improvement Title]

**Context:** What prompted this change?
**What Changed:** What's different now?
**Impact:** How does this help?
**Applies To:** [Agent/Process/Tool]
**Updated:** [Which docs were changed]
```

---

## Entries

### 2026-01-20 - Multi-Agent Coordination System Created

**Context:** 
Needed a way to distribute work across multiple AI agents (Codex, Claude, ChatGPT, Perplexity, Gemini, Haiku) while keeping costs optimized and context relevant.

**What Changed:**
- Created role-based agent distribution model
- Established git-based handoff coordination
- Documented workflow in MULTI_AGENT_WORKFLOW.md
- Created AGENTS.md decision tree for task routing

**Impact:**
- Agents know which tasks to handle
- Clear handoff process reduces friction
- Cost optimization through agent specialization
- Context stays focused and relevant

**Applies To:** All agents, all repos

**Updated:** 
- Created AGENTS.md
- Created MULTI_AGENT_WORKFLOW.md
- Created MULTI_AGENT_ARCHITECTURE.md

---

### 2026-01-20 - Hybrid Centralized-Local Model Adopted

**Context:**
Initial setup was repo-specific. Needed to scale to multiple repos while minimizing maintenance overhead.

**What Changed:**
- Moved coordination docs to org/.github (centralized)
- Each repo has LOCAL_CONTEXT.md (project-specific info)
- Each repo has TASKS.md (local task queue)
- All repos reference org/.github for process

**Impact:**
- Update workflow once → applies to all repos
- Zero ongoing maintenance per repo
- New repos can be created in ~5 minutes
- Process improvements captured globally

**Applies To:** Repository architecture, documentation structure

**Updated:**
- Created org/.github repository structure
- Created EVOLUTION_LOG.md (this file)
- Added PATTERNS/NEW_REPO_TEMPLATE

---

## Templates for New Entries

### Bug Fix Pattern
```markdown
### [Date] - [Bug Description Fixed]

**Context:** What was breaking and why?
**Solution:** How was it fixed?
**Prevention:** How to avoid this in the future?
**Applies To:** [Affected repos/components]
**Updated:** [Documentation changes]
```

### Process Improvement
```markdown
### [Date] - [Process Improved]

**Old Way:** How it used to work
**New Way:** How it works now
**Why Better:** Benefits of the change
**Applies To:** [Which agents/steps]
**Updated:** [Which docs]
```

### New Pattern Discovered
```markdown
### [Date] - [Pattern Name]

**Context:** What problem does this solve?
**Pattern:** How to implement it
**Example:** Link to first usage
**Applies To:** [When to use this]
**Added To:** PATTERNS/[filename]
```

### Cost Optimization
```markdown
### [Date] - [Optimization Description]

**Before:** Previous approach and cost
**After:** New approach and savings
**Impact:** How much saved / faster
**Applies To:** [Which agent/operation]
**Updated:** [Documentation]
```

---

## Contributing

**When to add an entry:**
- You discover a better way to do something
- You fix a recurring bug
- You optimize a workflow step
- You create a reusable pattern
- You learn something non-obvious

**How to add an entry:**
1. Use one of the templates above
2. Be specific about what changed
3. Link to relevant commits or files
4. Update affected documentation
5. Commit with message: `Docs: Evolution - [Title]`

---

## Statistics

**Total Improvements:** 2
**Last Updated:** 2026-01-20
**Repos Affected:** All (via org/.github)

---

**This log grows with every improvement. Check it regularly to learn from past experiences.**
