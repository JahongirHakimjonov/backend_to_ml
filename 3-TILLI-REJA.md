# Backend to ML loyihasini 3 tilga (uz / ru / en) o'tkazish rejasi

## Context

**Hozirgi holat**: `/Users/jakhangir/MyStuff/PythonJob/my/backend_to_ml` — mdBook v0.4.40 asosida qurilgan 6 oylik "Backend to ML" roadmap kitobi. 67 ta markdown fayl, ~20,300 qator, 100% o'zbek tilida. `https://backendtoml.milliytech.uz` da GitHub Pages orqali deploy qilinadi.

**Maqsad**: Loyihaga rus (ru) va ingliz (en) tillarini qo'shish. O'zbek tili **asosiy/default** bo'lib qoladi, Google'da indekslangan mavjud URL'lar buzilmasligi shart.

**Tanlangan yondashuv**: `mdbook-i18n-helpers` (gettext + `.po` fayllar). Bu Google'ning [Comprehensive Rust](https://github.com/google/comprehensive-rust) kitobida qo'llanilgan industry-standard yechim. Tarjima `.po` fayllarda saqlanadi — AI tarjimon (Claude/DeepL/GPT) `.po` formatini native qo'llab-quvvatlaydi, sinxron tracking avtomatik (`msgmerge`).

**URL strukturasi**:
- `https://backendtoml.milliytech.uz/` → **uz** (default, mavjud SEO saqlanadi)
- `https://backendtoml.milliytech.uz/ru/` → ru
- `https://backendtoml.milliytech.uz/en/` → en

**Tarjima usuli**: AI (revisisiz). Ru va en parallel.

---

## 1. mdbook-i18n-helpers qanday ishlaydi

3 ta alohida `src/` katalog o'rniga, **yagona `src/`** (manba — o'zbek) va **`po/`** katalog `.po` fayllar bilan ishlatiladi.

