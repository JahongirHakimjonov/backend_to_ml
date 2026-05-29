---
description: Run the full 3-language mdBook build locally to catch errors before CI
allowed-tools: Agent
---

# Local build check

Delegate to the `mdbook-builder` subagent. It will:
1. `mdbook build` (uz default)
2. `MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru`
3. `MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en`
4. `./scripts/fix-canonical-urls.sh` for each of `book/`, `book/ru/`, `book/en/`
5. `uv run python scripts/generate-sitemap.py`

If errors surface, the subagent reports them with pointers to source `src/*.md` files. Output goes to `book/` — git should show no changes (book/ is gitignored).

Use this command to catch issues locally before pushing and triggering the GitHub Actions deploy.
