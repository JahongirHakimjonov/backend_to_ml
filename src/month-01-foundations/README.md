# Oy 1 — Foundations (Asoslar)

## 🎯 Bu oydagi maqsad

Oy oxirida siz quyidagilarni bila olasiz:
- Matematika asoslari (linear algebra, calculus, statistika) ML kontekstida
- NumPy bilan vektor va matritsalarni samarali qayta ishlash
- Pandas bilan real ma'lumotlarni tahlil qilish
- Matplotlib/Seaborn bilan ma'lumotlarni vizualizatsiya qilish
- Tugatish: real datasetda to'liq EDA (Exploratory Data Analysis) report yozish

## Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | Matematika asoslari + NumPy | 8-12 soat |
| **Hafta 2** | Pandas (Series, DataFrame, groupby) | 8-12 soat |
| **Hafta 3** | Matplotlib + Seaborn | 6-10 soat |
| **Hafta 4** | EDA Capstone loyihasi | 10-15 soat |

## Boblar tartibi

1. [Matematika asoslari](./01-math-basics.md) — Linear algebra, calculus, statistika
2. [NumPy](./02-numpy.md) — Tezkor vektor/matritsa operatsiyalari
3. [Pandas](./03-pandas.md) — Tabular data bilan ishlash
4. [Matplotlib va Seaborn](./04-matplotlib-seaborn.md) — Vizualizatsiya
5. [EDA loyihasi (Capstone)](./05-eda-project.md) — To'liq amaliy loyiha
6. [Mashqlar](./exercises.md) — Barcha mavzular bo'yicha mashqlar to'plami

## Bu oydan keyin nima qila olasiz?

- Kaggle'dagi har qanday tabular datasetni o'qib, tahlil qila olasiz
- Backend'da kelayotgan JSON ma'lumotlarini DataFrame'ga aylantirib, statistika chiqarib bera olasiz
- ML loyihalarida 60-80% vaqt sarflanadigan "data wrangling" qismini bajara olasiz
- Mijozga hisobot tayyorlash uchun chiroyli grafiklar chiza olasiz

## Backend Dev uchun maslahat

Sizning advantage'ingiz — `JSON`, `dict`, `list` bilan ishlash. Pandas DataFrame'ni "in-memory PostgreSQL table" deb tasavvur qiling:
- `df.head()` ≈ `SELECT * FROM table LIMIT 5`
- `df.groupby('col').sum()` ≈ `SELECT col, SUM(...) FROM table GROUP BY col`
- `df.merge(df2)` ≈ `JOIN`
- `df.query("age > 30")` ≈ `WHERE age > 30`

Bu mental model bilan Pandas'ni juda tez tushunasiz.

## Boshlash

[Matematika asoslari](./01-math-basics.md) bilan boshlang.
