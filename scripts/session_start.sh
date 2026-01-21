#!/bin/bash
# Session Start Wrapper - Automatically runs Log Monitor Agent

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
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Home Assistant Session Start${NC}"
echo -e "${BLUE}================================${NC}\n"

# Check if HA project exists
if [ ! -d "$HA_PROJECT" ]; then
    echo -e "${RED}❌ Home Assistant project not found at: $HA_PROJECT${NC}"
    exit 1
fi

# Run log monitor
echo -e "${YELLOW}Running Log Monitor Agent...${NC}\n"

python3 "$SCRIPT_DIR/log_monitor.py" \
    --project-path "$HA_PROJECT" \
    "$@"

EXIT_CODE=$?

echo ""
echo -e "${BLUE}================================${NC}"

# Interpret exit code
if [ $EXIT_CODE -eq 2 ]; then
    echo -e "${RED}🚨 CRITICAL issues detected - immediate attention required${NC}"
    exit 2
elif [ $EXIT_CODE -eq 1 ]; then
    echo -e "${YELLOW}⚠️  HIGH priority issues detected - review TASKS.md${NC}"
    exit 1
elif [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Session analysis complete - system healthy${NC}"
    exit 0
else
    echo -e "${RED}❌ Log monitor failed${NC}"
    exit $EXIT_CODE
fi
