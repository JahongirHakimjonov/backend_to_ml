# Month 01 — Foundations Notebooks

## 📝 Notebook'lar ro'yxati

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `00_math_warmup.ipynb` | Matematik asoslar | [Math basics](../../src/month-01-foundations/01-math-basics.md) |
| `01_numpy_basics.ipynb` | NumPy mashqlari | [NumPy](../../src/month-01-foundations/02-numpy.md) |
| `02_pandas_practice.ipynb` | Pandas EDA | [Pandas](../../src/month-01-foundations/03-pandas.md) |
| `03_visualization.ipynb` | Matplotlib + Seaborn | [Visualization](../../src/month-01-foundations/04-matplotlib-seaborn.md) |
| `04_eda_titanic.ipynb` | Titanic EDA | [EDA project](../../src/month-01-foundations/05-eda-project.md) |
| `capstone_house_prices_eda.ipynb` | Capstone EDA | [EDA project](../../src/month-01-foundations/05-eda-project.md) |

## 🛠 Dependencies (faqat shu oy uchun)

```bash
# uv bilan (loyiha root'idan)
uv sync --group month-01

# Jupyter ishga tushirish
uv run jupyter lab
```

Dependencies ro'yxati `pyproject.toml`'dagi `[dependency-groups.month-01]` da: scipy, sympy, missingno, ydata-profiling (numpy/pandas/matplotlib core'da bor).

## 📚 Datasets

| Dataset | Source |
|---------|--------|
| Titanic | Kaggle / sklearn |
| House Prices (Ames) | Kaggle |
| California Housing | sklearn.datasets |
| Iris | sklearn.datasets |

## 💡 Maslahatlar

1. Har notebook'ni o'qib o'tib chiqing, keyin o'zingiz tepa tomondan boshlang
2. Har bobning checklist'ini bajarib chiqing
3. Capstone — to'liq EDA report (markdown + charts)

Notebook'larni mustaqil yarating — har biri uchun maqsad va talablar [asosiy bobda](../../src/month-01-foundations/README.md) yozilgan.
