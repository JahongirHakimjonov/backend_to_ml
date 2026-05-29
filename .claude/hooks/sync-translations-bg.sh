#!/usr/bin/env bash
# PostToolUse: when src/**/*.md is saved, runs sync-translations.sh in the background.
# Output goes to .claude/logs/sync.log.

set -euo pipefail

payload=$(cat)

file_path=$(printf '%s' "$payload" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("file_path", ""))
except Exception:
    print("")
')

# Only fire for src/**/*.md
case "$file_path" in
  */src/*.md)
    ;;
  *)
    exit 0
    ;;
esac

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
log_dir="$repo_root/.claude/logs"
mkdir -p "$log_dir"

# Debounce: skip if a run happened within the last 10 seconds.
last_run="$log_dir/.sync-last-run"
now=$(date +%s)
if [[ -f "$last_run" ]]; then
  prev=$(cat "$last_run" 2>/dev/null || echo 0)
  if (( now - prev < 10 )); then
    exit 0
  fi
fi
echo "$now" > "$last_run"

# Run in background: nohup + disown so the hook returns quickly.
(
  cd "$repo_root"
  export PATH="$HOME/.cargo/bin:$PATH"
  {
    echo "=== sync $(date '+%Y-%m-%d %H:%M:%S') trigger: $file_path ==="
    ./scripts/sync-translations.sh 2>&1 || echo "sync FAILED (exit $?)"
    echo ""
  } >> "$log_dir/sync.log"
) </dev/null >/dev/null 2>&1 &
disown 2>/dev/null || true

exit 0
