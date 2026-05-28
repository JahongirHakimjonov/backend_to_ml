# 🔒 Xavfsizlik siyosati — Security Policy

Loyihaning xavfsizligini ta'minlashda yordam berganingiz uchun **rahmat!** Quyidagi yo'riqnoma sizga zaifliklarni mas'uliyatli ravishda xabar berishga yordam beradi.

---

## 📦 Qo'llab-quvvatlanadigan versiyalar

Hozircha loyiha aktiv rivojlanish bosqichida. Quyidagi versiyalar uchun xavfsizlik yangilanishlari taqdim etiladi:

| Versiya | Qo'llab-quvvatlanadi |
|---------|----------------------|
| `main` (aktiv branch) | ✅ Ha |
| `v1.x` (kelajakda) | ✅ Ha (chiqarilgandan keyin) |
| Eski tag'lar / fork'lar | ❌ Yo'q |

> ℹ️ Bu kitob loyihasi (mdBook), shuning uchun ko'pchilik "xavfsizlik" masalalar — bu **kod misollardagi xatolar**, **bog'liqliklardagi (dependency) CVE'lar** yoki **buzilgan tashqi havolalar**. Klassik web/backend zaifliklari bu loyiha uchun kam ahamiyatli.

---

## 🚨 Zaiflikni qanday xabar berish kerak?

### ❌ NIMA QILMASLIK kerak

- **Ommaviy GitHub Issue OCHMANG** — zaiflik haqida ochiq xabar zarar yetkazishi mumkin
- Telegram'ning **ommaviy guruhlarida** muhokama qilmang
- Zaiflikni **boshqalar bilan oshkora ulashmang** (fix chiqqunga qadar)

### ✅ NIMA QILISH kerak

Zaiflik haqida **shaxsiy kanallar** orqali bizga xabar bering:

