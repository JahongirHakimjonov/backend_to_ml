# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project nature

`backend_to_ml` is an **mdBook-based 3-language (uz default, ru, en) educational book**, not a production application. Source is `src/*.md` (Uzbek), build output is `book/`. Python code (`scripts/`, `pyproject.toml`) is only for translation and build tooling; there is no runtime backend or ML service.

Language handling: the `mdbook-i18n-helpers` preprocessor reads `po/{ru,en}.po` (gettext) files; terms are standardized in `po/glossary.yaml`.

## Core rules

- **Use emojis sparingly** — only where genuinely necessary (navigation headers, exercise difficulty markers, capstone badges, etc.). Do not put an emoji in every paragraph or every bullet; if the text speaks for itself, leave the emoji out.
- **Translations must always stay in sync** — any content change in `src/*.md` (new sentence, edit, deletion) must be reflected in `po/ru.po` and `po/en.po` correspondingly. The workflow is mandatory: change → `./scripts/sync-translations.sh` (new msgids are added, changed ones are marked `fuzzy`) → re-translate fuzzy/new strings (`translate-with-ai.py --retranslate-fuzzy` or manually) → `validate-translation.py --strict`. Never let one language fall behind the others — `uz/ru/en` must always be in the same state.

## Build and Preview

**Critical**: `mdbook` and `mdbook-gettext` are installed in `~/.cargo/bin/`. Every session:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

**Single-language preview** (fastest — with live reload):

```bash
mdbook serve --open    # serves only uz
```

**Per-language build**:

```bash
mdbook build                                       # uz → book/
MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru   # ru → book/ru/
MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en   # en → book/en/
```

**Full 3-language preview** (`mdbook serve` returns 404 for `/ru/` and `/en/`):

```bash
# Build all 3 languages, then serve statically
cd book && python3 -m http.server 3000
# No hot reload — rebuild on every change
```

## Python tooling

Uses uv (Astral). Dependency groups in PEP 735 format:

```bash
uv sync                              # core + dev (default-groups = ["dev"])
uv sync --group month-XX             # single month's packages (month-01..06)
uv sync --group i18n                 # translation tooling (polib, anthropic, pyyaml)
uv sync --group month-03 --index pytorch-cu121   # NVIDIA GPU PyTorch
uv sync --all-groups                 # everything (~10 GB)
```

**Lint / format / type / test**:

```bash
uv run ruff check .                  # line-length 100, py311 target
uv run ruff format .
uv run mypy                          # notebooks/ and book/ excluded
uv run pytest                        # testpaths = ["tests"]
uv run pytest tests/test_X.py::test_name   # single test
```

**Notebook**:

```bash
uv run jupyter lab
```

## Translation workflow (PROJECT-SPECIFIC)

A new instance uses the `extract → translate → apply → validate` pipeline as follows:

**1. After `src/*.md` changes, sync `.po` files**:

```bash
./scripts/sync-translations.sh
# Internally: extract-messages.sh (POT generation) + msgmerge for ru.po and en.po
```

**2. Extract pending strings as a batch**:

```bash
uv run python scripts/extract-pending-batch.py po/ru.po \
    --filter "month-01-*" --count 200 \
    --output translations/ru-m01-batch.json
```

**3. AI translation** (Claude Haiku 4.5 default, respects glossary and do_not_translate rules):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run python scripts/translate-with-ai.py po/ru.po \
    --filter "month-01-*" --max-strings 100
