# Auto-Update Status via GitHub Gist

Simpler alternative to GitHub Actions. Updates a public gist that your site embeds.

## Setup

**1. Create GitHub Action to update gist:**

```yaml
name: Update Status Gist

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'

jobs:
  update-gist:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repos
        # ... same as before
        
      - name: Generate markdown status
        run: |
          cat > status.md << 'EOF'
          # Kit Lab Works - Live Status
          
          Updated: $(date)
          
          ## Currently Working On
          
          - Home Assistant: Update kitchen motion lights (Claude Code)
          - Data Scripts: Refactor pipeline (Codex)
          
          ## Recently Completed
          
          - ✅ Migrated to org-level coordination
          - ✅ Set up multi-agent workflow
          
          ## High Priority Backlog
          
          - Fix Tuya light naming (30 min)
          - Clean Music Assistant entities (15 min)
          EOF
          
      - name: Update gist
        uses: exuanbo/actions-deploy-gist@v1
        with:
          token: ${{ secrets.GIST_TOKEN }}
          gist_id: YOUR_GIST_ID
          file_path: status.md
```

**2. On kitlabworks.com:**

```html
<script src="https://gist.github.com/sasankaabey/YOUR_GIST_ID.js"></script>
```

**That's it!** GitHub embeds the gist with automatic styling.

## Pros/Cons

**GitHub Actions + JSON:**
- ✅ Full control over styling
- ✅ Can build complex UIs
- ✅ Fast (just fetch JSON)
- ❌ Need to host HTML/JS

**GitHub Gist:**
- ✅ Simplest possible
- ✅ GitHub handles hosting
- ✅ Can embed anywhere
- ❌ Limited styling control
- ❌ Looks like code (but that's fine!)

## Recommendation

**Start with Gist** (10 min setup)
→ If you want custom design later, migrate to JSON approach

Both auto-update on every commit. Zero ongoing work.
