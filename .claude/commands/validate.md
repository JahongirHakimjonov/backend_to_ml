---
description: Validate .po translation quality in strict mode
argument-hint: <lang: ru|en|all>
allowed-tools: Bash
---

# Validate translations

Arguments: `$ARGUMENTS` (empty = `all`).

Steps:
1. If the argument is `all` or empty, run for both `ru` and `en`.
2. For each language: `uv run python scripts/validate-translation.py po/<lang>.po --strict`
3. Checks: markdown structure, links, inline code, HTML tags, emoji, `do_not_translate` terms preserved.
4. If `po/needs-review.txt` is produced, show the first ~20 lines.
5. If issues are found, suggest `--mark-fuzzy` or manual editing.
