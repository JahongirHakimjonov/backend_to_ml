#!/usr/bin/env bash
# mdBook {{ path }} variable .md extension qaytaradi, lekin actual URL'lar .html.
# Bu skript build/ ichidagi barcha HTML fayllarda canonical, hreflang, og:url
# href atributlarini .md → .html ga, va /index.html → / ga o'zgartiradi.
set -euo pipefail

BOOK_DIR="${1:-book}"
cd "$(dirname "$0")/.."

if [ ! -d "${BOOK_DIR}" ]; then
    echo "Katalog topilmadi: ${BOOK_DIR}" >&2
    exit 1
fi

# macOS vs GNU sed
SED_INPLACE=(sed -i)
if sed --version 2>/dev/null | grep -q "GNU"; then
    SED_INPLACE=(sed -i)
else
    SED_INPLACE=(sed -i '')
fi

# .md → .html (faqat href= ichidagi)
find "${BOOK_DIR}" -name "*.html" -print0 | xargs -0 "${SED_INPLACE[@]}" -E \
    -e 's|(href="https://backendtoml\.milliytech\.uz[^"]*)\.md"|\1.html"|g'

# /index.html → / (canonical va og:url uchun)
find "${BOOK_DIR}" -name "*.html" -print0 | xargs -0 "${SED_INPLACE[@]}" -E \
    -e 's|(href="https://backendtoml\.milliytech\.uz[^"]*)/index\.html"|\1/"|g'

echo "Canonical URL'lar tuzatildi: ${BOOK_DIR}/"
