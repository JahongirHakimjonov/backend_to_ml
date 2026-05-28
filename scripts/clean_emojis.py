#!/usr/bin/env python3
"""Backend-to-ML kitobida emoji tozalash.

Code-block aware. Kontekstga qarab har xil qoidalar:
- Code block ichida: tegmaymiz.
- Heading qatorda (^#+ ...): faqat 🎯 🏋 ✅ va 🟢🟡🔴 saqlanadi.
- Jadval qatorda (^|...): ⚡⚡⚡, ⚡⚡, 🐌 → matnga; rating ⭐ va status ✅/❌ saqlanadi.
- Boshqa inline qatorda: dekorativ olib tashlanadi.
  Saqlanadi: ✅❌ 🟢🟡🔴 ⭐ va kontakt 💬📧🌐🐙💼 va 🎯 🏋.

Foydalanish:
    python3 clean_emojis.py --check FILES...
    python3 clean_emojis.py --apply FILES...
    python3 clean_emojis.py --check src/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VS16 = "️"
ZWJ = "‍"

# Keng emoji range (Unicode emoji ranges)
EMOJI_CLASS = (
    r"[\U0001F300-\U0001F5FF"
    r"\U0001F600-\U0001F64F"
    r"\U0001F680-\U0001F6FF"
    r"\U0001F700-\U0001F77F"
    r"\U0001F780-\U0001F7FF"
    r"\U0001F800-\U0001F8FF"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA00-\U0001FA6F"
    r"\U0001FA70-\U0001FAFF"
    r"\U00002600-\U000026FF"
    r"\U00002700-\U000027BF"
    r"\U0001F100-\U0001F1FF"
    r"\U0001F200-\U0001F2FF"
    r"]"
)

# Emoji token: bitta emoji + optional ZWJ-sequence + VS-16
EMOJI_TOKEN = re.compile(
    EMOJI_CLASS + r"(?:" + ZWJ + EMOJI_CLASS + r")*" + VS16 + r"?"
)

# Heading'da saqlanadigan emojilar (token'ning birinchi simvoli bilan match)
KEEP_HEADING = frozenset("🎯🏋✅🟢🟡🔴")

# Inline'da saqlanadigan emojilar (token'ning birinchi simvoli bilan match)
KEEP_INLINE = frozenset("🎯🏋✅❌🟢🟡🔴⭐💬📧🌐🐙💼")

# Jadval cell ichida matnga konvertatsiya
TABLE_REPLACEMENTS = [
    ("⚡⚡⚡", "Juda tez"),
    ("⚡⚡", "Tez"),
    ("\U0001F40C", "Sekin"),   # 🐌
]

CODE_FENCE = re.compile(r"^(\s*)(```|~~~)")
HEADING_LINE = re.compile(r"^#+\s")
TABLE_LINE = re.compile(r"^\s*\|")

# Hisobot uchun ro'yxat
INVENTORY_EMOJIS = [
    ("🎯", "saqlash"),
    ("✅", "saqlash"),
    ("❌", "saqlash"),
    ("🏋", "saqlash"),
    ("🟢", "saqlash"),
    ("🟡", "saqlash"),
    ("🔴", "saqlash"),
    ("⭐", "qisman saqlash"),
    ("💬", "kontakt"),
    ("📧", "kontakt"),
    ("🌐", "kontakt/heading"),
    ("🐙", "kontakt"),
    ("💼", "kontakt/heading"),
    ("🚀", "olib tashlash"),
    ("📚", "olib tashlash"),
    ("📖", "olib tashlash"),
    ("📦", "olib tashlash"),
    ("🧠", "olib tashlash"),
    ("💻", "olib tashlash"),
    ("🔌", "olib tashlash"),
    ("🎉", "olib tashlash"),
    ("💡", "olib tashlash"),
    ("📅", "olib tashlash"),
    ("🏆", "olib tashlash"),
    ("🎓", "olib tashlash"),
    ("🛠", "olib tashlash"),
    ("📋", "olib tashlash"),
    ("🏗", "olib tashlash"),
    ("📝", "olib tashlash"),
    ("🗂", "olib tashlash"),
    ("📊", "olib tashlash"),
    ("📈", "olib tashlash"),
    ("🔥", "olib tashlash"),
    ("🌟", "olib tashlash"),
    ("⚡", "jadval matnga"),
    ("🐌", "jadval matnga"),
]


def _replace_emoji(keep_set: frozenset[str], strip_space: bool):
    """Callback factory: agar token allowlist'da bo'lsa - keep, aks holda olib tashlash."""

    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        if token and token[0] in keep_set:
            return token
        return ""

    return replace


def clean_heading(line: str) -> str:
    """Heading qatorda allowlist'dan tashqari emojilarni olib tashlash."""
    cleaned = EMOJI_TOKEN.sub(_replace_emoji(KEEP_HEADING, False), line)
    cleaned = re.sub(r"^(#+)\s+", r"\1 ", cleaned)
    cleaned = re.sub(r"^(#+\s)\s+", r"\1", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.rstrip()


def clean_inline(line: str) -> str:
    """Inline qatorda allowlist'dan tashqari emojilarni olib tashlash."""
    # Emoji + keyingi optional space ni birga olib tashlash (artifact bo'lmasligi uchun)
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        if token and token[0] in KEEP_INLINE:
            return token
        # Token oxirida space bor edi - olib tashlash kerak
        return ""

    pattern = re.compile(EMOJI_TOKEN.pattern + r"[ \t]?")
    cleaned = pattern.sub(replace, line)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+([,.!?:;])", r"\1", cleaned)
    return cleaned.rstrip()


def clean_table(line: str) -> str:
    """Jadval cell'da ⚡/🐌 ni matnga aylantirish."""
    for src, dst in TABLE_REPLACEMENTS:
        line = line.replace(src, dst)
    return line.rstrip()


def process_text(text: str) -> tuple[str, bool]:
    lines = text.split("\n")
    new_lines: list[str] = []
    in_code = False
    code_pre: list[str] = []
    code_post: list[str] = []

    for line in lines:
        m = CODE_FENCE.match(line)
        if m:
            in_code = not in_code
            code_pre.append(line)
            code_post.append(line)
            new_lines.append(line)
            continue

        if in_code:
            code_pre.append(line)
            code_post.append(line)
            new_lines.append(line)
            continue

        if HEADING_LINE.match(line):
            new_lines.append(clean_heading(line))
        elif TABLE_LINE.match(line):
            new_lines.append(clean_table(line))
        else:
            new_lines.append(clean_inline(line))

    new_text = "\n".join(new_lines)
    code_safe = code_pre == code_post
    return new_text, code_safe


def count_emojis(text: str) -> dict[str, int]:
    return {e: text.count(e) for e, _ in INVENTORY_EMOJIS}


def report_file(path: Path, pre: str, post: str, code_safe: bool) -> None:
    pre_counts = count_emojis(pre)
    post_counts = count_emojis(post)
    changed = pre != post

    print(f"\n=== {path} ===")
    if not changed:
        print("  o'zgarish yo'q")
        return

    any_diff = False
    for emoji, role in INVENTORY_EMOJIS:
        if pre_counts[emoji] == 0 and post_counts[emoji] == 0:
            continue
        if pre_counts[emoji] == post_counts[emoji]:
            print(f"  {emoji} ({role}): {pre_counts[emoji]} = {post_counts[emoji]}")
        else:
            any_diff = True
            print(
                f"  {emoji} ({role}): {pre_counts[emoji]} -> {post_counts[emoji]}"
            )
    if not any_diff:
        print("  (faqat formatlash o'zgargan)")
    print(f"  code_safe: {code_safe}")


def collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description="Emoji tozalash skripti")
    parser.add_argument("--apply", action="store_true", help="O'zgarishlarni saqlash")
    parser.add_argument("--check", action="store_true", help="Dry-run, hisobot")
    parser.add_argument("paths", nargs="+", help="Fayl yoki papka yo'llari")
    args = parser.parse_args()

    if not (args.apply or args.check):
        print("--apply yoki --check tanlang", file=sys.stderr)
        return 2

    files = collect_files(args.paths)
    if not files:
        print("Hech qanday .md fayl topilmadi", file=sys.stderr)
        return 1

    bad_code: list[Path] = []
    changed_files: list[Path] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        new_text, code_safe = process_text(text)
        report_file(f, text, new_text, code_safe)
        if not code_safe:
            bad_code.append(f)
        if new_text != text:
            changed_files.append(f)
            if args.apply:
                f.write_text(new_text, encoding="utf-8")

    print()
    print("--- XULOSA ---")
    print(f"Tekshirilgan: {len(files)} ta")
    print(f"O'zgargan:   {len(changed_files)} ta")
    if bad_code:
        print(f"DIQQAT: code-block o'zgargan fayllar: {bad_code}")
    if args.apply:
        print("Saqlandi.")
    else:
        print("Dry-run (hech narsa yozilmadi). --apply qo'shing.")
    return 0 if not bad_code else 3


if __name__ == "__main__":
    raise SystemExit(main())
