#!/usr/bin/env bash
# po/messages.pot template fayl yaratish — manba src/ dan barcha msgid'larni chiqaradi.
# Foydalanish: ./scripts/extract-messages.sh
set -euo pipefail

cd "$(dirname "$0")/.."

MDBOOK_OUTPUT='{"xgettext": {}}' mdbook build -d po

if [ -f "po/xgettext/messages.pot" ]; then
    mv po/xgettext/messages.pot po/messages.pot
    rmdir po/xgettext 2>/dev/null || true
fi

echo "Yaratildi: po/messages.pot"
