#!/usr/bin/env bash
# SessionStart: surfaces PATH status and a translation-state summary.
# Output: stdout text — passed to Claude as additional context.

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"

# Is mdbook on PATH?
mdbook_path=""
if command -v mdbook >/dev/null 2>&1; then
  mdbook_path=$(command -v mdbook)
elif [[ -x "$HOME/.cargo/bin/mdbook" ]]; then
  mdbook_path="$HOME/.cargo/bin/mdbook"
fi

# Fuzzy count per language.
# Use awk — BSD grep -c returns exit 1 when zero lines match, which trips `set -e`.
ru_fuzzy=0
en_fuzzy=0
if [[ -f "$repo_root/po/ru.po" ]]; then
  ru_fuzzy=$(awk '/^#, fuzzy/ {c++} END {print c+0}' "$repo_root/po/ru.po" 2>/dev/null || echo 0)
fi
if [[ -f "$repo_root/po/en.po" ]]; then
  en_fuzzy=$(awk '/^#, fuzzy/ {c++} END {print c+0}' "$repo_root/po/en.po" 2>/dev/null || echo 0)
fi

cat <<EOF
backend_to_ml session started.

mdbook: ${mdbook_path:-"NOT FOUND — ensure \$HOME/.cargo/bin is on PATH"}
Translation state: ru.po fuzzy=$ru_fuzzy, en.po fuzzy=$en_fuzzy

Quick commands: /sync-po, /translate, /validate, /preview, /preview-all, /new-chapter
EOF