| Kanal | Aloqa | Tavsiya etilgan vaziyat |
|-------|-------|-------------------------|
| 📧 **Email** | jahongirhakimjonov@gmail.com | Asosiy kanal — barcha hisobotlar uchun |
| 💬 **Telegram** | [@ja_khan_gir](https://t.me/ja_khan_gir) | Shoshilinch (kritik darajadagi) zaifliklar uchun |

**Email mavzusi (subject)** quyidagi formatda bo'lsin:

```text
[SECURITY] backend_to_ml — <qisqa tavsif>
```

Masalan: `[SECURITY] backend_to_ml — outdated dependency in month-05`

---

## 📝 Xabarda nima bo'lishi kerak?

Hisobotingizda quyidagi ma'lumotlarni iloji boricha **batafsil** taqdim eting:

### 1. 🎯 Zaiflik turi

- [ ] Kod misolda xavfsiz amaliyot (SQL injection, XSS, command injection misoli)
- [ ] Bog'liqlikda CVE (dependency vulnerability)
- [ ] Infrastruktura/build jarayoni
- [ ] Maxfiy ma'lumot oshkor bo'lishi (.env, key, token)
- [ ] Boshqa: _________________

### 2. 📍 Joylashuv

- **Fayl yo'li**: `src/month-XX/example-Y.md`
- **Qator raqami** (agar aniq bo'lsa)
- **Bog'liqlik nomi va versiyasi** (CVE bo'lsa)

### 3. 🔄 Reproduce qadamlari

```text
1. ...
2. ...
3. Kutilgan natija: ...
4. Haqiqiy natija (zaiflik): ...
```

### 4. 💥 Ta'sir baholash

- **Kim ta'sir qilinadi?** (kitobni o'qiyotgan o'rganuvchilar, kodni production'da ishlatadigan kishilar va h.k.)
- **Qanday zarar yetishi mumkin?** (ma'lumot oshkor, kod bajarilishi, RCE va h.k.)
- **Severity (sizning bahoyingizcha)**: Critical / High / Medium / Low

### 5. 🛠️ Taklif qilingan yechim (ixtiyoriy)

Agar fikringiz bo'lsa — qanday tuzatish mumkin?

---

## ⏱️ Javob vaqti (SLA)

Biz quyidagi muddatlarda javob qaytarishga harakat qilamiz:

| Bosqich | Vaqt | Tasvir |
|---------|------|--------|
| **Birinchi javob** | 48 soat ichida | Hisobot olinganligini tasdiqlash |
| **Dastlabki baholash** | 7 kun ichida | Zaiflikning haqiqiyligini va severity'ni baholash |
| **Fix yoki rejim** | Severity'ga qarab: |
| └ Critical | 7 kun ichida | Tezkor patch |
| └ High | 14 kun ichida | Prioritet fix |
| └ Medium | 30 kun ichida | Keyingi release'da |
| └ Low | 90 kun ichida | Mos vaqtda |

> ℹ️ Bu — **shaxsiy loyiha** (bir kishi tomonidan saqlanadi), shuning uchun ba'zida javob biroz kechikishi mumkin. Sabringiz uchun rahmat!

---

## 🤝 Disclosure siyosati (Coordinated Disclosure)

Biz **coordinated (responsible) disclosure** prinsipiga amal qilamiz:

1. **Siz hisobot berasiz** — biz tasdiqlaymiz
2. **Birga muhokama qilamiz** — fix tayyorlanadi
3. **Fix chiqariladi** — yangi versiya/commit e'lon qilinadi
4. **Ommaviy e'lon** — fix chiqqandan **keyin** zaiflik haqida ochiq yoziladi
5. **Kredit beriladi** — sizning ismingiz (agar xohlasangiz) tashakkur ro'yxatida eslatiladi

### Embargo muddati

Standart holatda — **90 kun** (sanoat standarti). Agar zaiflik allaqachon ommaviy ekspluatatsiya qilinayotgan bo'lsa — qisqartirilishi mumkin.

---

## 🏆 Tashakkur (Hall of Fame)

Mas'uliyatli ravishda zaiflik xabari bergan tadqiqotchilarga **alohida minnatdorlik** bildiramiz:

- Ismingiz / GitHub username'ingiz `README.md` ning "Security Researchers" bo'limida eslatiladi (xohlasangiz)
- CHANGELOG yoki release notes'da kredit beriladi
- Telegram orqali shaxsiy minnatdorlik xabari

> ℹ️ Bug bounty (pulli mukofot) **mavjud emas** — bu bepul, open source loyiha. Lekin sizning hissangiz **qadrlanadi** va eslab qolinadi.

---

## 📚 Qo'shimcha resurslar

- 🛡️ [OWASP Top 10](https://owasp.org/Top10/) — eng keng tarqalgan web zaifliklar
- 🐍 [Python Security Best Practices](https://snyk.io/learn/python-security/)
- 🤖 [OWASP ML Top 10](https://owasp.org/www-project-machine-learning-security-top-10/) — ML modellar uchun
- 📦 [Snyk Vulnerability DB](https://security.snyk.io/) — bog'liqliklarni tekshirish

---

## ❓ Tez-tez so'raladigan savollar

<details>
<summary><b>Bu kitob loyihasida qanday "xavfsizlik" masalalari bo'lishi mumkin?</b></summary>

- 🔓 Kod misollarda `eval()`, `pickle.load()` kabi xavfli funksiyalarning izohsiz ishlatilishi
- 🔑 Misollarda haqiqiy API key, parol yoki token oshkor bo'lishi
- 📦 `pyproject.toml` da eskirgan, CVE'siga ega bog'liqliklar
- 🌐 Buzilgan yoki zararli tashqi havolalar (man-in-the-middle hujumlar uchun)
- 🤖 ML modellarni production'da xavfsiz deploy qilish bo'yicha noto'g'ri tavsiyalar

</details>

<details>
<summary><b>Men kichik bir narsa topdim — bu xavfsizlik masalasimi?</b></summary>

Agar shubhada bo'lsangiz — **bizga yozing**. Ommaviy issue ochishdan ko'ra, shaxsiy email yuborib so'raganingiz **doim yaxshiroq**. Biz birgalikda hal qilamiz: agar oddiy bug bo'lsa, ochiq issue ochishga taklif qilamiz; agar haqiqatdan xavfsizlik masalasi bo'lsa — protokol bo'yicha boramiz.

</details>

<details>
<summary><b>Anonim ravishda xabar bera olamanmi?</b></summary>

Ha. Email orqali anonim manzildan (masalan, ProtonMail) yuborishingiz mumkin. Lekin **javob olish** uchun qandaydir aloqa kanali kerak.

</details>

---

<div align="center">

**Xavfsizlikka birgalikda e'tibor beramiz! 🛡️**

[← README ga qaytish](README.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

</div>
