---
description: Audit po/glossary.yaml against src/ content
allowed-tools: Agent
---

# Glossary audit

Delegate to the `glossary-curator` subagent. It will:
1. Find frequently used technical terms in `src/**/*.md`
2. Report any that are missing from `po/glossary.yaml`
3. Check that existing terms are used consistently (uz/ru/en in sync)
4. Verify `do_not_translate` coverage

This is read-only — `glossary.yaml` is not modified automatically. If the user wants to apply changes, request explicit confirmation first.
