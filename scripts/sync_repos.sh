#!/usr/bin/env bash
set -euo pipefail

# Sync all GitHub repositories for a user/org into a single parent folder
# and regenerate the VS Code multi-root workspace file so all repos are always loaded.
#
# Environment overrides:
#   ORG                GitHub user/org to sync (default: sasankaabey)
#   BASE_DIR           Where to place the repos (default: /workspaces or parent of this script)
#   WORKSPACE_FILE     Path to the .code-workspace file (default: $BASE_DIR/sasankaabey.code-workspace)
#   INCLUDE_ARCHIVED   If "true", also sync archived repos (default: false)

ORG="${ORG:-sasankaabey}"

# Auto-detect base directory: use /workspaces in devcontainer, sasankaabey folder elsewhere
if [ -w /workspaces 2>/dev/null ]; then
  BASE_DIR="${BASE_DIR:-/workspaces}"
else
  # Find the sasankaabey folder that contains .github
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  GITHUB_DIR="$(dirname "$SCRIPT_DIR")"
  PARENT_DIR="$(dirname "$GITHUB_DIR")"
  
  # Check if parent is named sasankaabey, if not use parent of .github
  if [ "$(basename "$PARENT_DIR")" = "sasankaabey" ]; then
    BASE_DIR="${BASE_DIR:-$PARENT_DIR}"
  else
    BASE_DIR="${BASE_DIR:-$PARENT_DIR}"
  fi
fi

WORKSPACE_FILE="${WORKSPACE_FILE:-$BASE_DIR/sasankaabey.code-workspace}"
INCLUDE_ARCHIVED="${INCLUDE_ARCHIVED:-false}"

command -v gh >/dev/null 2>&1 || {
  echo "[sync] gh CLI is required; install GitHub CLI first" >&2
  exit 1
}

command -v git >/dev/null 2>&1 || {
  echo "[sync] git is required; install git first" >&2
  exit 1
}

mkdir -p "$BASE_DIR"

echo "[sync] Listing repos for $ORG ..."
REPOS_JSON="$(gh repo list "$ORG" --limit 200 --json name,sshUrl,isArchived)"

REPOS_TMP=$(REPOS_JSON="$REPOS_JSON" INCLUDE_ARCHIVED="$INCLUDE_ARCHIVED" python3 - <<'PY'
import json, os

data = json.loads(os.environ["REPOS_JSON"])
include_archived = os.environ.get("INCLUDE_ARCHIVED", "false").lower() == "true"

for repo in data:
    if repo.get("isArchived") and not include_archived:
        continue
    # Use the name (e.g., "sasankaabey/kitlabworks") for gh clone
    full_name = f"{repo['owner']['login']}/{repo['name']}"
    print(f"{repo['name']}\t{full_name}")
PY
)

paths=""

while IFS=$'\t' read -r name full_name; do
  [ -z "$name" ] && continue
  target="$BASE_DIR/$name"

  if [ -d "$target/.git" ]; then
    echo "[sync] Updating $name ..."
    git -C "$target" fetch --prune
    git -C "$target" pull --ff-only
  else
    echo "[sync] Cloning $name ..."
    if gh repo clone "$full_name" "$target" 2>&1; then
      :  # Success, continue
    else
      echo "[sync] ⚠️  Failed to clone $name (skipping)"
      continue
    fi
  fi

  paths="$paths
$target"
done <<< "$REPOS_TMP"

# Ensure deterministic ordering and uniqueness
SORTED_PATHS=$(printf "%s" "$paths" | grep -v '^$' | sort -u)

printf "%s" "$SORTED_PATHS" | python3 - "$WORKSPACE_FILE" <<'PY'
import json, sys

paths = [line.strip() for line in sys.stdin if line.strip()]
outfile = sys.argv[1]

data = {
    "folders": [{"path": p} for p in paths],
    "settings": {}
}

with open(outfile, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(f"[sync] Workspace updated -> {outfile}")
PY

echo "[sync] Done. Reopen the workspace file if VS Code is already open to reload folders."
