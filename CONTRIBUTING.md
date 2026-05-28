# 🤝 Hissa qo'shish — Contributing Guide

Salom! **Backend to ML** loyihasiga qiziqqaningiz uchun rahmat. Bu kitob — **jamoaviy ish**, va sizning har qanday hissangiz (kichik imlo xatosidan tortib, yangi bobgacha) loyihani yanada yaxshiroq qiladi.

> 💡 Hech qachon open source'ga hissa qo'shmaganmisiz? Tashvishlanmang — bu yerda yangi boshlovchilarga **alohida e'tibor** beriladi. Savol bering, biz yordam beramiz.

---

## 📋 Mundarija

1. [Boshlashdan oldin](#boshlashdan-oldin)
2. [Hissa qo'shish turlari](#hissa-qoshish-turlari)
3. [Lokal sozlash](#lokal-sozlash)
4. [Branch va commit konvensiyasi](#branch-va-commit-konvensiyasi)
5. [Pull Request jarayoni](#pull-request-jarayoni)
6. [Kontent stil qo'llanmasi](#kontent-stil-qollanmasi)
7. [Yordam kerakmi?](#yordam-kerakmi)

---

<a id="boshlashdan-oldin"></a>
## 🚦 Boshlashdan oldin

Ishni boshlashdan oldin quyidagi qadamlarni bajaring:

1. ✅ **[Code of Conduct](CODE_OF_CONDUCT.md)** ni o'qing va unga amal qilishga va'da bering
2. 🔍 Mavjud **[issue'larni qidirib](https://github.com/JahongirHakimjonov/backend_to_ml/issues)** chiqing — balki kimdir o'sha muammoni allaqachon ko'tarib qo'ygandir
3. 💬 Katta o'zgarishlardan oldin **issue oching va muhokama qiling** — vaqtingizni behuda sarflamaslik uchun

---

<a id="hissa-qoshish-turlari"></a>
## 🎁 Hissa qo'shish turlari

Loyihaga **har xil yo'llar** bilan yordam berishingiz mumkin — kod yozishingiz shart emas:

| 🎯 Tur | 📝 Tasvir | 🛠️ Qanday qilish |
|--------|-----------|-------------------|
| ⭐ **Star qo'yish** | GitHub'da loyihaga star bering | Eng oson va eng samarali yo'l |
| 📢 **Ulashish** | Do'stlaringizga LinkedIn/Telegram'da aytib bering | `@jahongir-hakimjonov` ni tag qiling |
| 🐛 **Bug report** | Imlo xatosi, eskirgan kod, buzilgan havola | [Issue oching](https://github.com/JahongirHakimjonov/backend_to_ml/issues/new) |
| 💡 **Feature request** | Yangi bob, mashq yoki misol taklifi | [Feature request shabloni](.github/ISSUE_TEMPLATE/feature_request.md) |
| 📝 **Kontent yaxshilash** | Tushuntirish, misol, lug'at termin qo'shish | Pull Request |
| 🌍 **Tarjima** | Inglizcha/ruscha versiya ustida ishlash | Issue orqali muhokama |
| 🔧 **Pull Request** | Kod, hujjat yoki konfiguratsiya o'zgartirish | Quyidagi yo'riqnoma |
| 🏆 **Yangi bob** | To'liq yangi mavzu yozish | Avval issue orqali kelishish |

---

<a id="lokal-sozlash"></a>
## ⚙️ Lokal sozlash

### Talablar

- **Python**: `>=3.11` ([pyproject.toml](pyproject.toml) ga mos)
- **uv**: Astral'ning paket menejeri — [o'rnatish yo'riqnomasi](https://docs.astral.sh/uv/getting-started/installation/)
- **mdBook**: Rust asosidagi kitob generatori — [o'rnatish yo'riqnomasi](https://rust-lang.github.io/mdBook/guide/installation.html)
- **Git**: versiya boshqaruvi

### Qadam-baqadam

```bash
# 1. Fork qiling (GitHub UI orqali)

# 2. Klon qiling
git clone https://github.com/<sizning-username>/backend_to_ml.git
cd backend_to_ml

# 3. Upstream remote qo'shing
git remote add upstream https://github.com/JahongirHakimjonov/backend_to_ml.git

# 4. Python bog'liqliklarni o'rnating
uv sync

# 5. Kitobni lokal preview qiling
mdbook serve --open
# → http://localhost:3000 da brauzer ochiladi
```

### Notebook'lar bilan ishlash

```bash
# Jupyter notebook'larni ishga tushirish
uv run jupyter lab

# Yoki muayyan oy uchun (masalan, 1-oy)
uv sync --group month-01
```

---

<a id="branch-va-commit-konvensiyasi"></a>
## 🌿 Branch va commit konvensiyasi

### Branch nomi

| Prefiks | Ishlatilish | Misol |
|---------|-------------|-------|
| `feature/` | Yangi kontent yoki funksiya | `feature/chapter-cnn-attention` |
| `fix/` | Xato tuzatish | `fix/typo-month-03-readme` |
| `docs/` | Faqat hujjat o'zgartirish | `docs/update-contributing-guide` |
| `refactor/` | Kontent qayta tashkillash | `refactor/glossary-alphabetical` |

### Commit xabar konvensiyasi

Loyiha **[Conventional Commits](https://www.conventionalcommits.org/)** dan foydalanadi:

```text
<type>: <qisqa tasvir>

[ixtiyoriy batafsil tana]

[ixtiyoriy footer]
```

**Type'lar**:

- `docs:` — Hujjat o'zgartirish (eng ko'p ishlatiladi — bu kitob loyihasi!)
- `feat:` — Yangi bob, mashq yoki misol
- `fix:` — Xato tuzatish (imlo, kod, havola)
- `style:` — Formatlash, bo'sh joy o'zgartirish (mazmunga ta'sir qilmaydi)
- `refactor:` — Kontentni qayta tashkillash
- `chore:` — Build, konfiguratsiya, dependency yangilash

**Misollar**:

```bash
git commit -m "docs: add new section on transformers in month-04"
git commit -m "fix: correct PyTorch import in chapter 3-rnn"
git commit -m "feat: add CNN exercise (Hard level) to month-03"
git commit -m "chore: update mdbook config to enable search"
```

---

<a id="pull-request-jarayoni"></a>
## 🚀 Pull Request jarayoni

### 1. Branch yarating va o'zgartirishlar qiling

```bash
# Asosiy branchni yangilang
git checkout main
git pull upstream main

# Yangi branch yarating
git checkout -b docs/add-pytorch-example

# O'zgartirishlar qiling
mdbook serve --open  # preview
```

### 2. Commit va push

```bash
git add src/month-03/01-pytorch-basics.md
git commit -m "docs: add minimal pytorch example to month-03"
git push origin docs/add-pytorch-example
```

### 3. PR oching

GitHub'da **"Compare & pull request"** tugmasini bosing. PR tavsifida quyidagilarni yoziring:

- 🎯 **Maqsad** — bu PR nima qiladi?
- 📝 **O'zgartirishlar ro'yxati** — bullet point shaklida
- 🔗 **Bog'liq issue** — `Closes #123` formatida
- 📸 **Screenshot** (UI/preview o'zgarishlar bo'lsa)

### ✅ PR Checklist

Quyidagi qadamlarni bajarganingizga ishonch hosil qiling:

- [ ] **`mdbook build`** lokal'da xatosiz o'tdi
- [ ] **`mdbook serve --open`** orqali preview tekshirildi
- [ ] **Imlo va grammatika** tekshirildi (o'zbek tilida)
- [ ] **Kod misollar** `uv run` bilan ishlaydi
- [ ] **Havolalar** (link'lar) buzilmagan
- [ ] **`src/SUMMARY.md`** ga yangi bob qo'shildi (agar kerak bo'lsa)
- [ ] **Conventional Commits** formatida commit yozildi
- [ ] **Bir PR — bir mavzu** prinsipiga rioya qildim

---

<a id="kontent-stil-qollanmasi"></a>
## 🎨 Kontent stil qo'llanmasi

Bu kitob o'ziga xos **falsafa** va **stil**ga ega. Yangi kontent qo'shganda quyidagilarga e'tibor bering:

### 🇺🇿 Til

- **O'zbek tilida** yozing (lotin alifbosi)
- **Texnik terminlar** inglizcha qoldirilsin: `gradient descent`, `backpropagation`, `embedding`
- Agar termin uchun yaxshi o'zbekcha muqobil bor bo'lsa — qavs ichida bering: `tensor (ko'pchillik matritsa)`

### 💻 Kontent prinsipi

- **Code-first, theory-minimum** — har bob: tushuncha → minimal misol → mashq
- **Production-oriented** — "real ishda qanday ishlatiladi" perspektivasidan yozing
- **Backend dev fokus** — har bobda "FastAPI/Django integratsiyasi" bo'limi (mantiqiy bo'lganda)

### 📝 Bob strukturasi (taklif)

```markdown
# Bob nomi

## Nimani o'rganamiz?
- Bullet point shaklida 3-5 ta maqsad

## Tushuncha
Qisqa nazariya (1-2 paragraf, ortiqcha emas)

## Minimal misol
```python
# 10-30 qator kod, to'liq ishlaydigan
```

## FastAPI/Django integratsiyasi
Real backend kontekstida qanday ishlatiladi

## Mashqlar
- 🟢 Easy: ...
- 🟡 Medium: ...
- 🔴 Hard: ...

## Keyingi qadam
Bog'liq boblarga havola
```

### 🚫 Nima qilmaslik kerak

- ❌ Ortiqcha akademik nazariya — Andrew Ng kursida ko'rsin
- ❌ "Bu juda oson" yoki "har kim biladi" kabi iboralar
- ❌ Tasdiqlanmagan/eskirgan ma'lumotlar
- ❌ Inglizcha-o'zbekcha aralash gaplar (`siz training qildingiz` ❌ → `siz model'ni o'rgatdingiz` ✅)

---

<a id="yordam-kerakmi"></a>
## 💬 Yordam kerakmi?

Savol, taklif yoki yordam kerakmi? Quyidagi kanallarga murojaat qiling:

| 🎯 Maqsad | 📞 Kanal |
|-----------|---------|
| **Tezkor savol** | [Telegram @ja_khan_gir](https://t.me/ja_khan_gir) |
| **Rasmiy aloqa** | jahongirhakimjonov@gmail.com |
| **Bug yoki feature** | [GitHub Issues](https://github.com/JahongirHakimjonov/backend_to_ml/issues) |
| **Umumiy muhokama** | [GitHub Discussions](https://github.com/JahongirHakimjonov/backend_to_ml/discussions) (yaqinda ochiladi) |

---

## 🙏 Tashakkur

Har bir hissadorni **README.md** dagi "Contributors" bo'limida (yaqinda qo'shiladi) va kitobning kelajakdagi versiyalarida minnatdorlik bilan eslaymiz.

Sizning hissangiz — o'zbek tilidagi sifatli ML kontentini ko'paytirishga qo'shilgan **qadr**. Rahmat! ❤️

---

<div align="center">

**[← README ga qaytish](README.md)** · **[Code of Conduct](CODE_OF_CONDUCT.md)** · **[Security Policy](SECURITY.md)**

🚀 **Birga o'rganamiz, birga o'samiz!** 🚀

</div>
