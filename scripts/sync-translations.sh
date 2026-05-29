#!/usr/bin/env bash
# Manba o'zgargandan keyin ru.po va en.po fayllarini yangilash.
# Yangi msgid'lar qo'shiladi, eskirganlari `#~` bilan belgilanadi,
# o'zgarganlari `fuzzy` belgisini oladi (msgmerge default xulqi).
set -euo pipefail

cd "$(dirname "$0")/.."

./scripts/extract-messages.sh

for lang in ru en; do
    if [ -f "po/${lang}.po" ]; then
        echo "Yangilanmoqda: po/${lang}.po"
        msgmerge --update --backup=none "po/${lang}.po" po/messages.pot
    else
        echo "Yaratilmoqda: po/${lang}.po"
        msginit --input=po/messages.pot --locale="${lang}" \
                --output=po/"${lang}.po" --no-translator
    fi
done

echo "Tugadi."
