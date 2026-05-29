---
name: mdbook-preview
description: Preview the backend_to_ml mdBook locally — single language or all three. Triggered when the user mentions "preview", "serve", "build", "show me the book", or "all three languages".
---

# mdBook preview options

`backend_to_ml` is a 3-language book, but `mdbook serve` only serves the default language (uz). Two main options below.

## Setup (every session)

```bash
export PATH="$HOME/.cargo/bin:$PATH"
mdbook --version    # should print mdbook v0.4.X
```

If `mdbook` is missing: `cargo install mdbook mdbook-i18n-helpers`.

## Option 1: single language with live reload

The fastest, most common option — Uzbek only:

```bash
mdbook serve --open
```

- Opens the browser automatically
- Rebuilds on `src/*.md` changes
- `/ru/` and `/en/` URLs return 404 (only the default language is built)

Different port: `mdbook serve --port 4000`.

Stop with Ctrl+C.

## Option 2: all 3 languages (no hot reload)

To see all three languages:

```bash
# 1. Build them
mdbook build
MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru
MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en

# 2. Fix canonical URLs (.md → .html)
./scripts/fix-canonical-urls.sh

# 3. Static server
cd book && python3 -m http.server 3000
```

URLs:
- `http://localhost:3000/` — Uzbek (default)
- `http://localhost:3000/ru/` — Russian
- `http://localhost:3000/en/` — English

No hot reload — rebuild after each change. Use this when you specifically need to check the translated output.

## Option 3: serve a single non-default language (rare)

```bash
MDBOOK_BOOK__LANGUAGE=ru mdbook serve --port 3001
```
Serves Russian as the default at `/` with live reload.

## Quick commands

- `/preview` — option 1 (uz, live reload)
- `/preview-all` — option 2 (all 3, no hot reload)
- `/build-check` — builds only, no server (CI-style verification)

## Notes

- `book/` is in `.gitignore` — never committed
- `theme/lang-switcher.js` adds the 🇺🇿/🇷🇺/🇬🇧 button to every page
- `theme/head.hbs` injects hreflang and canonical URL meta tags (SEO)
- Production: `https://backendtoml.milliytech.uz` — deployed via `.github/workflows/deploy.yml`
