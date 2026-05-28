# Oy 1 — Mashqlar to'plami

Bu sahifada **barcha mavzular** bo'yicha qo'shimcha mashqlar to'plangan. Har bobning oxiridagi mashqlardan **tashqari**, bu yerdagilarni ham bajaring — chuqurroq tushunish uchun.

## 🟢 Easy darajadagi mashqlar

### Math
1. NumPy bilan `(5, 5)` random matrix yarating, uning rank'ini hisoblang.
2. `[2, 4, 6, 8, 10]` vektorining variance va standard deviation'ini qo'lda va NumPy bilan hisoblang.
3. Quyidagi tasdiqlar to'g'ri yoki noto'g'ri ekanini tushuntiring:
   - "Mean — bu doim eng yaxshi markaziy tendensiya o'lchovi"
   - "Standard deviation — bu variance'ning kvadrat ildizi"

### NumPy
1. `np.eye(5)` ishlatib `5x5` identity matrix yarating.
2. `[1, 2, 3, 4, 5, 6, 7, 8, 9]` ni `(3, 3)` matrix'ga reshape qiling va transpose oling.
3. Ikki random vektor `(100,)` orasidagi Euclidean distance'ni hisoblang.

### Pandas
1. CSV faylni o'qing va birinchi 5 ta qatorni `JSON` formatda chiqaring.
2. Ustun nomidagi bo'sh joylarni `_` ga almashtiring (`df.columns.str.replace`).
3. `DataFrame`'da ikkala bo'sh va `0` qiymatlarni topib, ularning sonini chiqaring.

### Vizualizatsiya
1. Sinus va kosinus funksiyalarini bitta chart'da chizing.
2. 4 ta turli rangda `bar plot` chizing.
3. Random `(50, 50)` matrix uchun `imshow` ishlatib heatmap chizing.

## 🟡 Medium darajadagi mashqlar

### Real dataset bilan ishlash
1. **Iris dataset**: `seaborn.load_dataset('iris')` orqali yuklang. `species` bo'yicha har bir feature distribution'ini violin plot bilan chizing.
2. **Tips dataset**: `seaborn.load_dataset('tips')` ni yuklang. `day` va `time` bo'yicha o'rtacha `tip` ni pivot table sifatida chiqaring.
3. **Custom dataset**: O'zingiz Django/FastAPI loyihangizdan real ma'lumotni eksport qiling (orders, users, events) va EDA boshlash.

### Vectorization mashqlari
1. **Implement** `sigmoid(x) = 1 / (1 + exp(-x))` funksiyasini NumPy'da. 1M element uchun pure Python loop bilan solishtiring.
2. **Implement** `softmax(x) = exp(x) / sum(exp(x))` — numerical stability bilan (`x - max(x)`).
3. **Implement** moving average — `(window=10)`, NumPy'da loop yo'q.

### Pandas pipelines
1. **E-commerce funnel**: foydalanuvchilarning `view → cart → purchase` o'tish nisbatini hisoblang.
2. **Cohort retention**: foydalanuvchilarni ro'yxatdan o'tish oyiga ko'ra cohort'larga ajrating, 6 oy `retention` chizing.
3. **RFM Analysis**: Recency, Frequency, Monetary metric'larni har mijoz uchun hisoblang va segment'larga ajrating.

## 🔴 Hard darajadagi mashqlar (Backend integration)

### 1. Analytics API (FastAPI)

Quyidagi endpoint'lar bilan to'liq FastAPI servis yarating:

```
POST /api/v1/analytics/upload      # CSV/JSON dataset yuklash
GET  /api/v1/analytics/{id}/summary # describe() natijasi
GET  /api/v1/analytics/{id}/chart   # PNG chart qaytarish
GET  /api/v1/analytics/{id}/report  # ydata-profiling HTML
POST /api/v1/analytics/{id}/query   # custom SQL-like so'rov
```

