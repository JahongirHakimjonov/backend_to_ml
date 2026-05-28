# Matplotlib va Seaborn

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Matplotlib bilan o'z grafiklaringizni `figure`, `axes` darajasida boshqara olasiz
- Seaborn bilan statistik grafiklarni 1-2 qatorda yarata olasiz
- ML loyihalarda zarur bo'lgan barcha asosiy chart turlarini bilasiz
- EDA (Exploratory Data Analysis) hisobot uchun chiroyli vizualizatsiya tayyorlay olasiz

## 📖 Nimani o'rganish kerak

### Matplotlib
- `Figure` va `Axes` arxitekturasi
- `pyplot` interface (oddiy) vs Object-oriented API (kontrol)
- Asosiy chart turlari: `plot`, `scatter`, `bar`, `hist`, `boxplot`
- Subplot'lar: `subplots()`, `GridSpec`
- Customization: title, labels, legend, ticks, colors
- Saqlash: `savefig` (PNG, SVG, PDF)

### Seaborn
- Themes va styling (`set_theme`, `set_palette`)
- Categorical plots: `countplot`, `barplot`, `boxplot`, `violinplot`
- Distribution plots: `histplot`, `kdeplot`, `displot`
- Relationship plots: `scatterplot`, `lineplot`, `regplot`
- Matrix plots: `heatmap`, `clustermap`
- Multi-plot grids: `FacetGrid`, `PairGrid`, `pairplot`

## 📦 Kutubxonalar

```bash
pip install matplotlib seaborn
```

Plotly alternativasi (interaktiv grafiklar uchun):
```bash
pip install plotly
```

## 🧠 Muhim mavzular

### Matplotlib arxitekturasi

Matplotlib'da har bir grafik 3 ta qatlamdan iborat:

1. **Figure** — butun "kanvas" (rasm fayli)
2. **Axes** — bitta chart maydoni (subplot)
3. **Plot elementlari** — chiziq, nuqta, bar, label, va h.k.

```python
import matplotlib.pyplot as plt

# 2 ta interface bor:

# 1. Pyplot API (oddiy, lekin global state)
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Quick")
plt.show()

# 2. Object-oriented API (TAVSIYA — kattaroq loyihalarda)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Better")
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.savefig("plot.png", dpi=150, bbox_inches="tight")
```

### Qachon Matplotlib, qachon Seaborn?

- **Matplotlib** — to'liq kontrol kerak bo'lganda, custom layout
- **Seaborn** — statistik chart'lar, DataFrame bilan to'g'ridan-to'g'ri ishlash, "yaxshi ko'rinadigan default'lar"

Real ishda ko'pincha **ikkalasi birga**:
```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, ax=ax)
ax.set_title("My Correlation Matrix")
```

## 💻 Kod misollari

### Asosiy chart turlari

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y1, label="sin(x)", color="blue", linewidth=2)
ax.plot(x, y2, label="cos(x)", color="red", linestyle="--")
ax.set_title("Trigonometric Functions")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

### Subplotlar

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Histogram
data = np.random.normal(0, 1, 1000)
axes[0, 0].hist(data, bins=30, color="steelblue", edgecolor="black")
axes[0, 0].set_title("Histogram")

# Scatter
x = np.random.rand(100)
y = x + np.random.normal(0, 0.1, 100)
axes[0, 1].scatter(x, y, alpha=0.6)
axes[0, 1].set_title("Scatter")

# Bar
categories = ["A", "B", "C", "D"]
values = [23, 45, 56, 78]
axes[1, 0].bar(categories, values, color=["red", "green", "blue", "orange"])
axes[1, 0].set_title("Bar")

# Box plot
data_groups = [np.random.normal(i, 1, 100) for i in range(3)]
axes[1, 1].boxplot(data_groups, labels=["Group 1", "Group 2", "Group 3"])
axes[1, 1].set_title("Box Plot")

plt.tight_layout()
plt.show()
```

### Seaborn'da statistik chart'lar

```python
import seaborn as sns
import pandas as pd

# Titanic datasetni yuklash
df = sns.load_dataset("titanic")

# Tema o'rnatish
sns.set_theme(style="whitegrid", palette="muted")

# Categorical plot
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df, x="class", hue="survived", ax=ax)
ax.set_title("Survival by Class")
plt.show()

# Distribution
sns.histplot(data=df, x="age", hue="survived", multiple="stack", bins=30)
plt.title("Age distribution by survival")
plt.show()

# Pairplot — barcha features orasidagi munosabat
sns.pairplot(df[["age", "fare", "pclass", "survived"]].dropna(), hue="survived")
plt.show()

# Heatmap — correlation matrix
numeric_df = df.select_dtypes(include="number")
corr = numeric_df.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
ax.set_title("Correlation Matrix")
plt.show()
```

### Production uchun chiroyli style

```python
# Custom theme
plt.style.use("seaborn-v0_8-darkgrid")  # yoki "ggplot", "fivethirtyeight"

