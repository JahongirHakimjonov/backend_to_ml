#!/usr/bin/env python3
"""Tuzatish: `**X:**[link]` → `**X:** [link]`.

Avvalgi xato regex `(\\*\\*+)[ \\t]+(?=\\S)` bold yopilishidan keyingi spaceni
har joyda olib tashlagan. Bu skript shu artifaktni qaytaradi (faqat link
boshlanishidan oldin va `: kabi label-keyin holat uchun).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# `**X:**[...]` → `**X:** [...]`
PATTERN_LINK = re.compile(r"(\*\*[^*\n]+\*\*)(\[)")


def fix_text(text: str) -> str:
    return PATTERN_LINK.sub(r"\1 \2", text)


def main() -> int:
    if len(sys.argv) < 2:
        print("foydalanish: fix_bold_bracket.py PATH...", file=sys.stderr)
        return 2
    files: list[Path] = []
    for p in sys.argv[1:]:
        path = Path(p)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))

    changed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new_text = fix_text(text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"o'zgartirildi: {f}")
    print(f"\nJami: {changed} fayl tuzatildi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
