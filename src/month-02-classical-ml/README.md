# Oy 2 — Klassik ML (Scikit-learn)

## 🎯 Bu oydagi maqsad

Oy oxirida siz quyidagilarni qilolasiz:
- Real biznes muammosini ML masalasiga aylantirish (regression / classification / clustering)
- Scikit-learn bilan to'liq ML pipeline qurish
- Modelni baholash va xato turlarini tushunish
- XGBoost/LightGBM bilan production darajadagi modellar yaratish
- Kaggle competition'da qatnashish va top 30%'ga kirish

## Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | ML asoslari + Regression | 10-12 soat |
| **Hafta 2** | Classification + Clustering | 10-12 soat |
| **Hafta 3** | Feature Engineering + Evaluation | 8-10 soat |
| **Hafta 4** | Ensembles (XGBoost/LightGBM) + Kaggle | 12-15 soat |

## Boblar tartibi

1. [ML ga kirish](./01-ml-intro.md) — terminlar, jarayon, training/test split
2. [Regression](./02-regression.md) — uzluksiz qiymatni bashorat qilish
3. [Classification](./03-classification.md) — sinflarga ajratish
4. [Clustering](./04-clustering.md) — unsupervised guruhlash
5. [Feature Engineering](./05-feature-engineering.md) — feature'larni tayyorlash va yaratish
6. [Model Evaluation](./06-model-evaluation.md) — metrik va validation
7. [Ensemble Methods](./07-ensemble-methods.md) — Random Forest, XGBoost, LightGBM
8. [Mashqlar](./exercises.md) — qo'shimcha mashqlar va Kaggle topshiriqlari

## Oy oxirida nima qila olasiz?

- Tabular ma'lumotlarda 80% problemalarni hal qilish (regression, classification, clustering)
- Scikit-learn `Pipeline` yordamida reproducible kod yozish
- Modelni `joblib` bilan saqlash va FastAPI'da serve qilish
- XGBoost/LightGBM bilan Kaggle'da top 30%
- ML modelining biznes uchun **ROI**ni tushuntirish

## Backend Dev uchun maslahat

Backend'da REST API yozish kabi, ML'da `fit() → predict()` pattern bor:

```python
# Backend pattern
@app.post("/users")
def create_user(data: UserIn):
    user = User(**data.dict())
    db.add(user)
    return user

# ML pattern
model = LogisticRegression()
model.fit(X_train, y_train)        # "train" qilish
predictions = model.predict(X_test) # "predict" qilish
```

Bu pattern barcha sklearn modellarda bir xil — agar `LinearRegression`ni bilsangiz, `RandomForest`ni ham bilasiz.

## MLOps integration (boshidan)

Backend dev'ning ustunligi — `production thinking`. Birinchi modelni yozayotganingizda allaqachon o'ylang:

1. **Reproducibility** — `random_state=42` har joyda
2. **Saqlash** — `joblib.dump(model, 'model.pkl')`
3. **Versioning** — `model_v1.pkl`, `model_v2.pkl`
4. **Schema** — Pydantic bilan input/output validation
5. **Logging** — har bashorat uchun timestamp va input

Bu mavzular Oy 6 (MLOps)'da chuqurroq, lekin **birinchi kunidan boshlang**.

## Boshlash

[ML ga kirish](./01-ml-intro.md) bilan boshlang.
