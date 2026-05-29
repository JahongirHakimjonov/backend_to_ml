---
name: chapter-template
description: Write a new chapter for the backend_to_ml book — 10-section format, code-first style. Triggered when the user mentions "new chapter", "yangi bob", "month-XX", "new section", or asks to add content.
---

# Chapter template (10 sections)

`backend_to_ml` guides backend developers toward ML/MLOps. Every chapter follows a fixed 10-section structure. Style: **code-first, theory-minimum** — leave deep academic theory to Andrew Ng's course.

## Language and format

- **Body language**: Uzbek (Latin script)
- **Technical terms stay in English**: `gradient descent`, `embedding`, `backpropagation`, `tensor`, `loss function`
- **Code examples**: 10–30 lines, fully runnable (tested with `uv run`)
- **Emojis are rare**: only for navigation headers, exercise difficulty markers, capstone badges. Not in every paragraph.

## The 10 sections

```markdown
# Chapter title (short, specific)

## 1. Maqsad
1–2 sentences. What and why, framed in backend-developer terms.

## 2. O'rganadigan narsalar
A 5–8 item list. "Understand X", "Write Y", "Integrate with Z".

## 3. Kerakli kutubxonalar
\`\`\`bash
uv sync --group month-XX
\`\`\`
Or the matching pyproject.toml group. Show versions.

## 4. Asosiy mavzular
### 4.1 Topic 1
Short explanation (1–2 paragraphs). Don't dive deep into theory.

### 4.2 Topic 2
...

(Usually 3–5 subtopics)

## 5. Kod misollari
\`\`\`python
# 10–30 line example
# Imports
# Logic
# Output / print
\`\`\`

Multiple examples are fine. Each one fully self-contained.

## 6. Backend integratsiya
**Mandatory section** — the book targets backend developers.

\`\`\`python
# How to use the model from a FastAPI endpoint or Django view
from fastapi import FastAPI
# ...
\`\`\`

## 7. Manbalar
- 📘 [Book name](URL) — chapter/page
- 🎥 [Course name](URL) — module
- 📰 [Article](URL)
- 🔗 [GitHub repo](URL)

3–7 references. Andrew Ng, fast.ai, Hugging Face are standard.

## 8. Mashqlar

### 🟢 Easy (1–2)
1. ...
2. ...

### 🟡 Medium (2–3)
1. ...
2. ...
3. ...

### 🔴 Hard (1–2)
1. ...
2. ...

## 9. Capstone 🏆
A mini-project that ties the chapter together. 2–5 days of work. Backend integration required.

Example: "Add ML-based fraud detection to the User model in your existing Django project."

## 10. Tekshirish ro'yxati
- [ ] I understand X
- [ ] I can write Y
- [ ] I applied Z in a real project
- [ ] I completed at least 70% of the exercises
- [ ] I finished the capstone
```

## When creating a new chapter

1. Pick the folder: `src/month-XX-*/` — existing ones are `month-01-foundations`, `month-02-classic-ml`, etc.
2. Filename: `NN-topic.md` (NN = two-digit ordinal)
3. Add the link to `src/SUMMARY.md` in the right order, before `exercises.md`
4. Run `./scripts/sync-translations.sh` — appends new msgids to `po/ru.po` and `po/en.po`
5. If new terms appear, add them to `po/glossary.yaml`
6. Translate with `/translate ru month-XX-*` and `/translate en month-XX-*`

## Quick command

`/new-chapter month-XX NN-topic` — invokes this skill and delegates to the `chapter-creator` subagent.
