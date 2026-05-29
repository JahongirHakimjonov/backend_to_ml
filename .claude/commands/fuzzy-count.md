---
description: Count fuzzy/untranslated strings per .po file
allowed-tools: Bash
---

# Fuzzy / untranslated counts

For each `po/*.po` (`ru.po`, `en.po`), report:
- Total msgid count: `grep -c '^msgid' po/<lang>.po` (subtract 1 for the header)
- Fuzzy: `grep -c '^#, fuzzy' po/<lang>.po`
- Empty msgstr (untranslated): `awk '/^msgstr ""/{c++} END{print c}' po/<lang>.po` (approximate, excludes header)

Output as a table:
```
| Lang | Total | Fuzzy | Untranslated |
|------|-------|-------|--------------|
| ru   | ...   | ...   | ...          |
| en   | ...   | ...   | ...          |
```

If fuzzy or untranslated > 0, suggest `/translate <lang>`.
