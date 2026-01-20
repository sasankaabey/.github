# Reusable Patterns & Templates

This directory contains templates and patterns for common tasks across sasankaabey repos.

## Available Templates

### For New Repos

| Template | Purpose | Time to Customize |
|----------|---------|-------------------|
| [NEW_REPO_TEMPLATE/LOCAL_CONTEXT_TEMPLATE.md](NEW_REPO_TEMPLATE/LOCAL_CONTEXT_TEMPLATE.md) | Project overview and conventions | 10 min |
| [NEW_REPO_TEMPLATE/TASKS_TEMPLATE.md](NEW_REPO_TEMPLATE/TASKS_TEMPLATE.md) | Task queue structure | 2 min |
| [NEW_REPO_SETUP_GUIDE.md](NEW_REPO_SETUP_GUIDE.md) | Step-by-step new repo setup | 15 min total |

### Usage

**Setting up a new repo:**

```bash
# 1. Clone the new repo
git clone git@github.com:sasankaabey/[repo-name].git
cd [repo-name]

# 2. Copy templates
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/LOCAL_CONTEXT_TEMPLATE.md ./LOCAL_CONTEXT.md
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/TASKS_TEMPLATE.md ./TASKS.md

# 3. Customize LOCAL_CONTEXT.md (10 min)
code LOCAL_CONTEXT.md

# 4. Add initial tasks to TASKS.md
code TASKS.md

# 5. Commit and push
git add .
git commit -m "Setup: Initialize multi-agent coordination"
git push origin main
```

See [NEW_REPO_SETUP_GUIDE.md](NEW_REPO_SETUP_GUIDE.md) for complete instructions.

## Adding New Patterns

When you discover a reusable pattern or solution:

1. **Create a template** in this directory (e.g., `DEPLOYMENT_CHECKLIST_TEMPLATE.md`)
2. **Document usage** by adding an entry to this README
3. **Log the discovery** in [../EVOLUTION_LOG.md](../EVOLUTION_LOG.md)
4. **Commit to org/.github** so all repos benefit

### Template Creation Guidelines

**Good templates are:**
- ✅ **Generic** — Works across multiple projects
- ✅ **Documented** — Clear instructions for customization
- ✅ **Time-bounded** — "5 min to customize" helps adoption
- ✅ **Practical** — Solves real recurring needs

**Examples of patterns to capture:**
- Deployment checklists
- PR templates
- Issue templates
- CI/CD config snippets
- Security review checklists
- Architecture decision record (ADR) templates

## Pattern Format

Use this structure for new pattern templates:

```markdown
# [Pattern Name]

**Purpose:** One-sentence description

**When to Use:** Specific scenario or trigger

**Time to Apply:** ~X minutes

---

## Template

[Your template content here]

---

## Customization Guide

**Required changes:**
1. [What must be customized]
2. [What must be customized]

**Optional changes:**
- [What might be customized]

---

## Example

[Show a filled-in example]
```

## Contributing Improvements

Found a better way? Update the pattern and document in EVOLUTION_LOG.md:

```bash
# 1. Edit the template
code PATTERNS/[TEMPLATE_NAME].md

# 2. Document the improvement
echo "## YYYY-MM-DD - Improved [Pattern Name]

**Problem:** [What was wrong]

**Solution:** [What you changed]

**Impact:** All future repos using this template benefit

**By:** [Your name/agent]" >> ../EVOLUTION_LOG.md

# 3. Commit
git add PATTERNS/ ../EVOLUTION_LOG.md
git commit -m "Pattern: Improve [template name] - [brief description]"
git push origin main
```

Now all future repos benefit from your improvement!

## Pattern Discovery Process

1. **Work on a project** → Encounter a recurring need
2. **Solve it once** → Create solution for your repo
3. **Generalize it** → Extract project-specific details
4. **Template it** → Add to PATTERNS/
5. **Document it** → Update this README + EVOLUTION_LOG.md
6. **Share it** → All repos benefit

## Questions?

- **How do I know if something should be a pattern?** — If you've used it twice, it's worth templating.
- **Should I make templates for project-specific stuff?** — No, keep those in your repo's LOCAL_CONTEXT.md
- **What if a pattern needs major changes?** — Update it here, document in EVOLUTION_LOG.md, all repos benefit
- **Can I have private patterns?** — Yes, add `.private/` to .gitignore in your repo

## Current Gaps

Patterns we should add (contributions welcome):

- [ ] Deployment checklist template
- [ ] CI/CD workflow snippets
- [ ] PR template
- [ ] Issue templates (bug, feature, question)
- [ ] Security review checklist
- [ ] Architecture decision record (ADR) template
- [ ] Monitoring/alerting setup guide
- [ ] Database migration checklist

Add yours by creating the template and updating this list!
