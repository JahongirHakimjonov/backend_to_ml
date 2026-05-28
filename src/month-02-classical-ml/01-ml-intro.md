# ML ga kirish

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Machine Learning nima ekanini, qachon ishlatish kerakligini tushunasiz
- Supervised, Unsupervised va Reinforcement learning farqini bilasiz
- Training, Validation, Test sets nima uchun kerakligini bilasiz
- Overfitting va Underfitting muammolarini taniysiz
- Bitta to'liq ML pipeline yozasiz (idea → data → model → evaluation)

## 📖 Nimani o'rganish kerak

- **ML nima va qachon kerak** (kogda mendan tashlanmaslik kerak)
- **ML masala turlari** — supervised vs unsupervised vs reinforcement
- **Supervised tasks** — regression vs classification
- **Train / Validation / Test** — nima uchun 3 ga bo'lamiz
- **Overfitting va Underfitting** — bias-variance tradeoff
- **Cross-validation** — k-fold strategiyasi
- **Scikit-learn API design** — `fit`, `predict`, `transform`, `fit_transform`
- **Pipeline va ColumnTransformer**

## 📦 Kutubxonalar

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
```

Asosiy versiya: **scikit-learn 1.4+**.

## 🧠 Muhim mavzular

### ML qachon kerak emas?

Backend dev sifatida, **agar oddiy `if/else` qoidalar ishlasa — ML ishlatmang**. ML kerak bo'lgan vaziyatlar:

✅ Qoidalar juda ko'p va o'zgaruvchan (spam filter)
✅ Pattern murakkab (rasm tanish, til tarjima)
✅ Personalization (har foydalanuvchi uchun alohida)
✅ Bashorat (kelajakdagi sotuv, kasallik xavfi)

❌ Aniq formula bor (`area = π * r²`)
❌ Kam ma'lumot (10 ta misol — ML emas, qoida yozing)
❌ Critical safety (boshqaruvsiz ML — xavfli)
❌ Explainability talab qilinadi va ML black-box

### ML masala turlari

```
1. Supervised Learning (input → output mavjud)
   ├── Regression: continuous output
   │   └── Misol: uy narxi, harorat, foydalanuvchi LTV
   └── Classification: discrete classes
       ├── Binary: spam/not-spam, churn/retain
       └── Multi-class: rasm turi, kasallik turi

2. Unsupervised Learning (faqat input)
   ├── Clustering: o'xshashlarni guruhlash
   ├── Dimensionality reduction: PCA, t-SNE
   └── Anomaly detection: g'ayrioddiy nuqtalar

3. Reinforcement Learning (agent + reward)
   └── O'yinlar, robotics, recommendation systems
```

### Train / Validation / Test bo'lish

**Nima uchun?** Model "kelajakdagi" ma'lumotlarda qanday ishlashini baholash uchun.

```
Hammasi (100%)
├── Training set (60-70%)    — model o'rganadi
├── Validation set (15-20%)  — hyperparameter tuning
└── Test set (15-20%)        — yakuniy baholash (faqat 1 marta!)
```

**Muhim qoida:** Test set'ni model train qilayotganda **ko'rmaslik kerak**. Aks holda — `data leakage` va noto'g'ri natija.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### Overfitting vs Underfitting

```
Underfitting          Just right            Overfitting
   .                     .                     .
  / \                   / \                   /\/\
 /   \                 /   \                 /    \
/     \               /     \               /      \
Model juda             Model muvozanatda      Model trainni
oddiy                                         yodlab olgan
```

| | Training accuracy | Test accuracy |
|---|---|---|
| Underfitting | Past | Past |
| Just right | Yuqori | Yuqori |
| Overfitting | Juda yuqori | Past |

**Yechimlar:**
- Underfitting: murakkabroq model, ko'proq feature
- Overfitting: regularization, ko'proq data, oddiyroq model, cross-validation

### Cross-validation

Bitta train/test split ba'zan adolatli emas. Yechim — **k-fold cross-validation**:

```
5-fold CV:
Fold 1: Test=[1], Train=[2,3,4,5]
Fold 2: Test=[2], Train=[1,3,4,5]
Fold 3: Test=[3], Train=[1,2,4,5]
Fold 4: Test=[4], Train=[1,2,3,5]
Fold 5: Test=[5], Train=[1,2,3,4]
→ 5 ta accuracy → mean ± std
```

## 💻 Kod misollari

### To'liq pipeline misoli (Iris classification)

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Data yuklash
iris = load_iris(as_frame=True)
X, y = iris.data, iris.target

# 2. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Pipeline yaratish (preprocessing + model bir joyda)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
])

# 4. Train
pipeline.fit(X_train, y_train)

# 5. Predict va baholash
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 6. Saqlash
joblib.dump(pipeline, "iris_model.joblib")
```

