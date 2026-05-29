#!/usr/bin/env python3
"""JSON faylidan tarjimalarni .po faylga qo'llaydi.

Input formati:
    [
        {"id": "abc123def456", "msgstr": "Tarjima matni"},
        ...
    ]

`id` — extract-pending-batch.py chiqarganidek msgid'ning sha1 hash'ining birinchi
12 belgisi. Bu xavfsiz, chunki msgid juda uzun bo'lsa ham unique kalit beradi.

Foydalanish:
    python scripts/apply-translations.py po/ru.po translations/ru-batch-01.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent


def stable_key(msgid: str) -> str:
    return hashlib.sha1(msgid.encode("utf-8")).hexdigest()[:12]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("po_file", type=Path)
    parser.add_argument("translations_json", type=Path)
    parser.add_argument(
        "--remove-fuzzy",
        action="store_true",
        default=True,
        help="Tarjima qo'shilgan keyin fuzzy belgisini olib tashlash",
    )
    args = parser.parse_args()

    if not args.po_file.exists():
        print(f"Topilmadi: {args.po_file}", file=sys.stderr)
        return 1
    if not args.translations_json.exists():
        print(f"Topilmadi: {args.translations_json}", file=sys.stderr)
        return 1

    data = json.loads(args.translations_json.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("Input JSON list bo'lishi kerak", file=sys.stderr)
        return 1

    by_id: dict[str, str] = {}
    for item in data:
        if "id" not in item or "msgstr" not in item:
            continue
        by_id[item["id"]] = item["msgstr"]

    if not by_id:
        print("JSON ichida tarjima topilmadi", file=sys.stderr)
        return 1

    po = polib.pofile(str(args.po_file))
    applied = 0
    skipped = 0
    for entry in po:
        if entry.obsolete or not entry.msgid.strip():
            continue
        key = stable_key(entry.msgid)
        if key not in by_id:
            continue
        new_msgstr = by_id[key]
        if not new_msgstr.strip():
            skipped += 1
            continue
        entry.msgstr = new_msgstr
        if args.remove_fuzzy and "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")
        applied += 1

    po.save(str(args.po_file))
    print(f"Qo'llandi: {applied}/{len(by_id)} (skipped bo'sh: {skipped}) → {args.po_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
