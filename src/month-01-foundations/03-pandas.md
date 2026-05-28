# Pandas

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- DataFrame va Series ni "in-memory SQL table" sifatida ishlatishni o'rganasiz
- Real CSV/JSON/Parquet fayllar bilan ishlay olasiz
- Missing data, duplicates, type conversion'larni boshqara olasiz
- `groupby`, `pivot_table`, `merge` bilan murakkab so'rovlarni yozasiz
- Time series ma'lumotlar bilan ishlay olasiz

## 📖 Nimani o'rganish kerak

- **Series** va **DataFrame** strukturasi
- I/O: `read_csv`, `read_json`, `read_parquet`, `read_sql`, `to_*` variantlari
- Indexing: `.loc[]`, `.iloc[]`, boolean indexing, `query()`
- Missing data: `isna()`, `fillna()`, `dropna()`
- Aggregation: `groupby`, `agg`, `transform`, `apply`
- Joining: `merge`, `concat`, `join`
- Reshaping: `pivot_table`, `melt`, `stack`, `unstack`
- Time series: `pd.to_datetime`, `resample`, rolling windows
- Categorical data, ordering, ranking

## 📦 Kutubxonalar

```bash
pip install pandas pyarrow openpyxl
```

- **pandas** — asosiy
- **pyarrow** — tezroq engine, parquet fayllar uchun
- **openpyxl** — Excel fayllar bilan ishlash

## 🧠 Muhim mavzular

### Backend dev uchun mental model

| SQL | Pandas |
|-----|--------|
| `SELECT * FROM users LIMIT 5` | `df.head()` |
| `SELECT name, age FROM users` | `df[['name', 'age']]` |
| `WHERE age > 30` | `df[df.age > 30]` yoki `df.query('age > 30')` |
| `GROUP BY country` | `df.groupby('country')` |
| `JOIN ... ON` | `df.merge(other, on='id')` |
| `ORDER BY date DESC` | `df.sort_values('date', ascending=False)` |
| `COUNT, SUM, AVG` | `df.agg(['count', 'sum', 'mean'])` |

### `.loc` vs `.iloc`

- `.loc[]` — **label-based** (index nomi yoki ustun nomi bilan)
- `.iloc[]` — **integer position** (qator/ustun raqami bilan)

```python
df.loc[5, 'name']      # 5-index labelli qator, 'name' ustuni
df.iloc[5, 0]          # 5-qator, 0-ustun (Python list kabi)
```

### `inplace` muammosi

Eski Pandas'da `df.fillna(0, inplace=True)` patterni keng tarqalgan edi. **Yangi versiyada** (2.0+) bu deprecated. Buning o'rniga:

```python
df = df.fillna(0)              # to'g'ri
# yoki copy-on-write mode ishlatish
pd.set_option('mode.copy_on_write', True)
```

### Method chaining

ML'da odatda transformation'lar zanjir shaklida yoziladi:

```python
result = (
    df
    .dropna(subset=['price'])
    .query('price > 0')
    .assign(price_log=lambda x: np.log(x.price))
    .groupby('category')
    .agg(avg_price=('price', 'mean'), count=('id', 'count'))
    .sort_values('avg_price', ascending=False)
)
```

Bu — `pipe`, `assign`, `transform` ishlatish — ML data preparation'da "best practice".

## 💻 Kod misollari

### DataFrame yaratish va asosiy operatsiyalar

```python
import pandas as pd
import numpy as np

# Dict'dan
df = pd.DataFrame({
    "name": ["Ali", "Vali", "Salim", "Karim"],
    "age": [25, 30, 35, 28],
    "city": ["Tashkent", "Samarkand", "Bukhara", "Tashkent"],
    "salary": [1000, 1500, 2000, 1200],
})

# CSV'dan
# df = pd.read_csv("users.csv")

# Asosiy ko'rinish
print(df.head())          # birinchi 5 qator
print(df.info())          # shape, dtype, memory
print(df.describe())      # statistik xulosa
print(df.shape)           # (4, 4)
```

### Filtering va groupby

```python
# Filtering
adults = df[df.age >= 30]
tashkent_users = df.query("city == 'Tashkent' and salary > 1000")

# Groupby aggregation
by_city = df.groupby("city").agg(
    avg_salary=("salary", "mean"),
    max_age=("age", "max"),
    count=("name", "count"),
).reset_index()
print(by_city)

# Multiple aggregation
stats = df.groupby("city")["salary"].agg(["mean", "std", "min", "max"])
```

### Missing data va data cleaning

```python
# Sun'iy missing data
df.loc[0, "salary"] = np.nan
df.loc[2, "city"] = None

# Aniqlash
print(df.isna().sum())            # har ustunda NaN soni

# To'ldirish strategiyalari
df["salary"] = df["salary"].fillna(df["salary"].median())
df["city"] = df["city"].fillna("Unknown")

# Yoki tashlab yuborish
df_clean = df.dropna()
```

### Merge va join

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "user_name": ["Ali", "Vali", "Ali", "Karim"],
    "amount": [100, 200, 150, 75],
})

# INNER JOIN (default)
merged = df.merge(orders, left_on="name", right_on="user_name")

# LEFT JOIN
all_users = df.merge(orders, left_on="name", right_on="user_name", how="left")

