---
description: Extract pending translation strings as a JSON batch
argument-hint: <lang: ru|en> [filter] [count]
allowed-tools: Bash
---

# Extract a pending batch

Arguments: `$ARGUMENTS`

Format: `<lang> [filter] [count]` — e.g. `ru month-01-* 200`. Default count = 100.

Steps:
1. Parse language, filter, and count from arguments.
2. Create `translations/` if missing.
3. Run:
   ```
   uv run python scripts/extract-pending-batch.py po/<lang>.po \
     --filter "<filter>" --count <count> \
     --output translations/<lang>-<slug>-batch.json
   ```
   Where `<slug>` is derived from the filter (`month-01-*` → `m01`, empty → `all`).
4. Show the first 3 msgid samples from the generated JSON.
5. Suggest either filling the JSON by hand or delegating to AI via `/translate <lang>`.