# Yoki to'liq custom
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "figure.dpi": 100,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})
```

## 🔌 Backend integratsiyasi

### 1. FastAPI'da chart endpoint (PNG qaytarish)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import matplotlib
matplotlib.use("Agg")  # MUHIM: backend uchun GUI yo'q
import matplotlib.pyplot as plt
import io

app = FastAPI()

@app.get("/chart/sales.png")
async def sales_chart():
    df = pd.read_sql("SELECT date, sales FROM daily_sales ORDER BY date", engine)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["date"], df["sales"], color="navy", linewidth=2)
    ax.fill_between(df["date"], df["sales"], alpha=0.3, color="navy")
    ax.set_title("Daily Sales")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sales (USD)")
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)  # MUHIM: memory leak'ning oldini olish
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")
```

### 2. Background report generation

```python
@celery_app.task
def generate_monthly_report(month: str):
    df = load_data(month)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Revenue trend
    df.set_index("date")["revenue"].plot(ax=axes[0, 0], title="Revenue")
    
    # Top categories
    df.groupby("category")["revenue"].sum().nlargest(10).plot.barh(ax=axes[0, 1])
    
    # User growth
    df.groupby("date")["new_users"].sum().plot(ax=axes[1, 0])
    
    # Correlation
    sns.heatmap(df.corr(), ax=axes[1, 1], annot=True, fmt=".2f")
    
    plt.tight_layout()
    fig.savefig(f"/reports/{month}.pdf", format="pdf")
    plt.close(fig)
    
    send_email_with_attachment(f"/reports/{month}.pdf")
```

### ⚠️ Server-side rendering uchun muhim eslatma

Backend'da matplotlib ishlatganda:
1. **`matplotlib.use("Agg")` qiling** — GUI backend yuklab olmaslik uchun
2. **`plt.close(fig)`** chaqiring — memory leak'ning oldini olish
3. **Thread safety** — matplotlib thread-safe emas. Gunicorn workers ishlatishingiz mumkin, lekin async kontekstda alohida thread'da chiqaring (`asyncio.to_thread`)

## 📚 Resurslar

- **Matplotlib official tutorials** — [matplotlib.org/stable/tutorials/](https://matplotlib.org/stable/tutorials/)
- **Seaborn gallery** — [seaborn.pydata.org/examples/](https://seaborn.pydata.org/examples/)
- **"Python Data Science Handbook"** — Jake VanderPlas (bepul online: [jakevdp.github.io](https://jakevdp.github.io/PythonDataScienceHandbook/))
- **"Storytelling with Data"** — Cole Nussbaumer Knaflic (chart design)
- **Plotly Express** — interaktiv chart'lar uchun: [plotly.com/python/plotly-express/](https://plotly.com/python/plotly-express/)

## 🏋️ Mashqlar

### 🟢 Easy
1. NumPy bilan 1000 ta tasodifiy son yarating, histogram'ini chizing (matplotlib).
2. Seaborn'da `iris` datasetni yuklab, `pairplot` qiling.
3. 2x2 subplot yarating, har birida boshqa chart turi bo'lsin.

### 🟡 Medium
1. Titanic datasetning correlation matrix'ini heatmap bilan chizing, `annot=True` va custom colormap bilan.
2. Custom theme yarating: shrift, ranglar, grid stili — uni `mlflow_style.py` modulida saqlang va boshqa loyihalarda import qiling.
3. Bitta `Figure`'da 2 ta y-axis bo'lgan chart yarating (`twinx`) — masalan, daily users va daily revenue bir xil x-axisda.

### 🔴 Hard
1. **FastAPI Dashboard**: `/api/charts/{chart_type}.png` endpoint yarating. Foydalanuvchi query parametrlari bilan `chart_type=line|bar|hist|scatter`, `data_source=...`, `title=...` jo'natadi, chiroyli PNG qaytadi. Caching qo'shing (Redis bilan).
2. **PDF report**: 10 sahifali multi-page PDF report yarating (matplotlib `PdfPages` ishlatib): kover sahifa, har bo'lim bo'yicha analytics, oxirida summary.

## 🚀 Capstone

`notebooks/month-01/03_visualization.ipynb`:
- COVID-19 yoki har qanday public time-series datasetni yuklang
- 6 ta turli chart turi bilan EDA report yarating (line, bar, hist, box, scatter, heatmap)
- Hammasi bitta `Figure`da, `GridSpec` ishlatib layout qiling
- PDF formatda saqlang

## ✅ Tekshirish ro'yxati

- [ ] `pyplot` API va OO API farqini bilaman
- [ ] `Figure` va `Axes` munosabatini tushunaman
- [ ] Subplot'lar yarata olaman, layout boshqaraman
- [ ] Seaborn'da heatmap, pairplot, distplot ishlatishni bilaman
- [ ] Custom style/theme yarata olaman
- [ ] Backend'da matplotlib ishlatishda `Agg` va `plt.close` ishlatamanligimni bilaman
- [ ] Chart'ni PNG, SVG, PDF formatlarida saqlay olaman

[EDA Capstone loyihasi](./05-eda-project.md) — endi haqiqiy ishga o'tamiz.