**Workflow**:
1. `mdbook-xgettext` preprocessor markdown manbadan barcha tarjima qilinadigan stringlarni ajratib `po/messages.pot` ga yozadi (template fayl).
2. `msginit -i po/messages.pot -l ru -o po/ru.po` — yangi til uchun `.po` fayl yaratadi.
3. Tarjimon (yoki AI) `po/ru.po`, `po/en.po` fayllarini tahrirlaydi (har bir string uchun `msgstr ""` ga tarjima qo'shiladi).
4. Build vaqtida `mdbook-gettext` preprocessor `.po` fayldan tarjimani markdown ga injection qiladi.
5. Manba (o'zbek) o'zgarsa, `msgmerge po/ru.po po/messages.pot -U` bilan ru/en fayllarini sinxronlashtirish mumkin. Tarjima qilinmagan stringlar `fuzzy` belgisi bilan qoladi.

**Build buyrug'i** (har bir til alohida):
```bash
mdbook build -d book                                          # uz (default)
MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru              # ru
MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en              # en
```

Bu yondashuvning afzalliklari:
- **Yagona manba `src/`** — kontentni faqat bir joyda yangilaymiz.
- **AI uchun ideal**: `.po` fayllar `msgid`/`msgstr` juftliklari — Claude/DeepL bularni batch tarzda tarjima qila oladi.
- **Sinxron tracking**: manba o'zgarsa, qaysi ru/en stringlar eskirgani avtomatik aniqlanadi (`fuzzy` belgisi).
- **mdBook upgrade'ga chidamli**: official Google plugin'i, regular yangilanadi.

---

## 2. Tugatilgan fayl tuzilmasi

```
backend_to_ml/
├── book.toml                         # MODIFIKATSIYA — preprocessor.gettext qo'shiladi
├── src/                              # O'ZGARMAYDI — asl uz manbasi
│   ├── SUMMARY.md
│   ├── introduction.md
│   ├── ...67 ta fayl saqlanadi...
│   └── CNAME → o'chiriladi (workflow yaratadi)
├── theme/                            # MODIFIKATSIYA — head.hbs hreflang + lang switcher
│   ├── head.hbs                      # multilingual SEO (hreflang, og:locale alternates)
│   └── lang-switcher.js              # YANGI — additional-js
├── po/                               # YANGI — barcha tarjimalar
│   ├── messages.pot                  # avtomatik generatsiya (manbadan)
│   ├── ru.po                         # rus tarjimasi
│   └── en.po                         # ingliz tarjimasi
├── scripts/
│   ├── extract-messages.sh           # YANGI — po/messages.pot generatsiya
│   ├── sync-translations.sh          # YANGI — msgmerge bilan ru.po / en.po yangilash
│   ├── translate-with-ai.py          # YANGI — .po fayllarni AI bilan tarjima qilish
│   └── generate-sitemap.py           # YANGI — multilingual sitemap.xml + hreflang
├── .github/workflows/deploy.yml      # MODIFIKATSIYA — 3 til build + sitemap
├── book/                             # build output (gitignore)
│   ├── index.html                    # uz home
│   ├── month-01-foundations/...      # uz sahifalari (mavjud URL'lar saqlanadi)
│   ├── ru/                           # ru build
│   ├── en/                           # en build
│   ├── sitemap.xml                   # 3 til hreflang bilan
│   ├── robots.txt
│   └── CNAME
└── .gitignore                        # book/, *.mo qo'shiladi
```

**Eski tuzilmaning saqlanishi**: `src/` joyida qoladi, hech bir markdown fayl ko'chmaydi.

---

## 3. `book.toml` sozlamalari (yagona fayl, hammasi uchun)

```toml
[book]
title = "Backend to ML: 6 Oylik Roadmap"
authors = ["Jahongir Hakimjonov <jahongirhakimjonov@gmail.com>"]
description = "Middle Python backend developer uchun ML Engineer / MLOps Engineer bo'lish yo'li."
language = "uz"                       # BUG FIX — eski "en" emas, asl manba tili uz
src = "src"

[build]
build-dir = "book"
create-missing = false

[preprocessor.gettext]
after = ["links"]                     # YANGI — tarjima preprocessor

[output.html]
default-theme = "ayu"
preferred-dark-theme = "ayu"
mathjax-support = true
additional-js = ["theme/lang-switcher.js"]
git-repository-url = "https://github.com/JahongirHakimjonov/backend_to_ml"
edit-url-template = "https://github.com/JahongirHakimjonov/backend_to_ml/edit/main/{path}"

[output.html.print]
enable = true

[output.html.fold]
enable = true
level = 1

[output.html.search]
enable = true
limit-results = 30
teaser-word-count = 30
use-boolean-and = true
boost-title = 2
boost-hierarchy = 1
boost-paragraph = 1
expand = true
heading-split-level = 3
```

**Eslatma**: `site-url` qo'shilmaydi — build paytida environment variable orqali har bir til alohida `-d` flag bilan boshqariladi.

---

## 4. `.po` fayllar workflow

### `po/messages.pot` (template — auto-generated)

```
# po/messages.pot — manba template
msgid ""
msgstr ""
"Project-Id-Version: Backend to ML\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/introduction.md:1
msgid "Kirish"
msgstr ""

#: src/introduction.md:3
msgid "Salom, men Jahongir Hakimjonov..."
msgstr ""
```

### `po/ru.po` (tarjimadan keyin)

```
msgid "Kirish"
msgstr "Введение"

msgid "Salom, men Jahongir Hakimjonov..."
msgstr "Привет, я Джахонгир Хакимджонов..."
```

### Generatsiya buyruqlari (rasmiy USAGE.md dan)

`scripts/extract-messages.sh`:
```bash
#!/usr/bin/env bash
# .pot template yaratish — manba src/ dan barcha msgid'larni chiqaradi
set -euo pipefail
MDBOOK_OUTPUT='{"xgettext": {}}' mdbook build -d po
# Natija: po/messages.pot
```

`scripts/sync-translations.sh`:
```bash
#!/usr/bin/env bash
# Manba o'zgargandan keyin ru/en fayllarini yangilash
set -euo pipefail
./scripts/extract-messages.sh
for lang in ru en; do
  if [ -f "po/${lang}.po" ]; then
    msgmerge --update "po/${lang}.po" po/messages.pot
  else
    msginit -i po/messages.pot -l "${lang}" -o "po/${lang}.po" --no-translator
  fi
done
```

**Eslatma manba tili haqida**: rasmiy USAGE.md misol sifatida ingliz manbasini ko'rsatadi, lekin `gettext` standart format-agnostic — manba istalgan tilda bo'lishi mumkin. Bu loyihada manba **o'zbek** (`book.toml`'da `language = "uz"`), `.pot` fayl o'zbekcha `msgid`'lar bilan, ru/en — tarjima `msgstr`'lar bilan to'ldiriladi.

---

## 5. AI bilan tarjima — sifat va terminologiya nazorati

> **Kritik talab**: tarjima ma'nosi buzulmasligi, ML/MLOps atamalari to'g'ri va izchil qo'llanilishi shart. Quyidagi mexanizmlar shu uchun qurilgan.

### 5.1. Glossary (`po/glossary.yaml`) — eng muhim hujjat

Tarjimadan **avval** yaratiladi va manba sifatida ishlatiladi. Har bir kalit termin uchun standart ruscha va inglizcha ekvivalentlar belgilanadi.

```yaml
# po/glossary.yaml
terms:
  # ML asoslar
  - uz: "mashinaviy o'qitish"
    ru: "машинное обучение"
    en: "machine learning"
    note: "har doim shu tarjima, qisqartirish ML har 3 tilda ham qabul qilinadi"

  - uz: "chuqur o'qitish"
    ru: "глубокое обучение"
    en: "deep learning"

  - uz: "neyron tarmoq"
    ru: "нейронная сеть"
    en: "neural network"

  - uz: "o'qitish to'plami"
    ru: "обучающая выборка"
    en: "training set"

  - uz: "tasniflash"
    ru: "классификация"
    en: "classification"

  - uz: "regressiya"
    ru: "регрессия"
    en: "regression"

  - uz: "ortga tarqalish"
    ru: "обратное распространение ошибки"
    en: "backpropagation"

  - uz: "gradient tushishi"
    ru: "градиентный спуск"
    en: "gradient descent"

  - uz: "yo'qotish funksiyasi"
    ru: "функция потерь"
    en: "loss function"

  - uz: "ortiqcha moslashish"
    ru: "переобучение"
    en: "overfitting"

  - uz: "embedding"
    ru: "эмбеддинг"
    en: "embedding"

  # Backend / DevOps
  - uz: "ma'lumotlar bazasi"
    ru: "база данных"
    en: "database"

  - uz: "so'rov"
    ru: "запрос"
    en: "request"

  - uz: "javob"
    ru: "ответ"
    en: "response"

  - uz: "muhit o'zgaruvchisi"
    ru: "переменная окружения"
    en: "environment variable"

# Tarjima qilinmaydigan (do-not-translate)
do_not_translate:
  - Python
  - FastAPI
  - Django
  - DRF
  - scikit-learn
  - PyTorch
  - TensorFlow
  - Keras
  - NumPy
  - Pandas
  - Matplotlib
  - Seaborn
  - Jupyter
  - Docker
  - Kubernetes
  - MLflow
  - Airflow
  - Prefect
  - LangChain
  - LangGraph
  - RAG
  - LLM
  - GPU
  - CPU
  - API
  - REST
  - JSON
  - YAML
  - HuggingFace
  - OpenAI
  - Claude
  - Anthropic
  - GitHub
  - Git
  - SQL
  - NoSQL
  - Redis
  - PostgreSQL
  - MongoDB
  - AWS
  - GCP
  - Azure
```

### 5.2. `scripts/translate-with-ai.py` — pipeline

```
.po fayl → context-aware batching → Claude API + glossary inject → validation → .po yozish
```

**Qadamlar**:

1. **Kontekst yig'ish**: har bir `msgid` uchun manba markdown fayl yo'lini va abzas atrofini ham yuborish.
2. **Batching**: ~30 string per call. Glossary va do-not-translate ro'yxati har batch'da.
3. **System prompt** (har bir API call uchun):
   ```
   Sen "Backend to ML" texnik kitobining {ru|en} tarjimonisan. Manba — o'zbek tili.

   QATTIQ QOIDALAR:
   1. Ma'no aynan saqlanishi shart — qo'shimcha izoh qo'shma, qisqartirma.
   2. Quyidagi glossary'dagi atamalarni AYNAN belgilangan tarjimada ishlat: [glossary]
   3. Quyidagi so'zlar TARJIMA QILINMAYDI: [do_not_translate]
   4. Markdown sintaksisi 100% saqlanadi.
   5. Kod bloklari ICHIDAGI matn tarjima qilinmaydi.
   6. URL, fayl yo'llari, fayl nomlari o'zgarmaydi.
   7. HTML taglari saqlanadi.
   8. Emoji va maxsus belgilar saqlanadi.
   9. Ro'yxat va jadval tuzilmasi aynan ko'chiriladi.
   10. Texnik aniqlik > stilistik chiroy.
   ```
4. **Output validatsiya** (har bir tarjima yozilgunga qadar):
   - Markdown tuzilma diff (bold, code, link belgilari soni mos)
   - Kod bloklar soni mos
   - Link target'lari aynan saqlanishi
   - HTML taglar saqlanishi
   - Emoji saqlanishi
   - `do_not_translate` ro'yxatidagi so'zlar tarjimada ham bo'lishi
   - Glossary qo'llanilishi

   Validatsiya muvaffaqiyatsiz bo'lsa: string `fuzzy` deb belgilanadi va `po/needs-review.txt` ga yoziladi.

5. **Multi-pass strategiyasi**:
   - **Pass 1**: barcha stringlar dastlabki tarjimasi
   - **Pass 2**: glossary consistency check
   - **Pass 3** (sarlavhalar va kalit abzaslar): qisqartirilgan AI sanity check

### 5.3. `scripts/validate-translation.py` — bog'liq tekshiruv

`mdbook build` chaqirilishidan oldin ishga tushadi. Tekshiradi:
- Markdown tuzilma izchilligi
- Link bo'shliqlari
- Kod bloklar saqlanishi
- Glossary izchilligi

Xato topilsa, build to'xtaydi (CI'da ham).

