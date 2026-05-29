#!/usr/bin/env python3
"""AI yordamida .po fayllarni o'zbek (manba) → ru/en ga tarjima.

Asosiy xususiyatlar:
- Claude API (Anthropic) — Haiku 4.5 default (arzon va aniq)
- po/glossary.yaml dan kalit terminlar va do_not_translate ro'yxati
- Batch (30 string per call) — sifat va tezlik balansi
- JSON output format — parsing aniq
- Markdown tuzilma saqlash qoidalari
- Avtomatik validatsiya (scripts/validate-translation.py mantiqi)
- Sinov rejimi (--dry-run) va filter (--filter PATTERN)

Foydalanish:
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/translate-with-ai.py po/ru.po
    python scripts/translate-with-ai.py po/en.po --filter "month-01-*"
    python scripts/translate-with-ai.py po/ru.po --pilot   # faqat Phase 1 fayllar
    python scripts/translate-with-ai.py po/ru.po --model claude-sonnet-4-6
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import polib
import yaml
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = ROOT / "po" / "glossary.yaml"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 30
MAX_TOKENS_OUTPUT = 8192

PHASE_1_PATTERNS = [
    "SUMMARY.md",
    "introduction.md",
    "about-author.md",
    "month-01-foundations/index.md",
    "month-02-classical-ml/index.md",
    "month-03-deep-learning/index.md",
    "month-04-cv-nlp/index.md",
    "month-05-llm-rag/index.md",
    "month-06-mlops-production/index.md",
]

LANG_NAMES = {
    "ru": ("Russian", "русский"),
    "en": ("English", "English"),
}


def detect_lang_from_po(po_path: Path) -> str:
    name = po_path.stem  # "ru" yoki "en"
    if name not in LANG_NAMES:
        sys.exit(f"Noma'lum til: {name}. Faqat ru yoki en qo'llab-quvvatlanadi.")
    return name


def load_glossary() -> dict:
    with open(GLOSSARY_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def build_glossary_block(glossary: dict, lang: str) -> str:
    """Glossary'dan tilga xos tarjima ro'yxatini system prompt uchun tayyorlaydi."""
    rows: list[str] = []
    for term in glossary.get("terms", []) or []:
        uz = term.get("uz", "").strip()
        target = term.get(lang, "").strip()
        if uz and target:
            rows.append(f"  - \"{uz}\" → \"{target}\"")
    return "\n".join(rows)


def build_dnt_block(glossary: dict) -> str:
    items = glossary.get("do_not_translate") or []
    return ", ".join(items)


SYSTEM_PROMPT_TEMPLATE = """Sen "Backend to ML" texnik o'quv kitobining {lang_name} tilga professional tarjimonisan. Manba — o'zbek tili (lotin yozuvi).

QATTIQ QOIDALAR (HAMMASI MAJBURIY):

1. **Ma'no aynan saqlanishi shart** — qo'shimcha izoh QO'SHMA, qisqartirma. Faqat tarjima.

2. **Glossary atamalari** — quyidagilar AYNAN belgilangan ekvivalentda tarjima qilinadi:
{glossary_block}

3. **Tarjima qilinmaydigan so'zlar** — quyidagi nomlar asl ko'rinishida saqlanadi:
   {dnt_block}

