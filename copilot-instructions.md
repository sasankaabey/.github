# Copilot Instructions for Sasankaabey Workspace

## Workspace Overview

This is a **multi-project VS Code workspace** containing three distinct projects managed with a centralized **multi-agent coordination system**:

1. **home-assistant-config** - Smart home automation configuration (YAML/Python)
2. **kitlabworks** - Full-stack TypeScript web application (React + Express + Drizzle)
3. **headache-tracker** - Minimal project (limited context available)

**Key Architectural Principle:** Process and workflows are centralized in `.github/`, while project-specific context lives in each project's root.

## Multi-Agent Architecture

### Agent Roles & Task Distribution

Work is distributed across different AI agents based on capability and cost optimization:

| Agent | Primary Use Cases | Files to Reference |
|-------|------------------|-------------------|
| **Claude Code/Copilot** | Server ops, SSH, debugging, complex code, entity registry edits | `.github/copilot-instructions.md` (this file) |
| **Codex** | Documentation, YAML drafting, linting, refactoring | `LOCAL_CONTEXT.md`, `HOME_ASSISTANT.md` |
| **ChatGPT** | Planning, quick questions, agent coordination | `.github/AGENTS.md` |
| **Perplexity** | Research, finding docs/solutions | `DECISIONS.md` |
| **Gemini/NotebookLM** | Large document analysis, summarization | Project audit reports |

