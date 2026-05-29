#!/usr/bin/env python3
"""Tarjima sifatini validatsiya qilish.

Har bir msgid/msgstr juftligi uchun markdown tuzilmasi izchilligini tekshiradi:
- Kod bloklari soni va til belgisi mos
- Inline code (` `) soni
- Bold (**) va italic (*) soni
- Link va rasm targetlari aynan saqlangan
- HTML taglar saqlangan
- Emoji saqlangan
- do_not_translate so'zlari tarjimada ham bor

Foydalanish:
    python scripts/validate-translation.py po/ru.po
    python scripts/validate-translation.py po/en.po
    python scripts/validate-translation.py po/ru.po --strict      # fail on warnings
    python scripts/validate-translation.py po/ru.po --mark-fuzzy  # invalid msgstr → fuzzy
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable

import polib
import yaml

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = ROOT / "po" / "glossary.yaml"

# Markdown patternlari
CODE_FENCE = re.compile(r"```")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
BOLD = re.compile(r"\*\*([^*\n]+)\*\*")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)[^>]*>")
HEADING = re.compile(r"^#{1,6}\s+", re.MULTILINE)


def is_emoji(ch: str) -> bool:
    if not ch:
        return False
    cp = ord(ch)
    return (
        0x1F300 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or 0x2700 <= cp <= 0x27BF
        or 0x1F000 <= cp <= 0x1F2FF
        or 0x2300 <= cp <= 0x23FF
        or cp in (0x231A, 0x231B, 0x23E9, 0x23EA, 0x23EB, 0x23EC, 0x23F0, 0x23F3)
    )


def extract_emojis(s: str) -> list[str]:
    return [ch for ch in s if is_emoji(ch)]


def load_glossary() -> dict:
    if not GLOSSARY_PATH.exists():
        return {"do_not_translate": []}
    with open(GLOSSARY_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def find_violations(msgid: str, msgstr: str, do_not_translate: Iterable[str]) -> list[str]:
    """Bitta msgid/msgstr juftligi uchun barcha xato/ogohlantirishlarni qaytaradi."""
    issues: list[str] = []
    if not msgstr.strip():
        return issues  # bo'sh tarjima — fallback uchun OK

    # Code fence soni
    if msgid.count("```") != msgstr.count("```"):
        issues.append(
            f"code fence count: msgid={msgid.count('```')} msgstr={msgstr.count('```')}"
        )

    # Inline code count
    msgid_inline = INLINE_CODE.findall(msgid)
    msgstr_inline = INLINE_CODE.findall(msgstr)
    if len(msgid_inline) != len(msgstr_inline):
        issues.append(
            f"inline code count: msgid={len(msgid_inline)} msgstr={len(msgstr_inline)}"
        )
    else:
        # Inline code AYNAN saqlanishi kerak (tarjima emas)
        for a, b in zip(msgid_inline, msgstr_inline):
            if a != b:
                issues.append(f"inline code changed: `{a}` != `{b}`")
                break

    # Bold count
    if len(BOLD.findall(msgid)) != len(BOLD.findall(msgstr)):
        issues.append(
            f"bold count: msgid={len(BOLD.findall(msgid))} "
            f"msgstr={len(BOLD.findall(msgstr))}"
        )

    # Link targetlari aynan saqlanishi
    msgid_links = LINK.findall(msgid)
    msgstr_links = LINK.findall(msgstr)
    if len(msgid_links) != len(msgstr_links):
        issues.append(
            f"link count: msgid={len(msgid_links)} msgstr={len(msgstr_links)}"
        )
    else:
        for a, b in zip(msgid_links, msgstr_links):
            if a != b:
                issues.append(f"link target changed: '{a}' != '{b}'")
                break

    # HTML taglar
    msgid_tags = sorted(t.lower() for t in HTML_TAG.findall(msgid))
    msgstr_tags = sorted(t.lower() for t in HTML_TAG.findall(msgstr))
    if msgid_tags != msgstr_tags:
        issues.append(f"HTML tags differ: msgid={msgid_tags} msgstr={msgstr_tags}")

    # Emoji
    msgid_emojis = extract_emojis(msgid)
    msgstr_emojis = extract_emojis(msgstr)
    if sorted(msgid_emojis) != sorted(msgstr_emojis):
        issues.append(
            f"emoji differ: msgid={msgid_emojis} msgstr={msgstr_emojis}"
        )

    # Sarlavha darajasi (#) ham saqlanishi
    if HEADING.search(msgid) and not HEADING.search(msgstr):
        issues.append("heading marker (#) yo'qolgan")

    # do_not_translate — agar msgid'da bo'lsa, msgstr'da ham bo'lishi kerak
    for term in do_not_translate:
        if term in msgid and term not in msgstr:
            issues.append(f"DNT term '{term}' yo'qolgan")
            break  # bitta misol yetarli

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate .po translation quality")
    parser.add_argument("po_file", type=Path, help="po/ru.po yoki po/en.po")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Warning'larni ham fail deb hisoblash (exit code 1)",
    )
    parser.add_argument(
        "--mark-fuzzy",
        action="store_true",
        help="Validatsiya fail bo'lgan msgstr'larni fuzzy deb belgilash va faylni qayta yozish",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "po" / "needs-review.txt",
        help="Topilgan muammolar yoziladigan fayl",
    )
    args = parser.parse_args()

    if not args.po_file.exists():
        print(f"Fayl topilmadi: {args.po_file}", file=sys.stderr)
        return 1

    glossary = load_glossary()
    dnt = glossary.get("do_not_translate") or []

    po = polib.pofile(str(args.po_file))
    total = 0
    invalid = 0
    issues_log: list[str] = []

    for entry in po:
        if not entry.msgstr or entry.obsolete:
            continue
        total += 1
        issues = find_violations(entry.msgid, entry.msgstr, dnt)
        if issues:
            invalid += 1
            if args.mark_fuzzy:
                if "fuzzy" not in entry.flags:
                    entry.flags.append("fuzzy")
            location = ""
            if entry.occurrences:
                location = f" [{entry.occurrences[0][0]}:{entry.occurrences[0][1]}]"
            issues_log.append(
                f"--- msgid: {entry.msgid[:80]!r}{location}\n"
                f"    msgstr: {entry.msgstr[:80]!r}\n"
                f"    issues: {'; '.join(issues)}\n"
            )

    if args.mark_fuzzy:
        po.save(str(args.po_file))

    if issues_log:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            f"# Validatsiya hisoboti: {args.po_file.name}\n"
            f"# {invalid}/{total} stringda muammo topildi\n\n"
            + "\n".join(issues_log),
            encoding="utf-8",
        )

    print(f"{args.po_file.name}: {total} tarjima qilingan, {invalid} muammo")
    if invalid and args.strict:
        print(f"Strict rejim: muammo topildi → {args.report}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