4. **Markdown sintaksisi 100% saqlanadi**:
   - `**bold**` → `**tarjima**`
   - `*italic*` → `*tarjima*`
   - `` `inline code` `` → AYNAN o'zgarmaydi (kod tarjima qilinmaydi)
   - ```` ```code blocks``` ```` → ICHIDA matn O'ZGARMAYDI, faqat `# comment` lar tarjima qilinadi
   - `# Sarlavha` → `# Tarjima` (# soni saqlanadi)
   - `- Ro'yxat` → `- Tarjima`
   - `[matn](url)` → `[tarjima](url)` — URL AYNAN saqlanadi
   - `![alt](url)` → `![tarjima](url)` — URL AYNAN saqlanadi

5. **HTML taglar** (`<details>`, `<summary>`, `<br>`, `<sub>`, `<sup>`) — saqlanadi.

6. **Emoji va maxsus belgilar** — saqlanadi (✅, 🎯, ⚠️, 🚀, va h.k.).

7. **URL, fayl yo'llari, fayl nomlari, email** — o'zgarmaydi.

8. **Sonlar, formula, matematik belgilar** — o'zgarmaydi.

9. **Texnik aniqlik > stilistik chiroy.** Shubhada — sodda va aniq variant.

10. **Bir nechta gap** — manbada qancha gap bo'lsa, tarjimada ham shuncha bo'lishi shart.

OUTPUT FORMATI:
Faqat JSON object qaytar:
```json
{{"translations": ["tarjima1", "tarjima2", ...]}}
```
Hech qanday tushuntirish, kirish, izoh yo'q. Faqat JSON.
Tarjimalar tartibi inputdagi tartibga aynan mos kelishi shart."""


def build_user_message(batch: list[dict]) -> str:
    lines = ["Quyidagi matnlarni tarjima qil (har biri alohida string):", ""]
    for i, item in enumerate(batch, 1):
        ref = item.get("ref", "")
        lines.append(f"--- #{i}{(' [' + ref + ']') if ref else ''} ---")
        lines.append(item["msgid"])
        lines.append("")
    lines.append("Qaytar: JSON object {\"translations\": [...]}")
    return "\n".join(lines)


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    reraise=True,
)
def call_anthropic(
    client: Anthropic,
    model: str,
    system_prompt: str,
    user_msg: str,
) -> str:
    msg = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS_OUTPUT,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    if not msg.content:
        raise RuntimeError("Bo'sh javob")
    text = msg.content[0].text  # type: ignore[union-attr]
    return text


def parse_translations(raw: str, expected_count: int) -> list[str]:
    """Claude JSON javobini ajratib oladi. Markdown code fence'ni ham e'tiborga oladi."""
    text = raw.strip()
    # ```json ... ``` chiqarib tashlash
    if text.startswith("```"):
        # birinchi nechta qatorlar (``` va ehtimol json) ni o'tkazib yuborish
        lines = text.split("\n")
        # birinchi ``` qator
        if lines[0].startswith("```"):
            lines = lines[1:]
        # oxirgi ```
        while lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        # Fallback: brace matching bilan birinchi {} ni topish
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                data = json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                raise RuntimeError(f"JSON parse fail: {e}\nRaw: {raw[:500]}")
        else:
            raise RuntimeError(f"JSON topilmadi: {e}\nRaw: {raw[:500]}")

    translations = data.get("translations")
    if not isinstance(translations, list):
        raise RuntimeError(f"'translations' kaliti yo'q. Got: {list(data.keys())}")
    if len(translations) != expected_count:
        raise RuntimeError(
            f"Tarjima soni mos kelmadi: kutilgan {expected_count}, olingan {len(translations)}"
        )
    return [str(t) for t in translations]


def entry_matches_filter(entry: polib.POEntry, patterns: list[str]) -> bool:
    if not patterns:
        return True
    for src_file, _ in entry.occurrences or []:
        for pat in patterns:
            if fnmatch.fnmatch(src_file, pat):
                return True
            if pat in src_file:
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="AI translate .po file")
    parser.add_argument("po_file", type=Path, help="po/ru.po yoki po/en.po")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model nomi")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument(
        "--filter",
        action="append",
        default=[],
        help="Faqat ushbu pattern'ga mos manba fayllarni tarjima qilish",
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="Phase 1 fayllar (skelet kontent) bilan cheklanish",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Faqat hisoblash, API'ga so'rov yubormaslik",
    )
    parser.add_argument(
        "--retranslate-fuzzy",
        action="store_true",
        help="`fuzzy` belgilangan stringlarni qayta tarjima qilish",
    )
    parser.add_argument(
        "--max-strings",
        type=int,
        default=0,
        help="Maksimal nechta string tarjima qilinadi (0 = limitsiz)",
    )
    args = parser.parse_args()

    if not args.po_file.exists():
        print(f"Fayl topilmadi: {args.po_file}", file=sys.stderr)
        return 1

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        print("ANTHROPIC_API_KEY environment variable yo'q.", file=sys.stderr)
        return 1

    lang = detect_lang_from_po(args.po_file)
    lang_name, _ = LANG_NAMES[lang]
    glossary = load_glossary()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        lang_name=lang_name,
        glossary_block=build_glossary_block(glossary, lang) or "  (bo'sh)",
        dnt_block=build_dnt_block(glossary) or "(bo'sh)",
    )

    patterns = list(args.filter)
    if args.pilot:
        patterns.extend(PHASE_1_PATTERNS)

    po = polib.pofile(str(args.po_file))
    pending: list[tuple[polib.POEntry, dict]] = []

    for entry in po:
        if entry.obsolete:
            continue
        if not entry.msgid.strip():
            continue
        is_fuzzy = "fuzzy" in entry.flags
        has_translation = bool(entry.msgstr.strip())
        if has_translation and not (args.retranslate_fuzzy and is_fuzzy):
            continue
        if not entry_matches_filter(entry, patterns):
            continue
        ref = ""
        if entry.occurrences:
            ref = f"{entry.occurrences[0][0]}:{entry.occurrences[0][1]}"
        pending.append((entry, {"msgid": entry.msgid, "ref": ref}))

    if args.max_strings > 0:
        pending = pending[: args.max_strings]

    print(f"Tarjima qilinadigan stringlar: {len(pending)}")
    if args.dry_run or not pending:
        return 0

    client = Anthropic(api_key=api_key)

    total_done = 0
    save_every = max(1, len(pending) // 20)  # ~5% qadamlarda saqlash

    for batch_start in range(0, len(pending), args.batch_size):
        batch = pending[batch_start : batch_start + args.batch_size]
        batch_data = [item for _, item in batch]
        user_msg = build_user_message(batch_data)

        try:
            raw = call_anthropic(client, args.model, system_prompt, user_msg)
            translations = parse_translations(raw, len(batch_data))
        except Exception as e:  # noqa: BLE001
            print(
                f"[XATO batch={batch_start//args.batch_size}] {e}",
                file=sys.stderr,
            )
            time.sleep(5)
            continue

        for (entry, _meta), translated in zip(batch, translations):
            entry.msgstr = translated
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            total_done += 1

        if total_done and total_done % save_every == 0:
            po.save(str(args.po_file))
            print(f"  saqlandi: {total_done}/{len(pending)}")

    po.save(str(args.po_file))
    print(f"Tugadi: {total_done}/{len(pending)} string tarjima qilindi → {args.po_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