# Or manually: fill in `msgstr` inside the JSON
```

**4. Apply translations from JSON to `.po`**:

```bash
uv run python scripts/apply-translations.py po/ru.po translations/ru-m01-batch.json
```

**5. Validation** (checks that markdown structure, links, inline code, HTML tags, emojis, and DNT terms are preserved):

```bash
uv run python scripts/validate-translation.py po/ru.po --strict
uv run python scripts/validate-translation.py po/ru.po --mark-fuzzy
# Issues → po/needs-review.txt
```

## Architecture

**Source → Output pipeline**:

```
src/*.md (uz source)
    ↓ mdbook build (UZ default)
    ↓ MDBOOK_BOOK__LANGUAGE=ru → [preprocessor.gettext] reads po/ru.po
    ↓ MDBOOK_BOOK__LANGUAGE=en → [preprocessor.gettext] reads po/en.po
book/  book/ru/  book/en/  (HTML output)
    ↓ scripts/fix-canonical-urls.sh   (.md → .html href fix, /index.html → /)
    ↓ scripts/generate-sitemap.py     (multilingual sitemap.xml + hreflang)
    ↓ GitHub Actions deploy.yml → GitHub Pages → backendtoml.milliytech.uz
```

**Key configuration files**:

- `book.toml` — mdBook configuration. `[preprocessor.gettext]` enables 3-language translation, `theme/lang-switcher.js` is added, `mathjax-support = true`.
- `pyproject.toml` — uv dependency groups, ruff (line-length 100, py311), mypy, pytest. `default-groups = ["dev"]`.
- `theme/head.hbs` — injects `hreflang` + canonical URL into every page (SEO).
- `theme/lang-switcher.js` — adds the 🇺🇿/🇷🇺/🇬🇧 button to the page header.
- `po/glossary.yaml` — 100+ standardized uz/ru/en term translations + `do_not_translate` list. When adding a new term, add it here too.
- `po/messages.pot` — POT template extracted from source (auto-generated, DO NOT edit manually).
- `po/{ru,en}.po` — full translation file for each language.
- `.github/workflows/deploy.yml` — on push to `main`, builds all 3 languages, generates the sitemap, adds CNAME, deploys to GitHub Pages.

**Content structure** (`src/`):

- `SUMMARY.md` — book navigation (required by mdBook). When adding a new chapter, the link must be added here.
- 6 `month-XX-*/` directories, each with `README.md` + `01-...md`, `02-...md`, ... + `exercises.md`.
- `final-projects/` — briefs for the 4 capstone projects.
- `resources/` — books, courses, datasets, cheatsheets.
- `glossary.md` — 200+ term glossary (displayed inside the book, distinct from `po/glossary.yaml`).

## `.claude/` tooling

This project ships with a `.claude/` directory that configures Claude Code for the project's workflow. All files inside `.claude/` are written in **English** — it's the config/infra layer, intentionally separate from the book content (Uzbek). The book itself (`src/*.md`, `po/*.po`, content commit messages) stays in Uzbek as defined elsewhere in this file.

### Layout

```
.claude/
├── settings.json              # permissions, env, hooks (commitable)
├── hooks/                     # 3 shell scripts wired to Claude Code events
│   ├── block-protected-files.sh
│   ├── sync-translations-bg.sh
│   └── session-start.sh
├── agents/                    # 4 project-specific subagents
│   ├── translation-batch.md
│   ├── chapter-creator.md
│   ├── glossary-curator.md
│   └── mdbook-builder.md
├── skills/                    # 3 auto-triggered skills
│   ├── translation-workflow/SKILL.md
│   ├── chapter-template/SKILL.md
│   └── mdbook-preview/SKILL.md
├── commands/                  # 10 slash commands
└── logs/                      # background hook output (gitignored)
```

### Hooks

Three shell scripts wired into Claude Code's hook events via `settings.json`:

- **`block-protected-files.sh`** (`PreToolUse`) — blocks `Edit`/`Write` to auto-generated files: `po/messages.pot`, `book/**`, `translations/*.json.tmp`. Returns exit 2 with an explanation.
- **`sync-translations-bg.sh`** (`PostToolUse`) — after Claude edits a `src/**/*.md` file, runs `./scripts/sync-translations.sh` in the background (debounced to once per 10 seconds). Output → `.claude/logs/sync.log`.
- **`session-start.sh`** (`SessionStart`) — surfaces `mdbook` PATH status and the fuzzy counts for `po/ru.po` and `po/en.po`.

### Subagents

Invoke with `Agent(subagent_type=<name>)`. They isolate specialized work from the main context.

| Agent | Purpose |
|-------|---------|
| `translation-batch` | End-to-end translation batch (extract → AI translate → validate) |
| `chapter-creator` | Scaffold a new chapter using the 10-section template + SUMMARY.md link |
| `glossary-curator` | Audit `po/glossary.yaml` against `src/` (read-only report) |
| `mdbook-builder` | Run the full 3-language build pipeline locally |

### Skills

Auto-triggered by Claude when matching context appears in the user's request:

- **`translation-workflow`** — fires when the user mentions `.po`, `gettext`, `msgstr`, `fuzzy`, or after `src/*.md` edits. Drives the 5-step pipeline.
- **`chapter-template`** — fires on "new chapter", "yangi bob", "month-XX". Documents the 10-section format.
- **`mdbook-preview`** — fires on "preview", "serve", "build", "3 languages". Documents preview options.

### Slash commands

Invoke with `/<name>`:

| Command | What it does |
|---------|-------------|
| `/sync-po` | `./scripts/sync-translations.sh` |
| `/translate <lang> [filter]` | AI translate via `translate-with-ai.py` (delegates to `translation-batch` for large batches) |
| `/validate <lang\|all>` | `validate-translation.py --strict` |
| `/extract-batch <lang> [filter] [count]` | `extract-pending-batch.py` → JSON |
| `/fuzzy-count` | Counts of fuzzy and untranslated per `.po` file |
| `/preview` | `mdbook serve --open` (uz only, live reload) |
| `/preview-all` | 3-language build + `python3 -m http.server 3000` |
| `/new-chapter <month-XX> <NN-topic>` | Scaffold via `chapter-creator` subagent |
| `/check-glossary` | Audit via `glossary-curator` subagent |
| `/build-check` | Local 3-language build via `mdbook-builder` subagent |

### `settings.json`

Project-wide configuration (commitable):

- **`permissions.allow`** — pre-approved Bash commands: `mdbook`, `MDBOOK_BOOK__LANGUAGE=* mdbook build`, `uv run *`, `./scripts/*.sh`, `python3 -m http.server`, `msgmerge`, `git status`, `grep`, etc.
- **`permissions.deny`** — `Edit(po/messages.pot)`, `Edit(book/**)`, `Write(book/**)`, `Edit(translations/*.json.tmp)`, `rm -rf book*`, `git push --force`
- **`env`** — prepends `~/.cargo/bin` to `PATH` (where `mdbook` lives)
- **`hooks`** — wires the three scripts above to `SessionStart`, `PreToolUse`, `PostToolUse`

## Content writing conventions

- **Language**: Uzbek (Latin script). Technical terms stay in English: `gradient descent`, `embedding`, `backpropagation`.
- **Style**: Code-first, theory-minimum. Do not dive into academic theory — let Andrew Ng's course do that.
- **Standard 10 sections per chapter**:
  1. Goal → 2. What we'll learn → 3. Libraries → 4. Key topics
  5. Code examples → 6. Backend integration (FastAPI/Django) → 7. Resources
  8. Exercises (Easy/Medium/Hard) → 9. Capstone → 10. Checklist
- **Code examples**: 10–30 lines, fully runnable, tested with `uv run`.
- **Commit convention**: Conventional Commits — `docs:`, `feat:`, `fix:`, `style:`, `refactor:`, `chore:`. `docs:` is the most common.

## Gotchas

- `mdbook` and `mdbook-gettext` live in `~/.cargo/bin/` — `export PATH="$HOME/.cargo/bin:$PATH"` every session.
- `mdbook serve` only serves the default (uz) language; `/ru/` and `/en/` return 404 locally. For full preview, build all 3 languages and run a static server from `book/`.
- After AI translation, **always** run `validate-translation.py --strict` to catch markdown breakage.
- Ruff excludes `notebooks/**/*.ipynb`; mypy excludes `notebooks/` and `book/`.
- `pyproject.toml` has `default-groups = ["dev"]` — `uv sync` always installs dev tools.
- PyTorch defaults to CPU; for CUDA, use the `--index pytorch-cu121` flag.
- `translations/*.json.tmp` — half-processed batches, do not commit.
- `fix-canonical-urls.sh` works with both macOS sed and GNU sed (`SED_INPLACE` detection).

## Do not

- Do not hand-edit `book/`, `book/ru/`, `book/en/` — they are auto-generated. Source is `src/`.
- Do not hand-edit `po/messages.pot` — `extract-messages.sh` rewrites it on every sync.
- Do not change `msgid` in existing `po/{ru,en}.po` — only `msgstr`. `msgid` is extracted from source.
- Do not include `notebooks/**/*.ipynb` in ruff/format — they're cleaned with `nbstripout`.
