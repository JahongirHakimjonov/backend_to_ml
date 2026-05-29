---
name: translation-workflow
description: Run the backend_to_ml translation pipeline (extract → translate → apply → validate). Triggered when the user mentions .po, gettext, msgstr, fuzzy, sync-translations, translate-with-ai, validate-translation, or after writing new src/*.md content.
---

# Translation workflow

`backend_to_ml` is a 3-language mdBook (uz default, ru, en). Translations live in `po/ru.po` and `po/en.po` in gettext format. msgids are extracted from `src/*.md`; msgstrs are the translations.

## 5-step pipeline

### 1. Sync (refresh msgids)
After editing `src/*.md`, update the po files:
```bash
./scripts/sync-translations.sh
```
Internally:
- `extract-messages.sh` → regenerates `po/messages.pot`
- `msgmerge` → updates `po/ru.po`, `po/en.po` (new msgids appended, changed ones marked `#, fuzzy`)

### 2. Extract a batch (optional)
For larger translation runs, pull pending strings into JSON:
```bash
uv run python scripts/extract-pending-batch.py po/ru.po \
  --filter "month-01-*" --count 200 \
  --output translations/ru-m01-batch.json
```
The filter matches msgid `occurrences` (file paths). Picks up both untranslated and fuzzy strings.

### 3. AI translation
```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run python scripts/translate-with-ai.py po/ru.po \
  --filter "month-01-*" --max-strings 100
```
- Default model: Claude Haiku 4.5
- Applies the 100+ standardized terms from `po/glossary.yaml`
- Skips words in the `do_not_translate` list
- Batches 30 strings per API call
- `--retranslate-fuzzy` — re-translates only entries marked fuzzy

Alternative: fill the JSON by hand, then run:
```bash
uv run python scripts/apply-translations.py po/ru.po translations/ru-m01-batch.json
```

### 4. Validate
```bash
uv run python scripts/validate-translation.py po/ru.po --strict
```
Checks:
- Markdown structure preserved (`#`, `-`, `>`, links)
- Inline code, HTML tags, emojis unchanged
- `do_not_translate` terms unchanged
- Plurals, format strings intact

Issues are written to `po/needs-review.txt`.

Flags:
- `--strict` — all checks
- `--mark-fuzzy` — automatically mark problematic msgstrs as fuzzy
- `--fix` (if available) — attempt auto-fix

### 5. Build check
```bash
MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru
```
A gettext error here means `po/ru.po` has a syntax issue.

## Hard rules

- **Never edit `msgid` by hand** — it's extracted from `src/*.md`
- **Never edit `po/messages.pot`** — auto-generated
- Add new terms to `po/glossary.yaml` to keep translation quality consistent
- All 3 languages stay in sync — if one falls behind, `mdbook build` falls back to source (not ideal)

## Quick commands

- `/sync-po` — step 1
- `/extract-batch <lang> <filter> <count>` — step 2
- `/translate <lang> [filter]` — step 3
- `/validate <lang>` — step 4
- `/fuzzy-count` — show fuzzy/untranslated counts per .po file