**Decision Tree:** See [AGENTS.md](AGENTS.md#decision-tree-for-task-routing)

### Coordination Mechanism

**Not** chat-based handoffs. Instead:
- Tasks tracked in each project's `TASKS.md`
- Handoffs via git commits with detailed messages
- Context preserved in markdown docs, not conversation history

**Workflow Process:** See [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)

## Project 1: home-assistant-config

Smart home configuration for a 5-person household with extensive automation.

### Critical Context Files
- `LOCAL_CONTEXT.md` - Project overview and conventions
- `home-assistant-config/.github/copilot-instructions.md` - Detailed HA-specific instructions
- `DECISIONS.md` - Architecture decisions
- `TASKS.md` - Current work queue

### Architecture

**Deployment Model:**
- Local dev: `/Users/ankit/Developer/sasankaabey/home-assistant-config`
- Production: `192.168.4.141:/config` (HA OS on minipc)
- Sync: `./sync_to_ha.sh` → restart HA

**Key Directories:**
```
configuration.yaml       # Core config (rarely edit)
automations/            # Manual YAML automations by category
  lighting/            # Motion sensors, schedules
  litterbot/          # Pet automation
light_groups.yaml       # YAML-based groups (NOT UI groups)
inputs/                # Helper entities (input_select, etc.)
custom_components/     # 23+ custom integrations
```

### Critical Patterns

**Entity Naming Convention:**
```
[domain].[location]_[description]
```
Examples: `light.living_room_ceiling`, `sensor.kitchen_temperature`

**Light Groups Pattern:**
- Defined in `light_groups.yaml` using `platform: group`
- **Never** use UI groups (not version controlled)
- Entity IDs must match `.storage/core.entity_registry` exactly
- Require HA restart to apply changes

**Entity Registry Edits:**
```bash
# CRITICAL: Use stop + start, NOT restart
ha core stop
# Edit .storage/core.entity_registry
ha core start  # NOT "ha core restart" - overwrites uncommitted changes
```

**Deployment Workflow:**
```bash
# Validate locally
python3 -c "import yaml; yaml.safe_load(open('automations/file.yaml'))"

# Sync to server
./sync_to_ha.sh

# Restart HA (via UI or SSH)
ssh root@192.168.4.141 'ha core restart'

# Test & commit if successful
```

### Common Issues

**Light group unavailable:** Entity IDs in `light_groups.yaml` don't match registry. Check `.storage/core.entity_registry` on server.

**Notify group fails:** Service names (e.g., `mobile_app_ankit_s_iphone`) are slugified device names. Verify in `Configuration → Integrations`.

**Custom component patches lost:** Document in `CHANGELOG.md`, may need to reapply after updates.

## Project 2: kitlabworks

Full-stack TypeScript web application using modern tooling.

### Tech Stack
- **Frontend:** React 19, Vite, TanStack Query, Wouter (routing), shadcn/ui components
- **Backend:** Express 5, TypeScript (ESM), WebSocket support
- **Database:** PostgreSQL + Drizzle ORM
- **Styling:** Tailwind CSS v4, Radix UI primitives
- **Auth:** Passport (local strategy), express-session

### Architecture

**Monorepo Structure:**
```
client/                 # Frontend source
  src/
    components/        # React components
      ui/             # shadcn/ui components
    pages/           # Route pages
    lib/             # Utilities, query client
server/                # Backend source
  index.ts           # Express app, middleware
  routes.ts          # API route definitions
  storage.ts         # Data access interface
  vite.ts            # Dev mode Vite integration
shared/
  schema.ts          # Drizzle schema + Zod types (SSOT)
script/
  build.ts           # Production build script
```

**Path Aliases:**
- `@/*` → `client/src/*`
- `@shared/*` → `shared/*`
- `@assets/*` → `attached_assets/*`

### Development Workflow

**Local Development:**
```bash
npm run dev         # Starts Express server with Vite middleware (port 5000)
npm run dev:client  # Vite dev server only (port 5000)
npm run check       # TypeScript type checking
npm run db:push     # Push schema changes to PostgreSQL
```

**Production Build:**
```bash
npm run build       # Vites client → dist/public, esbuild server → dist/index.cjs
npm start          # NODE_ENV=production node dist/index.cjs
```

### Critical Patterns

**Shared Type Safety:**
- Database schema lives in `shared/schema.ts`
- Uses `drizzle-zod` to generate Zod schemas from Drizzle tables
- Export both DB types and Zod insert schemas:
  ```typescript
  export const users = pgTable("users", { ... });
  export const insertUserSchema = createInsertSchema(users);
  export type User = typeof users.$inferSelect;
  export type InsertUser = z.infer<typeof insertUserSchema>;
  ```

**Storage Interface Pattern:**
- `server/storage.ts` defines `IStorage` interface
- Current implementation: `MemStorage` (in-memory)
- Production: Switch to Drizzle-backed implementation
- Routes use `storage` export, not direct DB calls

**Component Structure:**
- UI components in `client/src/components/ui/` (shadcn/ui)
- Feature components in `client/src/components/`
- Configured via `components.json` (shadcn CLI config)

**Build Optimization:**
- `script/build.ts` bundles select server deps to reduce cold start time
- Allowlist in build script controls bundling (e.g., drizzle-orm, zod, pg)
- All other deps externalized

### Development Notes

**Port Configuration:**
- Always use port from `process.env.PORT` (default: 5000)
- Other ports are firewalled in production environment
- Single port serves both API and client

**WebSocket Support:**
- HTTP server created via `createServer(app)`
- Pass `httpServer` to `registerRoutes` for WS upgrade support

**Environment Variables:**
- `DATABASE_URL` required for Drizzle operations
- `NODE_ENV` controls dev vs prod mode (Vite vs static serving)
- `REPL_ID` enables Replit-specific plugins

## Project 3: headache-tracker

Minimal project with limited documentation. Appears to be in early stages.

## Workspace-Wide Conventions

### Documentation Structure

**Organization-Level (`.github/`):**
- `AGENTS.md` - Agent roles and routing
- `MULTI_AGENT_WORKFLOW.md` - Step-by-step workflow process
- `EVOLUTION_LOG.md` - What we learned and improved
- `PATTERNS/` - Reusable templates for new repos

**Project-Level (each project root):**
- `LOCAL_CONTEXT.md` - "What is this project?"
- `TASKS.md` - Current work queue
- `CHANGELOG.md` - User-facing changes
- `DECISIONS.md` - Project-specific architecture decisions

### Task Management

**Before starting work:**
1. Read `LOCAL_CONTEXT.md` (2 min)
2. Check `TASKS.md` for assignment
3. Reference `.github/AGENTS.md` to confirm your role

**During work:**
- Commit every 30-90 minutes with descriptive messages
- Update `TASKS.md` progress checkboxes
- Use commit message format: `"Task: [Name] - [Checkpoint]"`

**After completing:**
- Update `TASKS.md` status to "Complete"
- Document in `CHANGELOG.md` (user-facing changes)
- Record decisions in `DECISIONS.md` (architecture choices)

### Git Workflow

**Commit Message Patterns:**
```
Task: [Task Name] - [What was done]
Setup: [What was initialized]
Fix: [What was broken and how it was fixed]
Docs: [Documentation updates]
Cleanup: [Code organization/refactoring]
```

**Multi-file changes:** Use descriptive commit message with context for next agent/session.

## Best Practices

### Context Preservation
- **Don't rely on chat history** - document in markdown files
- **Use git commits as context** - next agent reads `git log` for understanding
- **Update TASKS.md frequently** - it's the coordination hub

### Cost Optimization
- Use fast/cheap agents (Codex, ChatGPT) for drafting
- Reserve expensive agents (Claude Code) for critical operations
- Batch server operations to reduce SSH sessions and restarts

### Agent Handoffs
When handing off to another agent:
1. Commit all work with detailed message
2. Update `TASKS.md` with what's done and what's next
3. Specify which agent should continue: `**Agent:** Claude Code (next)`

### File Organization
- Keep project-specific code in project directories
- Share patterns/templates via `.github/PATTERNS/`
- Never duplicate org-level docs into projects

## Resources

- **HA Docs:** https://www.home-assistant.io/docs/
- **Drizzle Docs:** https://orm.drizzle.team/
- **shadcn/ui:** https://ui.shadcn.com/
- **Org Workflow:** See `.github/MULTI_AGENT_WORKFLOW.md`
