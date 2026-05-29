---
description: Translate pending strings via Claude Haiku into a .po file
argument-hint: <lang: ru|en> [filter] [--max-strings N]
allowed-tools: Bash, Agent
---

# AI translation

Arguments: `$ARGUMENTS`

Format: `<lang> [filter] [--max-strings N]`
Examples: `ru month-01-*`, `en month-03-* --max-strings 50`

Steps:
1. Check that `ANTHROPIC_API_KEY` is set. If not, tell the user to run `export ANTHROPIC_API_KEY=sk-ant-...` in their terminal and stop.
2. Parse the language (`ru` or `en`) and optional filter from arguments. If no filter is given, translate the whole .po file.
3. If the batch is expected to contain 50+ strings, delegate to the `translation-batch` subagent (to keep the main context small). Otherwise run directly:
   ```
   uv run python scripts/translate-with-ai.py po/<lang>.po --filter <filter> --max-strings <N>
   ```
4. When finished, suggest `/validate <lang>`.
