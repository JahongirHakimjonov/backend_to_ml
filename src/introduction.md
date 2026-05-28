# Kirish

Salom! Bu kitob — **middle darajadagi Python backend developer**uchun **6 oylik ML Roadmap**. Agar siz Django, DRF, FastAPI bilan ishlab kelayotgan bo'lsangiz va Machine Learning / MLOps Engineer yo'nalishiga o'tmoqchi bo'lsangiz — bu kitob aynan siz uchun.

## Kim uchun bu kitob?

- ✅ Python sintaksisini yaxshi bilasiz (OOP, decorators, async/await, type hints)
- ✅ Django, DRF yoki FastAPI bilan production'da kamida 1 yil ishlagansiz
- ✅ Docker, PostgreSQL, Redis, Celery bilan tanishsiz
- ✅ Git, REST API, asosiy Linux buyruqlarni bilasiz
- ❌ Math (matematika) yoki ML tajribangiz bo'lmasligi mumkin — kitob nol darajadan boshlanadi

## Nima uchun "Backend to ML"?

Aksariyat ML kurslari **data scientist**bo'lish uchun yozilgan — Jupyter notebook'da model qurish, prezentatsiya tayyorlash. Lekin sizning ustunligingiz boshqacha:

| Data Scientist | Backend Dev → ML Engineer |
|----------------|---------------------------|
| Notebook'da eksperiment | Productionda ishlaydigan tizim |
| Model accuracy | Model latency + throughput |
| CSV bilan ishlash | PostgreSQL + Kafka bilan ishlash |
| `.fit()` chaqirish | Docker'ga joylash, monitoring qo'shish |

Siz **production system'larni qurishni bilasiz** — bu juda katta ustunlik. Faqat ML qismini qo'shish kifoya.

## Roadmap qanday tuzilgan?

6 oy, har oy o'z mavzusiga ega:

| Oy | Mavzu | Asosiy natija |
|----|-------|---------------|
| **1** | Foundations | Math + NumPy/Pandas — har qanday ML kodni o'qiy olasiz |
| **2** | Klassik ML | Scikit-learn + XGBoost — production'da 80% ishlaydigan modellar |
| **3** | Deep Learning | PyTorch — neural network'larni o'zingiz quryasiz |
| **4** | CV + NLP | OpenCV, YOLO, HuggingFace — image va text bilan ishlay olasiz |
| **5** | LLM + RAG | OpenAI, Anthropic, LangChain, Vector DB — AI mahsulotlar yaratasiz |
| **6** | MLOps | MLflow, DVC, Docker, Airflow — to'liq production pipeline |

## Har bir bobda nimalar bor?

Har bir mavzu bo'limi quyidagi standart strukturaga ega:

1. **🎯 Maqsad** — bu bobni o'qib bo'lgach nimani bila olasiz
2. **Nimani o'rganish kerak** — asosiy tushunchalar ro'yxati
3. **Kutubxonalar** — Python paketlari va o'rnatish buyruqlari
4. **Muhim mavzular** — chuqurroq kirib chiqish kerak bo'lgan tushunchalar
5. **Kod misollari** — 2-3 ta minimal ishlaydigan misol (markdown ichida)
6. **Backend integratsiyasi** — bu bilimni FastAPI/Django'da qo'llash
7. **Resurslar** — kitoblar, video, maqolalar (link bilan)
8. **🏋️ Mashqlar** — 3 darajadagi amaliy topshiriqlar (Easy → Medium → Hard)
9. **Topshiriq (Capstone)** — boblovchi katta loyiha
10. **✅ Tekshirish ro'yxati** — o'zingizni baholash uchun checklist

## Mashqlar tizimi

Har bobda **3 darajadagi mashqlar**mavjud:

- 🟢 **Easy (warm-up)** — kontseptsiyani tushunganligini tekshirish (5-10 daqiqa)
- 🟡 **Medium (apply)** — real datasetda qo'llash (30-60 daqiqa)
- 🔴 **Hard (integrate)** — FastAPI/Django'ga integratsiya qilish (2-4 soat)

Mashqlarning ko'pi `notebooks/` papkasida tayyor `.ipynb` shablon bilan beriladi — siz uni to'ldirib chiqasiz.

## Kuniga qancha vaqt kerak?

