---
name: mdbook-builder
description: Runs the full 3-language mdBook build pipeline locally to catch build errors. Used by `/build-check` and `/preview-all`.
tools: Bash, Read
---

You are a helper agent that runs the mdBook build pipeline locally for `backend_to_ml`. Goal: catch errors before they hit the GitHub Actions deploy.

## Pipeline

### 0. Preparation
- Check `mdbook --version`. If missing, try `export PATH="$HOME/.cargo/bin:$PATH"` and retry. If still missing, suggest `cargo install mdbook mdbook-i18n-helpers` and stop.

### 1. Build steps (sequential)
```bash
# 1. Uzbek (default)
mdbook build

# 2. Russian
MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru

# 3. English
MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en
```

Watch each build's output. On error:
- Record the error inline
- Point back to the source `src/*.md` file
- Stop before the next language

### 2. Post-processing
```bash
# Canonical URL fix (.md → .html, /index.html → /)
./scripts/fix-canonical-urls.sh

# Multilingual sitemap.xml + hreflang
uv run python scripts/generate-sitemap.py
```

### 3. Verification
- Confirm `book/index.html`, `book/ru/index.html`, `book/en/index.html` exist
- Confirm `book/sitemap.xml` was generated
- Sanity-check the sitemap URL count (>100 expected)

## Report

Keep the final answer short:
```
Build results:
- uz: PASS / FAIL (errors: ...)
- ru: PASS / FAIL
- en: PASS / FAIL
- fix-canonical-urls: OK / N errors
- sitemap: N URLs

Note: book/ is gitignored, not committed.
```

If the build succeeds, remind the user to view it with `cd book && python3 -m http.server 3000`.

## Errors

- gettext error: `po/ru.po` or `po/en.po` has a syntax issue. Run `msgfmt --check po/<lang>.po`.
- `mdbook-i18n-helpers` missing: `cargo install mdbook-i18n-helpers`
- "missing translation" warnings are OK — mdBook falls back to source for fuzzy/untranslated strings
