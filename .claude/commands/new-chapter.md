---
description: Scaffold a new chapter using the 10-section format
argument-hint: <month-XX> <NN-topic>
allowed-tools: Agent
---

# Create a new chapter

Arguments: `$ARGUMENTS`

Format: `<month-XX> <NN-topic>` — e.g. `month-03 03-pytorch-basics`.

Steps:
1. Validate arguments. If incomplete, ask the user for the month (01..06) and the chapter number + name.
2. Delegate to the `chapter-creator` subagent with the task:
   - Create `src/<month-XX-*>/<NN-topic>.md` from the 10-section template
   - Insert a link in `src/SUMMARY.md` at the correct position
   - Note any new technical terms missing from `po/glossary.yaml`
   - Run `./scripts/sync-translations.sh`
3. Once the subagent returns, check the fuzzy count and suggest `/translate ru` and `/translate en`.