- **Minimum:**1 soat/kun (asosan o'qish + kichik mashqlar)
- **Recommended:**1.5-2 soat/kun (o'qish + Medium darajadagi mashqlar)
- **Intensive:**3+ soat/kun (barcha mashqlar + capstone loyiha)

**Muhim:**vaqt sifatdan muhimroq emas. Har kuni 1 soat ishlash, hafta oxiri 7 soat ishlashdan ko'ra yaxshiroq.

## Til haqida

Bu kitob **o'zbek tilida**yozilgan, lekin **texnik terminlar**(gradient, overfitting, embedding, tensor, h.k.) **inglizcha asl shaklida**qoldirilgan — chunki:

1. Documentation, StackOverflow, GitHub issues — hammasi inglizcha
2. Tarjima qilingan terminlar (masalan, "gradient" → "qiyalik") ishlatilmaydi va chalkashlik tug'diradi
3. Sizning maqsadingiz xalqaro darajadagi ML Engineer bo'lish

Birinchi marta uchragan har bir termin **qavs ichida o'zbekcha izoh**bilan keladi:

> `gradient` (qiyalik — funksiyaning eng tez o'sish yo'nalishi)

Lug'atning to'liq ro'yxati [Glossary](./glossary.md) bo'limida.

## Loyihalar va portfolio

6 oy davomida quyidagi **4 ta katta loyihani**GitHub'da to'playsiz:

1. **Prediction API** — Klassik ML + FastAPI + Postgres + Docker
2. **Computer Vision Service** — YOLO + FastAPI + S3/MinIO + Celery
3. **RAG Chatbot** — Vector DB + LLM + Streamlit/React UI
4. **MLOps Pipeline** — DVC + MLflow + Airflow + Docker + GitHub Actions

Bu loyihalar **portfolio**ngiz bo'ladi. CV'ga "ML Engineer" deb yozish uchun yetarli.

## Texnik talablar

### Hardware
- **Minimum:**8 GB RAM, ixtiyoriy CPU
- **Recommended:**16 GB RAM, M1/M2/M3 Mac yoki RTX 3060+ GPU
- **Cloud alternative:**Google Colab (bepul GPU), Kaggle Notebooks

### Software
- Python 3.10+ (recommended 3.11)
- VS Code yoki PyCharm
- Docker Desktop
- Git
- Jupyter Lab yoki VS Code Jupyter extension

### Cloud accountlar (bepul tier'lar yetarli)
- GitHub (kod hosting)
- Kaggle (datasets, competitions)
- HuggingFace (modellar, datasets)
- Google Colab (GPU access)
- OpenAI yoki Anthropic API (LLM oyi uchun, $5-10 yetarli)

## Bu kitobdan qanday foydalanish?

**Tartibli o'qing** — har oy oldingisining ustiga quriladi. Oy 3'dan boshlash uchun Oy 1-2 bilim kerak.

**Mashqlarni qiling** — o'qish kifoya emas. Har bir mavzuni o'z qo'lingiz bilan kod yozib mustahkamlang.

**Loyiha yozing** — har oy oxiridagi capstone'ni o'tkazib yubormang. Bu portfolio'ngiz.

**Kommitlang** — har bir mashq va loyiha uchun GitHub repo oching, har kuni commit qiling. 6 oydan keyin yashil kvadratchalar tarixingiz bo'ladi.

**Yordam so'rang** — turg'un qoldingizmi? StackOverflow, Reddit r/MachineLearning, HuggingFace forum, yoki Telegram'dagi `@uzbekdevs`, `@uz_ai_community`.

## Muallif

Bu kitob **Jahongir Hakimjonov**tomonidan yozilgan — Python backend developer va o'z yo'lida ML/MLOps Engineer'ga aylanish jarayonida bo'lgan inson. Kitob — shaxsiy o'rganish yo'lining natijasi va uni o'zbek tilida boshqalarga yetkazish istagidan tug'ilgan.

Savollar, taklif yoki yordam uchun:

- 💬 **Telegram:** [@ja_khan_gir](https://t.me/ja_khan_gir) — eng tezkor kanal
- 📧 **Email:** [jahongirhakimjonov@gmail.com](mailto:jahongirhakimjonov@gmail.com)
- 🌐 **Website:** [dev.jakhangir.uz](https://dev.jakhangir.uz/)
- 🐙 **GitHub:** [@JahongirHakimjonov](https://github.com/JahongirHakimjonov)
- 💼 **LinkedIn:** [Jahongir Hakimjonov](https://www.linkedin.com/in/jahongir-hakimjonov/)

To'liq ma'lumot, mentorlik takliflari va minnatdorchilik — [Muallif haqida](./about-author.md) sahifasida.

## Boshlang'ich qadam

Tayyormisiz? [Oy 1: Foundations](./month-01-foundations/README.md) ga o'ting va birinchi qadamni qo'ying.

Omad!
