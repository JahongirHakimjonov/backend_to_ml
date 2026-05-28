# EDA Capstone Loyihasi

## 🎯 Maqsad

1-oyning yakunlovchi loyihasi. Real datasetda **to'liq Exploratory Data Analysis (EDA)**bajarib, **professional darajadagi report**tayyorlaysiz. Bu sizning portfolio'ngizdagi birinchi ish bo'ladi.

## Loyiha brief

### Dataset tanlovi (bittasini tanlang)

| Dataset | Source | Mavzu |
|---------|--------|-------|
| **House Prices** | Kaggle (Ames Housing) | Uy narxi bashorat (continuous target) |
| **Telco Customer Churn** | Kaggle | Mijoz ketishi (binary classification) |
| **NYC Taxi Trips** | NYC Open Data | Time series + geo-spatial |
| **Olist E-commerce** | Kaggle (Brazil) | Multi-table relational |
| **Uzbekistan Open Data** | data.gov.uz | Mahalliy kontekst |

**Tavsiya:**Birinchi marta — **House Prices**yoki **Titanic**. Bular yaxshi hujjatlangan va Kaggle'da minglab kernel'lar bor.

### EDA report'ning standart strukturasi

#### 1. Project Overview (1 sahifa)
- Maqsad: nima uchun bu ma'lumotlarni tahlil qilamiz?
- Business question: javob izlanayotgan asosiy savol
- Dataset haqida qisqacha (manba, hajmi, ustunlar soni)

#### 2. Data Loading va Initial Inspection
```python
df = pd.read_csv("data.csv")
print(df.shape)          # nechta qator/ustun
print(df.dtypes)         # ustun tiplari
print(df.head())         # birinchi qatorlar
print(df.info())         # memory va null'lar
print(df.describe())     # statistik xulosa
```

#### 3. Data Quality Check
- **Missing values** — har ustunda nechta NaN, % bo'yicha
- **Duplicates** — `df.duplicated().sum()`
- **Data type issues** — masalan, `date` string ko'rinishida
- **Outliers** — IQR yoki z-score usulida
- **Value distributions** — har bir categorical ustunda unique qiymatlar

```python
# Missing values vizualizatsiyasi
import missingno as msno
msno.matrix(df)
msno.bar(df)
```

#### 4. Univariate Analysis
Har bir ustunni alohida o'rganish:
- **Numerical**: histogram, KDE, box plot
- **Categorical**: count plot, value_counts
- **Date**: time series plot

#### 5. Bivariate Analysis
- Ikki ustun orasidagi munosabat
- **Num vs Num**: scatter, correlation
- **Cat vs Num**: box plot, violin plot
- **Cat vs Cat**: cross-tabulation, stacked bar

#### 6. Multivariate Analysis
- 3+ ustun aralashgan
- **Pair plot**(Seaborn)
- **Heatmap**(correlation matrix)
- **Faceted plots**(FacetGrid)

#### 7. Target Variable Deep Dive
Agar supervised ML maqsadingiz bo'lsa:
- Target distribution
- Class imbalance (classification)
- Feature vs target munosabati

#### 8. Feature Engineering Ideas
EDA jarayonida quyidagilarni qayd qiling:
- Yangi feature'lar yaratish g'oyalari (masalan, `age * income`)
- Transformatsiya zarur ustunlar (log, sqrt)
- Encoding strategiyalari (categorical → numerical)

#### 9. Key Insights (BIZNES TILIDA)
- 5-10 ta asosiy topilma
- Har biri bitta gap, ortidan vizualizatsiya
- **Storytelling**: "Mijozlar 70% ehtimol bilan oxirgi 3 oyda qo'ng'iroq qilmagan bo'lsa, ketadi"

#### 10. Conclusion va Next Steps
- EDA xulosasi
- Modelga o'tish uchun tavsiyalar
- Datadagi cheklovlar va xavflar

## Texnik talablar

### Tools
- **Jupyter Notebook**yoki **VS Code**(`.ipynb`)
- **Pandas** — data manipulation
- **NumPy** — hisob-kitoblar
- **Matplotlib + Seaborn** — vizualizatsiya
- **missingno** — missing data vizual
- **pandas-profiling**yoki **ydata-profiling**(avtomatik EDA report)

```bash
pip install pandas numpy matplotlib seaborn missingno ydata-profiling
```