**Talablar:**
- Yuklangan datasetlarni Redis'da yoki diskda saqlash (TTL bilan)
- Pydantic models bilan to'liq type-safe
- OpenAPI docs avtomatik
- Pytest bilan unit testlar

### 2. Django Admin Reports

Mavjud Django loyihangizga (yoki yangi yarating) `admin custom action` qo'shing:
- Tanlangan obyektlar uchun PDF report generatsiya
- Pandas + matplotlib bilan grafiklar
- ReportLab yoki WeasyPrint bilan PDF

### 3. Real-time Dashboard

Server-Sent Events (SSE) bilan real-time dashboard yarating:
- FastAPI backend har 5 sekundda fresh data
- Frontend (oddiy HTML+Chart.js)
- Pandas backend'da agregatsiya qiladi
- Plotly JSON formatda data jo'natadi

### 4. Data Quality Service

Pandera yoki Great Expectations ishlatib:
- Yuklangan CSV uchun schema validation
- Quality score (0-100)
- Anomaliyalarni aniqlash (outliers, type mismatch)
- Slack notification noto'g'ri data kelganda

## 🏆 Mini-loyihalar (har biri 1-2 hafta)

### Mini-loyiha 1: Personal Finance Tracker
- O'zingizning bank statement (CSV)
- Pandas bilan kategoriyalash (rules-based)
- Oylik xarajatlar dashboard
- Trend'lar va anomaliyalar
- Streamlit'da interaktiv UI

### Mini-loyiha 2: GitHub Profile Analyzer
- GitHub API'dan o'z repolaringizni yuklab oling
- Tillar bo'yicha kod taqsimoti
- Commit faolligi (kalendar heatmap)
- Top kontribyutorlar
- README'ga avtomatik embed qilish

### Mini-loyiha 3: O'zbekiston Open Data EDA
- [data.gov.uz](https://data.gov.uz) dan dataset olib EDA qiling
- Insights'larni o'zbek tilida yozing
- Habr.com/dev.to'ga post sifatida chiqaring

## 🧪 Quiz (o'zingizni sinash)

### Pandas
1. `df.iloc[0]` va `df.loc[0]` orasidagi farq nima?
2. `df.merge()` ning `how='left'` va `how='outer'` farqi?
3. `apply()` va `map()` qachon ishlatiladi?
4. `transform()` va `agg()` farqi?
5. Memory'da katta DataFrame'ni qanday optimallashtirish mumkin? (`category` dtype, `downcast`)

### NumPy
1. `np.array` va `np.asarray` farqi?
2. Broadcasting qoidasini tushuntiring.
3. `np.copy()` va `[:]` slicing farqi nima?
4. `axis=0` va `axis=1` ni `(rows, cols)` bilan munosabati?
5. `np.vectorize()` haqiqatdan tezroq qiladimi? (Hint: yo'q!)

### Math
1. `cosine similarity` formulasi va nima uchun ishlatiladi?
2. `gradient descent` da `learning rate` juda katta bo'lsa nima bo'ladi?
3. Normal distribution va uniform distribution farqi?
4. Bayes theorem'ni o'z so'zlaringiz bilan tushuntiring.
5. `correlation = 0` — bu doim "munosabat yo'q" degan ma'noni anglatadimi? (Hint: yo'q, faqat linear munosabat yo'q)

## ✅ Oy oxiri checklist

- [ ] Math bobi tugatildi, gradient descent kodi yozilgan
- [ ] NumPy mashqlari yakunlangan, broadcasting tushunaman
- [ ] Pandas EDA mashqlari (Titanic / House Prices)
- [ ] Visualization mashqlari, FastAPI'dan PNG qaytaradigan endpoint
- [ ] **Capstone**: bitta to'liq EDA loyihasi GitHub'da
- [ ] LinkedIn'da post (loyihaga link bilan)

Tabriklayman! 🎉 [Oy 2 — Klassik ML](../month-02-classical-ml/README.md) ga tayyormiz.