### 5.4. Spot-check namunalar

Har bir Bosqich 5 iteratsiyasidan keyin (har oy bo'yicha):
- 5 ta tasodifiy abzas tanlanadi (`shuf -n 5`)
- Qo'lda o'qib chiqiladi (ru va en)
- ML termin to'g'riligi tekshiriladi
- Topilgan xatolar → glossary'ga qo'shimcha → qayta tarjima

### 5.5. Texnik dependency

`pyproject.toml` ga qo'shiladi:
```toml
dependencies = [
    "polib>=1.2.0",
    "anthropic>=0.40.0",
    "pyyaml>=6.0",
    "markdown-it-py>=3.0",
]
```

### 5.6. Tarjima sifatining quvuri

```
src/*.md (o'zbek manba)
   ↓
mdbook-xgettext → po/messages.pot
   ↓
msgmerge → po/ru.po, po/en.po
   ↓
po/glossary.yaml ← src/glossary.md (qo'lda kengaytiriladi)
   ↓
scripts/translate-with-ai.py
   - System prompt + glossary + do-not-translate
   - Per-string kontekst
   - Multi-pass (rough → glossary refine → sanity)
   - Validatsiya (markdown, link, kod, emoji)
   ↓
po/ru.po, po/en.po (to'ldirilgan)
   ↓
scripts/validate-translation.py
   ↓
mdbook build → book/ru/, book/en/
   ↓
Spot-check (har oy bo'yicha 5 abzas qo'lda revisi)
   ↓
Glossary yangilash → fuzzy stringlar qayta tarjima
```

---

## 6. GitHub Actions workflow (`.github/workflows/deploy.yml`)

```yaml
name: Deploy multilingual mdBook to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      MDBOOK_VERSION: 0.4.40
      MDBOOK_I18N_HELPERS_VERSION: 0.3.6
    steps:
      - uses: actions/checkout@v4

      - uses: Swatinem/rust-cache@v2

      - name: Install Rust + mdBook + i18n helpers
        run: |
          curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain none
          rustup toolchain install stable --profile minimal
          cargo install --version ${MDBOOK_VERSION} mdbook
          cargo install --version ${MDBOOK_I18N_HELPERS_VERSION} mdbook-i18n-helpers

      - name: Install gettext
        run: sudo apt-get update && sudo apt-get install -y gettext

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Build UZ (default)
        run: mdbook build -d book

      - name: Build RU
        run: MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru

      - name: Build EN
        run: MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en

      - name: Generate multilingual sitemap
        run: python3 scripts/generate-sitemap.py

      - name: Create robots.txt + CNAME
        run: |
          cat > book/robots.txt <<EOF
          User-agent: *
          Allow: /
          Sitemap: https://backendtoml.milliytech.uz/sitemap.xml
          EOF
          echo "backendtoml.milliytech.uz" > book/CNAME

      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./book

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

---

## 7. SEO — `theme/head.hbs` (hreflang)

```hbs
{{!-- Canonical va hreflang — multilingual SEO --}}
{{#if language}}
  {{#if (eq language "uz")}}
    <link rel="canonical" href="https://backendtoml.milliytech.uz/{{ path }}">
    <meta property="og:locale" content="uz_UZ">
  {{else if (eq language "ru")}}
    <link rel="canonical" href="https://backendtoml.milliytech.uz/ru/{{ path }}">
    <meta property="og:locale" content="ru_RU">
  {{else if (eq language "en")}}
    <link rel="canonical" href="https://backendtoml.milliytech.uz/en/{{ path }}">
    <meta property="og:locale" content="en_US">
  {{/if}}
{{/if}}

<link rel="alternate" hreflang="uz" href="https://backendtoml.milliytech.uz/{{ path }}">
<link rel="alternate" hreflang="ru" href="https://backendtoml.milliytech.uz/ru/{{ path }}">
<link rel="alternate" hreflang="en" href="https://backendtoml.milliytech.uz/en/{{ path }}">
<link rel="alternate" hreflang="x-default" href="https://backendtoml.milliytech.uz/{{ path }}">

<meta property="og:locale:alternate" content="ru_RU">
<meta property="og:locale:alternate" content="en_US">
```

---

## 8. Til o'zgartirgich (`theme/lang-switcher.js`)

Navbar'ga dropdown qo'shadi. URL prefiksini `<html lang>` atributidan aniqlaydi:

```javascript
(function() {
  const LANGS = [
    { code: 'uz', label: "O'zbek",  prefix: '' },
    { code: 'ru', label: 'Русский', prefix: '/ru' },
    { code: 'en', label: 'English', prefix: '/en' }
  ];

  const currentLang = document.documentElement.lang || 'uz';
  const currentLangCfg = LANGS.find(l => l.code === currentLang) || LANGS[0];

  function pathWithoutPrefix() {
    let p = window.location.pathname;
    if (currentLangCfg.prefix && p.startsWith(currentLangCfg.prefix)) {
      p = p.slice(currentLangCfg.prefix.length);
    }
    return p || '/';
  }

  function build() {
    const path = pathWithoutPrefix();
    const select = document.createElement('select');
    select.className = 'lang-switcher';
    select.style.cssText = 'margin-left:1rem;background:transparent;color:inherit;border:1px solid currentColor;padding:0.25rem 0.5rem;border-radius:4px;cursor:pointer;';
    LANGS.forEach(l => {
      const opt = document.createElement('option');
      opt.value = l.prefix + path;
      opt.textContent = l.label;
      if (l.code === currentLang) opt.selected = true;
      select.appendChild(opt);
    });
    select.addEventListener('change', e => {
      const sel = LANGS.find(l => (l.prefix + path) === e.target.value);
      if (sel) localStorage.setItem('preferred-lang', sel.code);
      window.location.href = e.target.value;
    });
    return select;
  }

  function inject() {
    const target = document.querySelector('.right-buttons') || document.querySelector('.menu-bar');
    if (target) target.appendChild(build());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
```

---

## 9. Migration bosqichlari (xavfsiz, regressiyasiz)

Har bir bosqich alohida commit/deploy. Eski URL'lar har bir bosqichdan keyin ishlashi tekshiriladi.

### Bosqich 0 — `book.toml` bug fix + Handlebars verifikatsiya
- `book.toml`: `language = "en"` → `language = "uz"`
- **VERIFIKATSIYA A**: `theme/head.hbs` ga vaqtinchalik `<!-- LANG_VAR_TEST: {{ language }} -->` commenti qo'shish, `mdbook build`, `grep "LANG_VAR_TEST" book/index.html`:
  - Agar `LANG_VAR_TEST: uz` chiqsa → variable ishlaydi, 7-bo'lim strategiyasi to'g'ri
  - Agar `LANG_VAR_TEST: {{ language }}` literal qolsa → fallback: per-language `theme-uz/`, `theme-ru/`, `theme-en/` kataloglar
  - Vaqtinchalik comment olib tashlash
- Local: `<html lang="uz">` borligini tekshirish
- Deploy va `curl -s https://backendtoml.milliytech.uz/ | grep '<html lang'` — `uz`

### Bosqich 1 — `mdbook-i18n-helpers` + o'zbek manba sanity check
- `cargo install mdbook-i18n-helpers --version 0.3.6`
- `gettext` paketi (msgmerge, msginit) — `brew install gettext`
- `book.toml` ga `[preprocessor.gettext]` qo'shish
- `scripts/extract-messages.sh` yaratish va ishga tushirish → `po/messages.pot`
- **VERIFIKATSIYA B**: `po/messages.pot` ichini ko'zdan kechirish:
  - O'zbekcha apostrof (`'`) `msgid`'larda buzilmasdan ko'chirilganmi
  - Qo'sh tirnoq escape qilingan holatda saqlanganmi
  - O'zbekcha so'zlar sentence boundary bo'yicha to'g'ri ajratilganmi
  - Agar buzilish bo'lsa, A-variantga (3 ta alohida `src/`) o'tish kerak
- `msginit -i po/messages.pot -l ru -o po/ru.po --no-translator`
- `msginit -i po/messages.pot -l en -o po/en.po --no-translator`
- **VERIFIKATSIYA C**: `MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru`, `grep '<html lang' book/ru/index.html`:
  - Agar `lang="ru"` chiqsa → env var to'g'ri ta'sir qiladi
  - Agar `lang="uz"` qolsa → qo'shimcha sozlash kerak
- **Bu bosqichda deploy qilinmaydi**, faqat lokal sinov

### Bosqich 2 — GitHub Actions multilingual build + build izolyatsiya
- `.github/workflows/deploy.yml` yangilash
- `theme/head.hbs` ga hreflang taglari
- `scripts/generate-sitemap.py` qo'shish
- `src/CNAME` o'chirish, workflow'da yaratish
- `.gitignore` ga `book/` qo'shish
- **VERIFIKATSIYA D** (build izolyatsiya — local):
  ```bash
  rm -rf book/
  mdbook build -d book
  MDBOOK_BOOK__LANGUAGE=ru mdbook build -d book/ru
  MDBOOK_BOOK__LANGUAGE=en mdbook build -d book/en
  ls book/index.html book/ru/index.html book/en/index.html
  ```
  - Hammasi mavjud bo'lishi shart
- Deploy → `/ru/` va `/en/` URL'lari ishlashi
- **Regressiya sinovi**: eski URL'lar hamon 200

### Bosqich 3 — Til o'zgartirgich
- `theme/lang-switcher.js` yaratish
- `book.toml` ga `additional-js`
- Lokalda dropdown sinovi
- Deploy va browser sinovi

### Bosqich 4 — Glossary va tarjima infratuzilmasi (kontentdan oldin!)
**Maqsad**: sifat asosi qurish.

- `po/glossary.yaml` qo'lda yaratish — 5.1 dagi YAML namuna
- `src/glossary.md` dan ML/MLOps kalit terminlarni ajratish
- `scripts/extract-glossary.py` — frequency analysis
- `scripts/translate-with-ai.py` — 5.2 da batafsil
- `scripts/validate-translation.py` — markdown, link, kod izchilligi
- `pyproject.toml` ga deps qo'shish
- `ANTHROPIC_API_KEY` `.env` ga

### Bosqich 5 — Phase 1 tarjima + tekshiruv (faqat 8 fayl)
**Pilot**: katta tarjima boshlashdan oldin sinov.

- Phase 1: SUMMARY, introduction, about-author, 6 ta `month-XX/README.md`
- `translate-with-ai.py --pilot`
- **Sifat audit**: tarjima qilingan har bir abzasni qo'lda o'qish (~2-3 soat)
- Glossary kengaytirish, `fuzzy` stringlar qayta tarjima
- Deploy va browser sinovi

### Bosqich 6 — Qolgan kontent (oy-oy bo'yicha, parallel ru + en)

Har oy iteratsiyasi:
1. `translate-with-ai.py --filter "month-01-*"`
2. `validate-translation.py`
3. **Spot-check**: 5 ta tasodifiy abzas
4. Glossary kengaytirish
5. `fuzzy` stringlar qayta tarjima
6. Local build (3 til)
7. Browser sinovi
8. Commit: `git commit -m "translate: month-XX → ru, en"`
9. Deploy

Tartib: Oy 1 → Oy 2 → ... → Oy 6 → `final-projects/` → `resources/` → `glossary.md`.

### Bosqich 7 — SEO verifikatsiya va Google Search Console
- `sitemap.xml` ni GSC ga qo'shish
- hreflang xatolarini tekshirish
- Lighthouse audit har 3 til uchun

---

## 10. Tarjima qilinmagan stringlarning fallback

`mdbook-gettext` default xulqi: `msgstr` bo'sh bo'lsa, manba `msgid` (o'zbekcha matn) ko'rsatiladi. Demak, qisman tarjima qilingan ru/en sahifalar sinmaydi — faqat tarjima qilinmagan abzaslar o'zbekcha qoladi.

---

## 11. Verifikatsiya (test plan)

### Avtomatik regressiya sinovi
```bash
URLS=(
  "/"
  "/introduction.html"
  "/month-01-foundations/01-math-basics.html"
  "/month-06-mlops-production/08-airflow-prefect.html"
  "/final-projects/project-1-prediction-api.html"
  "/glossary.html"
)
for u in "${URLS[@]}"; do
  code=$(curl -o /dev/null -s -w "%{http_code}" "https://backendtoml.milliytech.uz$u")
  [ "$code" = "200" ] || echo "BROKEN: $u → $code"
done
```

### Bosqich 2 dan keyin
- `/ru/`, `/en/` → 200
- `lang="ru"` ru sahifalarda
- `hreflang="ru"` uz sahifalarda

### Bosqich 3 dan keyin
- Navbar dropdown ko'rinishi
- Til o'zgartirish ishlashi
- localStorage saqlash

### Bosqich 4+ dan keyin
- Tarjima qilingan kontent ko'rsatilishi
- Tarjima qilinmagan abzaslar o'zbekcha (fallback)
- mdBook search per-language

### SEO sinovi
- `sitemap.xml` valid + hreflang
- GSC International Targeting xatolarsiz
- Lighthouse SEO ≥ 95

---

## 12. Kritik fayllar

**Modifikatsiya qilinadigan**:
- `book.toml` — `language = "uz"` + `[preprocessor.gettext]` + `additional-js`
- `theme/head.hbs` — hreflang, canonical, og:locale alternates
- `.github/workflows/deploy.yml` — 3 til build, sitemap, robots, CNAME
- `.gitignore` — `book/`, `*.mo` qo'shiladi
- `pyproject.toml` — `polib`, `anthropic` deps

**Yangi yaratiladigan**:
- `theme/lang-switcher.js`
- `po/messages.pot` (avtomatik)
- `po/ru.po`, `po/en.po`
- `po/glossary.yaml` — **sifat asosi**
- `po/needs-review.txt`
- `scripts/extract-messages.sh`
- `scripts/sync-translations.sh`
- `scripts/translate-with-ai.py`
- `scripts/validate-translation.py`
- `scripts/extract-glossary.py`
- `scripts/generate-sitemap.py`

**O'chiriladigan**:
- `src/CNAME` (workflow'da generatsiya qilinadi)

**O'zgarmaydigan**:
- `src/` ichidagi **barcha 67 ta markdown fayl** — joyida qoladi.

---

## 13. Risklar va yumshatish

1. **cargo install vaqti** — GitHub Actions'da 3-5 daqiqa. Yumshatish: `Swatinem/rust-cache@v2`.
2. **`.po` fayl katta o'lchami** — ~30,000 qator. Git history o'sadi, kritik emas.
3. **AI tarjima sifati va atamalar izchilligi** — eng katta risk:
   - `po/glossary.yaml` qattiq qoida
   - `do_not_translate` ro'yxati
   - Multi-pass tarjima
   - Validatsiya skripti
   - Per-string kontekst
   - Spot-check har iteratsiyada
   - Phase 1 pilot
4. **Ma'no buzilishi (semantic drift)**:
   - System prompt qattiq qoidasi
   - Per-string kontekst
   - Pass 3 sanity check
   - Qo'lda audit
5. **Terminologiya drift**:
   - Glossary qattiq belgilangan
   - Pass 2 consistency check
   - Build oldi validatsiya
6. **`{{ language }}` Handlebars variable** — Bosqich 0 Verifikatsiya A da tekshiriladi
7. **Markdown tuzilma buzilishi** — `validate-translation.py` taqqoslaydi

---

## 14. Boshlash tartibi va vaqt baholash

1. **Bosqich 0** (book.toml fix + Verifikatsiya A) — 30 daqiqa
2. **Bosqich 1** (i18n helpers + Verifikatsiya B, C) — 1.5 soat
3. **Bosqich 2** (workflow + Verifikatsiya D) — 2 soat
4. **Bosqich 3** (lang switcher UI) — 1 soat
5. **Bosqich 4** (glossary, tarjima skriptlari) — **3-4 soat**
6. **Bosqich 5** (Phase 1 pilot — 8 fayl) — **3-4 soat**
7. **Bosqich 6** (qolgan kontent, oy-oy) — **6-8 kun**
8. **Bosqich 7** (SEO, GSC) — 1 soat

**Eng kritik nuqtalar**:
- Bosqich 0 va 2 dan keyin mavjud URL'lar **buzilmasligi**
- **Bosqich 1 Verifikatsiya B** — abort nuqtasi (A-variantga o'tish)
- Bosqich 4 da **glossary sifati** muhim
- Bosqich 5 (pilot) **bekor qilish nuqtasi**
- Bosqich 6 da spot-check **o'tkazib yuborilmasligi** kerak

### "Revisisiz" rejimning aniq talqini

**Qo'lda revisi qilinadi**:
- `po/glossary.yaml` — bir martalik investitsiya
- Bosqich 5 pilot — 8 fayl qo'lda audit
- Har oy yakuni — 5 ta tasodifiy abzas spot-check
- `po/needs-review.txt` — validatsiya fail bo'lganlar

**Qo'lda revisi QILINMAYDI**:
- Qolgan ~99% kontentning tarjimasi — AI output to'g'ridan-to'g'ri ishlatiladi
- Stilistik nozikliklar

### Byudjet (AI tarjima)

~30,000 string × 2 til × 2 pass = ~120,000 API call:
- **Claude Haiku 4.5** (tavsiya): ~$30-60 jami
- **Claude Sonnet 4.6**: ~$150-300 jami

Haiku ML kontent va atamalar uchun yetarli darajada aniq.

---

## 15. Keyingi qadamlar

1. Reja tasdiqlangan (bu fayl)
2. Implementation Bosqich 0 dan boshlanadi (`book.toml` `language = "en"` → `"uz"` + Verifikatsiya A)
3. Har bir bosqichdan keyin regressiya sinovi
4. Bosqich 1 Verifikatsiya B muvaffaqiyatsiz bo'lsa, A-variantga o'tish

Tegishli fayllar:
- Asl reja nusxasi: `/Users/jakhangir/.claude-shaxsiy/plans/ushbu-loyihani-3ta-tilda-mutable-cookie.md`
- Loyiha katalogi: `/Users/jakhangir/MyStuff/PythonJob/my/backend_to_ml/`
- Mavjud sayt: `https://backendtoml.milliytech.uz/`