### Cross-validation

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
print(f"Each fold: {scores}")
```

### ColumnTransformer (mixed types)

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Numerik va categorical ustunlar uchun alohida preprocessing
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["age", "salary"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city", "department"]),
])

full_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression()),
])

full_pipeline.fit(X_train, y_train)
```

## 🔌 Backend integratsiyasi

### FastAPI'da ML model serve qilish (minimal)

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("iris_model.joblib")

CLASS_NAMES = ["setosa", "versicolor", "virginica"]

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisPrediction(BaseModel):
    class_name: str
    confidence: float

@app.post("/predict", response_model=IrisPrediction)
def predict(data: IrisInput):
    X = np.array([[data.sepal_length, data.sepal_width, 
                   data.petal_length, data.petal_width]])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    return IrisPrediction(
        class_name=CLASS_NAMES[pred],
        confidence=float(proba.max()),
    )

@app.get("/health")
def health():
    return {"status": "ok", "model_version": "v1"}
```

```bash
uvicorn main:app --reload
# POST http://localhost:8000/predict
# {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
```

### Best practices for ML serving

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Model'ni faqat bir marta yuklash (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("iris_model.joblib")
    app.state.model_version = "v1.2.0"
    yield
    # cleanup if needed

app = FastAPI(lifespan=lifespan)
```

## 📚 Resurslar

- **Scikit-learn User Guide** — [scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html)
- **"Hands-On Machine Learning"** — Aurélien Géron (3-nashr) — **MUST READ** kitob
- **Andrew Ng — Machine Learning Specialization** (Coursera) — bepul auditing
- **StatQuest** — ML algoritmlarini eng yaxshi tushuntiruvchi YouTube
- **Kaggle Learn** — Intro to Machine Learning (bepul mini-course)

## 🏋️ Mashqlar

### 🟢 Easy
1. `sklearn.datasets.load_wine()` yuklang, `LogisticRegression` bilan classify qiling, accuracy chiqaring.
2. `train_test_split` da `random_state` ni o'zgartirib bir necha marta natija olib, farqni ko'ring.
3. `cross_val_score` bilan 3-fold va 10-fold CV solishtiring.

### 🟡 Medium
1. **Pipeline misoli**: Titanic dataset uchun `Pipeline` yarating — `SimpleImputer` + `OneHotEncoder` + `StandardScaler` + `LogisticRegression`.
2. **Stratification**: Imbalanced datasetda `stratify=y` ishlatish va ishlatmaslik farqini ko'ring.
3. **Overfitting demo**: bitta xususiyatli regressionga `PolynomialFeatures(degree=20)` qo'shing va overfitting'ni vizual ko'rsating.

### 🔴 Hard
1. **FastAPI ML servis**: Iris classifier'ni Docker'da containerize qiling, GitHub Actions bilan CI/CD qo'shing, healthcheck endpoint yarating. Bu ish 6-oydagi MLOps loyihasi uchun asos bo'ladi.
2. **Custom Estimator**: o'zingizning `BaseEstimator` va `TransformerMixin`'dan inherit qiluvchi custom transformer yarating — `Pipeline` ichida ishlatish mumkin bo'lsin.

## 🚀 Capstone

`notebooks/month-02/00_ml_intro.ipynb`:
- **California Housing** datasetni yuklang (`sklearn.datasets.fetch_california_housing`)
- Train/test split, `LinearRegression` train qiling
- Cross-validation bilan baholang (RMSE)
- Pipeline shaklida yozing (`StandardScaler` + `LinearRegression`)
- FastAPI endpoint yarating va `curl` bilan test qiling

## ✅ Tekshirish ro'yxati

- [ ] Supervised vs Unsupervised farqini bilaman
- [ ] Regression va Classification masalalarini ajrata olaman
- [ ] Train/Validation/Test bo'lish nima uchun kerakligini tushunaman
- [ ] Overfitting va Underfitting'ni ko'rganda taniyman
- [ ] Cross-validation kodida yozaman
- [ ] Scikit-learn Pipeline va ColumnTransformer ishlataman
- [ ] Modelni saqlash va FastAPI'da serve qilishni bilaman
- [ ] `random_state=42` ning ahamiyatini tushunaman

[Regression](./02-regression.md) ga o'tamiz.
