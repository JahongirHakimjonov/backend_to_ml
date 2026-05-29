#!/usr/bin/env python3
"""Multilingual sitemap.xml generatsiya, hreflang annotations bilan.

book/ ichida 3 til mavjudligi taxmin qilinadi: book/ (uz), book/ru/, book/en/.
Faqat haqiqatda mavjud fayllar uchun hreflang qo'shiladi (tarjima qilinmaganlar uchun emas).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent / "book"
BASE_URL = "https://backendtoml.milliytech.uz"
LANGS = [
    ("uz", ""),       # default, root
    ("ru", "/ru"),
    ("en", "/en"),
]
EXCLUDE_SUFFIXES = ("print.html", "404.html")


def collect_pages(root: Path) -> list[str]:
    """Berilgan katalogdagi HTML sahifalarning relative path'larini qaytaradi."""
    if not root.exists():
        return []
    pages: list[str] = []
    for html in sorted(root.rglob("*.html")):
        # ru/, en/ sub-buildlarni uz ro'yxatiga qo'shmaslik
        try:
            rel = html.relative_to(root).as_posix()
        except ValueError:
            continue
        if rel.startswith(("ru/", "en/")):
            continue
        if rel.endswith(EXCLUDE_SUFFIXES):
            continue
        if rel == "index.html":
            rel = ""
        elif rel.endswith("/index.html"):
            rel = rel[: -len("index.html")]
        pages.append(rel)
    return pages


def page_exists_for_lang(page: str, lang_prefix: str) -> bool:
    """Tilga xos versiyada sahifa fayli mavjudligini tekshiradi."""
    sub = lang_prefix.lstrip("/")
    base = BOOK_DIR if not sub else BOOK_DIR / sub
    if not page or page.endswith("/"):
        return (base / page / "index.html").exists()
    return (base / page).exists()


def main() -> None:
    if not BOOK_DIR.exists():
        raise SystemExit(f"book/ topilmadi: {BOOK_DIR}. Avval `mdbook build` ishlatilsin.")

    uz_pages = collect_pages(BOOK_DIR)
    today = datetime.now(timezone.utc).date().isoformat()

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    for page in uz_pages:
        loc_uz = f"{BASE_URL}/{page}" if page else f"{BASE_URL}/"
        out.append("  <url>")
        out.append(f"    <loc>{loc_uz}</loc>")
        out.append(f"    <lastmod>{today}</lastmod>")
        for code, prefix in LANGS:
            if not page_exists_for_lang(page, prefix):
                continue
            href = f"{BASE_URL}{prefix}/{page}" if page else f"{BASE_URL}{prefix}/"
            out.append(f'    <xhtml:link rel="alternate" hreflang="{code}" href="{href}"/>')
        out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc_uz}"/>')
        out.append("  </url>")

    out.append("</urlset>")

    sitemap = BOOK_DIR / "sitemap.xml"
    sitemap.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Yaratildi: {sitemap} ({len(uz_pages)} sahifa)")


if __name__ == "__main__":
    main()
