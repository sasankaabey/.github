#!/bin/bash
# Session Start: Health check + Task routing for multi-agent workflows
#
# Usage:
#   ./session_start.sh              # Interactive: Show backlog, select task
#   ./session_start.sh --next       # Auto-continue last task
#   ./session_start.sh --last       # Re-show last task prompt
#   ./session_start.sh --health     # Just run health check (old behavior)

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HA_PROJECT="$WORKSPACE_ROOT/home-assistant-config"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Parse args
MODE="interactive"
LOG_MONITOR_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --next)
            MODE="next"
            shift
            ;;
        --last)
            MODE="last"
            shift
            ;;
        --health)
            MODE="health_only"
            shift
            ;;
        *)
            # Pass through to log monitor
            LOG_MONITOR_ARGS+=("$1")
            shift
            ;;
    esac
done

# ============================================================================
# Phase 1: System Health Check (Log Monitor)
# ============================================================================

echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}${BOLD}🔍 Phase 1: System Health Check${NC}"
echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run log monitor (dry-run to avoid modifying TASKS.md yet)
if [ "$MODE" = "health_only" ]; then
    # Full health check
    python3 "$SCRIPT_DIR/log_monitor.py" \
        --project-path "$HA_PROJECT" \
        "${LOG_MONITOR_ARGS[@]}"
else
    # Quick dry-run
    python3 "$SCRIPT_DIR/log_monitor.py" \
        --project-path "$HA_PROJECT" \
        --dry-run \
        "${LOG_MONITOR_ARGS[@]}"
fi

HEALTH_EXIT_CODE=$?

echo ""

# Interpret health check
if [ $HEALTH_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ System healthy - no critical issues detected${NC}"
elif [ $HEALTH_EXIT_CODE -eq 1 ]; then
    echo -e "${YELLOW}⚠️  High priority issues detected - may affect work${NC}"
elif [ $HEALTH_EXIT_CODE -eq 2 ]; then
    echo -e "${RED}🚨 CRITICAL issues found - recommend fixing before proceeding${NC}"
    echo -e "${RED}   Run './session_start.sh --health' for details${NC}"
fi

echo ""

# If health-only mode, stop here
if [ "$MODE" = "health_only" ]; then
    exit $HEALTH_EXIT_CODE
fi

# ============================================================================
# Phase 2: Task Routing (Session Router)
# ============================================================================

echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}${BOLD}🎯 Phase 2: Task Selection & Agent Routing${NC}"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run session router based on mode
cd "$WORKSPACE_ROOT"

if [ "$MODE" = "next" ]; then
    python3 "$SCRIPT_DIR/session_router.py" --next
elif [ "$MODE" = "last" ]; then
    python3 "$SCRIPT_DIR/session_router.py" --last
else
    # Interactive mode
    python3 "$SCRIPT_DIR/session_router.py"
fi

ROUTER_EXIT_CODE=$?

# ============================================================================
# Summary
# ============================================================================

echo ""
echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}${BOLD}📋 Session Summary${NC}"
echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $HEALTH_EXIT_CODE -eq 0 ]; then
    echo -e "  System Health: ${GREEN}✅ OK${NC}"
else
    echo -e "  System Health: ${YELLOW}⚠️  Issues Found${NC}"
fi

if [ $ROUTER_EXIT_CODE -eq 0 ]; then
    echo -e "  Task Selected: ${GREEN}✅ Prompt Generated${NC}"
else
    echo -e "  Task Selected: ${RED}❌ No task selected${NC}"
fi

echo ""
echo -e "${CYAN}💡 Next Steps:${NC}"
echo -e "   1. Copy the prompt above"
echo -e "   2. Paste into the assigned agent (Claude, Codex, etc.)"
echo -e "   3. When done, run: ${BOLD}./session_start.sh --next${NC}"
echo ""

exit $ROUTER_EXIT_CODE