# Userlar va ularning umumiy buyurtmasi
user_totals = (
    df.merge(orders, left_on="name", right_on="user_name", how="left")
      .groupby("name")["amount"].sum()
      .fillna(0)
      .reset_index()
)
```

### Time series

```python
# Tasodifiy daily sales data
dates = pd.date_range("2024-01-01", periods=365, freq="D")
sales = pd.DataFrame({
    "date": dates,
    "sales": np.random.poisson(100, size=365) + np.sin(np.arange(365) / 30) * 20,
})

sales = sales.set_index("date")

# Haftalik agregatsiya
weekly = sales.resample("W").sum()

# 30 kunlik rolling mean
sales["rolling_30"] = sales["sales"].rolling(window=30).mean()

# Year, month, weekday ajratish
sales["month"] = sales.index.month
sales["weekday"] = sales.index.day_name()
```

## 🔌 Backend integratsiyasi

### 1. Django ORM → Pandas
```python
from django.db.models import Sum
import pandas as pd

# Django QuerySet → DataFrame
qs = Order.objects.values('user_id', 'amount', 'created_at')
df = pd.DataFrame(list(qs))

# Yoki to'g'ridan-to'g'ri SQL
df = pd.read_sql("SELECT * FROM orders WHERE created_at >= NOW() - INTERVAL '30 days'",
                 connection)
```

### 2. FastAPI'da CSV export endpoint
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import io

app = FastAPI()

@app.get("/reports/orders.csv")
async def export_orders():
    df = pd.read_sql("SELECT * FROM orders", engine)
    # Boyitish: yangi ustun qo'shish
    df["revenue_per_item"] = df["total"] / df["quantity"]
    
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=orders.csv"},
    )
```

### 3. Background job — daily report
```python
# Celery task
@app.task
def generate_daily_report():
    df = pd.read_sql("SELECT * FROM events WHERE date = CURRENT_DATE - 1", engine)
    
    report = (
        df.groupby("country")
          .agg(users=("user_id", "nunique"),
               revenue=("amount", "sum"),
               avg_session=("duration_sec", "mean"))
          .sort_values("revenue", ascending=False)
    )
    
    report.to_excel(f"/reports/daily_{date.today()}.xlsx")
    # Email send via Celery beat
```

## 📚 Resurslar

- **Official Pandas docs** — [pandas.pydata.org/docs/user_guide/](https://pandas.pydata.org/docs/user_guide/)
- **"Python for Data Analysis"** — Wes McKinney (Pandas yaratuvchisi, 3-nashr) — **MUST READ**
- **"Modern Pandas"** — Tom Augspurger (blog series) — best practices
- **Kaggle Learn — Pandas** — bepul mini-course
- **DataCamp / pandas tutor** — [pandastutor.com](https://pandastutor.com/) — vizual debug

## 🏋️ Mashqlar

### 🟢 Easy
1. CSV faylni o'qing (masalan, Titanic dataset), birinchi 10 qatorni ko'ring va `info()`, `describe()` chiqaring.
2. Bitta ustun bo'yicha filter qiling (`age > 18`).
3. Yangi ustun yarating (`bmi = weight / height ** 2`).

### 🟡 Medium
1. Titanic'da `Survived` bo'yicha `Sex` va `Pclass` qiyosini chiqaring (pivot table).
2. Missing values strategiyasini taqqoslang: `fillna(mean)` vs `fillna(median)` vs `dropna()` — har biri uchun statistikani solishtiring.
3. Time series: 1 yil davomidagi soxta sotuv ma'lumotlarini yarating va haftalik trendlarni topib chizing.

### 🔴 Hard
1. **Django/FastAPI endpoint**: `/api/analytics/cohort/` — foydalanuvchilarni ro'yxatdan o'tish oyiga ko'ra kohortlarga ajrating va har bir kohortning keyingi 6 oydagi `retention` ni heatmap data shaklida qaytaring. Pandas `pivot_table` va `groupby` ishlating.
2. **Streaming CSV**: 1 GB CSV faylni xotiraga sig'maydigan tarzda chunk'lar bilan o'qing (`chunksize`), har chunk'da agregatsiya qiling, oxirgi natijani qaytaring.

## 🚀 Capstone

`notebooks/month-01/02_pandas_practice.ipynb`:
- E-commerce datasetni yuklang ([Olist Brazilian e-commerce Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce))
- 5 ta jadval orasida `merge` qiling
- Har bir mahsulot kategoriyasi bo'yicha:
  - O'rtacha narx
  - Buyurtmalar soni
  - O'rtacha yetkazib berish vaqti (kunlarda)
  - Mijoz qoniqishi reytingi (`review_score` mean)
- Top 10 daromad keltiruvchi kategoriyalarni ranking qiling

## ✅ Tekshirish ro'yxati

- [ ] DataFrame va Series farqini bilaman
- [ ] `.loc` va `.iloc` farqini tushunaman, har birini joyida ishlataman
- [ ] `groupby + agg` pattern'ni o'zlashtirdim
- [ ] Missing data uchun kamida 3 ta strategiya bilaman
- [ ] `merge` ning `how` parametrlarini (inner, left, right, outer) bilaman
- [ ] Time series'da `resample` va `rolling` ishlataman
- [ ] Method chaining bilan o'qishli kod yozaman
- [ ] Django/FastAPI'dan SQL natijasini DataFrame'ga aylantiraman

[Matplotlib va Seaborn](./04-matplotlib-seaborn.md) ga o'tamiz.
