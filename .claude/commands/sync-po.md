---
description: Refresh .po files from src/ (extract + msgmerge)
allowed-tools: Bash
---

# Sync .po files

Run `./scripts/sync-translations.sh`. It will:
1. Regenerate `po/messages.pot` via `extract-messages.sh`
2. Update `po/ru.po` and `po/en.po` via `msgmerge` (new msgids appended, changed ones marked `fuzzy`)

After the script finishes, run `git status` and summarize which files changed. If new or fuzzy strings appeared, suggest running `/translate`.
