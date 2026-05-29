#!/usr/bin/env python3
"""Tarjima kutib turgan keyingi N msgid'ni JSON sifatida chiqaradi.

Foydalanish:
    python scripts/extract-pending-batch.py po/ru.po --count 100 --pilot
    python scripts/extract-pending-batch.py po/ru.po --count 200 --filter "month-01-*"
    python scripts/extract-pending-batch.py po/ru.po --count 100 --offset 200

Output formati (stdout):
[
    {"id": "<msgid uniqueness key>", "msgid": "...", "ref": "src/.../path:line"},
    ...
]
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parent.parent

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


def stable_key(msgid: str) -> str:
    return hashlib.sha1(msgid.encode("utf-8")).hexdigest()[:12]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("po_file", type=Path)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--filter", action="append", default=[])
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument(
        "--include-fuzzy",
        action="store_true",
        help="fuzzy belgilanganlarni ham chiqarish",
    )
    parser.add_argument("--output", type=Path, help="Faylga yozish (stdout default)")
    args = parser.parse_args()

    if not args.po_file.exists():
        print(f"Topilmadi: {args.po_file}", file=sys.stderr)
        return 1

    patterns = list(args.filter)
    if args.pilot:
        patterns.extend(PHASE_1_PATTERNS)

    po = polib.pofile(str(args.po_file))
    pending: list[dict] = []
    for entry in po:
        if entry.obsolete or not entry.msgid.strip():
            continue
        is_fuzzy = "fuzzy" in entry.flags
        has_translation = bool(entry.msgstr.strip())
        if has_translation and not (args.include_fuzzy and is_fuzzy):
            continue
        if not entry_matches_filter(entry, patterns):
            continue
        ref = ""
        if entry.occurrences:
            ref = f"{entry.occurrences[0][0]}:{entry.occurrences[0][1]}"
        pending.append(
            {
                "id": stable_key(entry.msgid),
                "msgid": entry.msgid,
                "ref": ref,
            }
        )

    sliced = pending[args.offset : args.offset + args.count]
    output = json.dumps(sliced, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(
            f"Yozildi: {args.output} ({len(sliced)} string, jami pending: {len(pending)})",
            file=sys.stderr,
        )
    else:
        print(output)
        print(
            f"# {len(sliced)} string chiqarildi, jami pending: {len(pending)}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