### Code quality
- Notebook'ni mantiqiy section'larga bo'lish (Markdown headings bilan)
- Har bir kod bloki oldida tushuntirish
- Function'larga ajratish (`def plot_distribution(col)`)
- Reproducibility: `random_state=42` doim aniq

### Notebook strukturasi (har bo'lim alohida cell)

```python
# 1. IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

pd.set_option("display.max_columns", 100)
sns.set_theme(style="whitegrid")

# 2. LOAD DATA
DATA_PATH = Path("../data/house_prices.csv")
df = pd.read_csv(DATA_PATH)

# 3. OVERVIEW
print(f"Shape: {df.shape}")
print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
df.head()
```

## Deliverable (topshiriladigan ish)

GitHub repo'da quyidagilar bo'lishi kerak:

```
eda-house-prices/
├── README.md                       # Loyiha tavsifi, qanday ishga tushirish
├── notebooks/
│   └── 01_eda.ipynb               # Asosiy EDA
├── data/
│   ├── raw/                       # Dastlabki CSV (gitignore bilan)
│   └── processed/                 # Tozalangan dataset
├── reports/
│   ├── insights.md                # 5-10 ta key insights (markdown)
│   ├── figures/                   # PNG/PDF chart'lar
│   └── eda_report.html            # ydata-profiling output
├── src/
│   └── plotting.py                # Reusable plot funksiyalari
└── requirements.txt
```

### README.md shabloni

```markdown
# House Prices EDA

## Maqsad
Ames Housing datasetni tahlil qilib, uy narxiga ta'sir qiluvchi asosiy omillarni aniqlash.

## Asosiy topilmalar
- OverallQual eng kuchli korrelatsiyaga ega (0.79)
- GrLivArea (yashash maydoni) ikkinchi muhim feature (0.71)
- ...

## Qanday ishga tushirish
\`\`\`bash
pip install -r requirements.txt
jupyter notebook notebooks/01_eda.ipynb
\`\`\`

## Texnologiyalar
- Python 3.11
- pandas, numpy, matplotlib, seaborn
```

## Evaluation criteria

O'zingizni baholash uchun:

| Mezon | 0 | 1 | 2 | 3 |
|-------|---|---|---|---|
| Data Quality | Tekshirilmagan | Asosiy nullik | + outliers + types | + business logic check |
| Visualization | Yo'q | 5+ chart | 10+ chart, mantiqli | Storytelling bilan, professional |
| Insights | Yo'q | 3 ta tabular | 5+ insight, biznes tili | + actionable recommendations |
| Code quality | Spaghetti | Cells aniq | Function'lar + comments | Production-ready |
| Reproducibility | Random | random_state | + requirements.txt | + Docker + Make |

**Maqsad: kamida har mezonda 2 ball.**

## Referenslar

- **Kaggle EDA notebooks**(eng yaxshilarni o'rganing):
 - [Comprehensive Data Exploration with Python](https://www.kaggle.com/code/pmarcelino/comprehensive-data-exploration-with-python)
 - [Titanic EDA + ML](https://www.kaggle.com/code/startupsci/titanic-data-science-solutions)
- **"Effective Data Storytelling"** — Brent Dykes
- **ydata-profiling**docs — [docs.profiling.ydata.ai](https://docs.profiling.ydata.ai/)

## Bonus mashqlar (extra credit)

1. **Streamlit dashboard**: EDA natijalarini interaktiv dashboard'ga aylantiring
2. **Automated EDA**: `ydata-profiling` yoki `Sweetviz` ishlatib avtomatik report yarating va manual EDA bilan solishtiring
3. **Geographic visualization**(agar dataset'da lat/long bo'lsa): Folium yoki Plotly bilan map yarating

## ✅ Loyihani topshirishdan oldin

- [ ] Notebook xatosiz to'liq run bo'ladi
- [ ] Har bir chart `title`, `xlabel`, `ylabel`, `legend`ga ega
- [ ] Markdown bilan har bo'lim tushuntirilgan
- [ ] README aniq va to'liq
- [ ] GitHub'ga commit qilingan (notebook ham, charts ham)
- [ ] LinkedIn'ga post yozasiz (bu — sizning birinchi ML loyihangiz!)

Tabriklayman — birinchi katta qadam tugadi. [Mashqlar](./exercises.md) bo'limidagi qo'shimcha praktikani ham bajaring.

So'ngra: [Oy 2 — Klassik ML](../month-02-classical-ml/README.md) ga o'ting.
