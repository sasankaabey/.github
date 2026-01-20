#!/usr/bin/env bash
set -euo pipefail

# Sync all GitHub repositories for a user/org into a single parent folder
# and regenerate the VS Code multi-root workspace file so all repos are always loaded.
#
# Environment overrides:
#   ORG                GitHub user/org to sync (default: sasankaabey)
#   BASE_DIR           Where to place the repos (default: /workspaces)
#   WORKSPACE_FILE     Path to the .code-workspace file (default: $BASE_DIR/sasankaabey.code-workspace)
#   INCLUDE_ARCHIVED   If "true", also sync archived repos (default: false)

ORG="${ORG:-sasankaabey}"
BASE_DIR="${BASE_DIR:-/workspaces}"
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

mapfile -t REPOS < <(REPOS_JSON="$REPOS_JSON" INCLUDE_ARCHIVED="$INCLUDE_ARCHIVED" python3 - <<'PY'
import json, os

data = json.loads(os.environ["REPOS_JSON"])
include_archived = os.environ.get("INCLUDE_ARCHIVED", "false").lower() == "true"

for repo in data:
  if repo.get("isArchived") and not include_archived:
    continue
  print(f"{repo['name']}\t{repo['sshUrl']}")
PY
)

paths=()

for line in "${REPOS[@]}"; do
  name="${line%%$'\t'*}"
  url="${line#*$'\t'}"
  target="$BASE_DIR/$name"

  if [ -d "$target/.git" ]; then
    echo "[sync] Updating $name ..."
    git -C "$target" fetch --prune
    git -C "$target" pull --ff-only
  else
    echo "[sync] Cloning $name ..."
    git clone "$url" "$target"
  fi

  paths+=("$target")
done

# Ensure deterministic ordering and uniqueness
mapfile -t SORTED_PATHS < <(printf "%s\n" "${paths[@]}" | sort -u)

printf "%s\n" "${SORTED_PATHS[@]}" | python3 - "$WORKSPACE_FILE" <<'PY'
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