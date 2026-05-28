# Feature Engineering

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Feature Engineering ML loyihasining 60-80% vaqtini olishini bilasiz
- Categorical, numerical va datetime feature'larni to'g'ri tayyorlay olasiz
- Yangi feature'lar yaratish (domain-based) san'atini o'rganasiz
- Feature selection texnikalari bilan dimensionality'ni kamaytirasiz
- PCA va boshqa dimensionality reduction texnikalarini ishlatasiz

## 📖 Nimani o'rganish kerak

- **Scaling**: StandardScaler, MinMaxScaler, RobustScaler, Normalizer
- **Encoding**: OneHot, Label, Ordinal, Target, Frequency, Binary
- **Missing data**: SimpleImputer, KNNImputer, IterativeImputer
- **Feature creation**: polynomial, interaction, binning, datetime extraction
- **Text features**: BoW, TF-IDF, n-grams
- **Feature selection**: Filter, Wrapper, Embedded methods
- **Dimensionality reduction**: PCA, LDA, t-SNE, UMAP
- **Outliers**: detection (IQR, z-score) va treatment

## 📦 Kutubxonalar

```bash
pip install scikit-learn category_encoders feature-engine
```

- **scikit-learn** — asosiy
- **category_encoders** — kengaytirilgan encoding (Target, James-Stein, h.k.)
- **feature-engine** — feature engineering pipeline'lari

## 🧠 Muhim mavzular

### Feature Engineering — ML'ning aysbergi

```
   ML algoritmi (10%)
   ───────────────────  ← ko'rinadigan qism
       Feature Engineering (60%)
       Data Quality (20%)
       Domain Knowledge (10%)
```

**Andrew Ng:** "Coming up with features is difficult, time-consuming, requires expert knowledge. Applied machine learning is basically feature engineering."

### Scaling — qachon va qaysi?

| Scaler | Formula | Qachon |
|--------|---------|--------|
| **StandardScaler** | `(x - μ) / σ` | Default, normal distribution'ga moslashtiradi |
| **MinMaxScaler** | `(x - min) / (max - min)` | Neural networks (ranglar uchun [0,1]) |
| **RobustScaler** | `(x - median) / IQR` | Outlier'lar mavjud bo'lganda |
| **Normalizer** | `x / ||x||` | Vektor normasini 1 ga keltirish |

**Qoidalar:**
- Distance-based algoritmlar (KNN, SVM, K-Means) — scaling **shart**
- Tree-based (Random Forest, XGBoost) — scaling **shart emas**
- Linear models — scaling **tavsiya etiladi** (regularization uchun)

### Categorical Encoding

```python
# Cat values: ['cat', 'dog', 'fish']

# 1. Label Encoding (faqat ordinal data uchun!)
[0, 1, 2]  # ['cat'=0, 'dog'=1, 'fish'=2] — soxta tartib!

# 2. OneHot Encoding (nominal data uchun)
cat: [1, 0, 0]
dog: [0, 1, 0]
fish:[0, 0, 1]

# 3. Target Encoding (high cardinality uchun)
# Har category uchun target'ning o'rta qiymati
cat: 0.5    # avg(y | category=cat)
dog: 0.3
fish: 0.7
```

### High Cardinality muammosi

Agar feature'da **1000+ unique value** bo'lsa (masalan, `user_id`, `city`), OneHot encoding 1000 ustun yaratadi va overfitting'ga olib keladi.

**Yechimlar:**
1. **Target encoding** — mean(y) bilan almashtirish (CV ichida!)
2. **Frequency encoding** — har category'ning hisobi
3. **Embedding** — neural network (chuqurroq oyda)
4. **Hashing** — `HashingEncoder`
5. **Grouping** — kam uchraydiganlarni "Other" ga birlashtirish

### Datetime feature'lari

```python
import pandas as pd

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.dayofweek
df["weekend"] = df["weekday"].isin([5, 6]).astype(int)
df["hour"] = df["date"].dt.hour
df["quarter"] = df["date"].dt.quarter

# Cyclic encoding (vakt davriy bo'lgani uchun)
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
```

### Feature Selection — 3 ta yondashuv

1. **Filter methods** (algoritmsiz)
   - Variance Threshold (variansi past feature'larni o'chirish)
   - Correlation-based (target bilan korrelyatsiya)
   - Chi-squared test (categorical uchun)
   - Mutual Information

2. **Wrapper methods** (algoritm bilan)
   - Recursive Feature Elimination (RFE)
   - Sequential Forward/Backward Selection

3. **Embedded methods** (algoritm ichida)
   - Lasso (L1) → coefficient = 0 bo'lgan feature'lar o'chiriladi
   - Tree-based feature importance

## 💻 Kod misollari

### To'liq ColumnTransformer pipeline

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

numeric_features = ["age", "income", "tenure"]
nominal_features = ["city", "department"]
ordinal_features = ["education"]
education_order = [["primary", "secondary", "bachelor", "master", "phd"]]

# Numeric pipeline
numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

# Nominal categorical pipeline
nominal_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

# Ordinal pipeline
ordinal_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("ord", OrdinalEncoder(categories=education_order)),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("nom", nominal_pipe, nominal_features),
    ("ord", ordinal_pipe, ordinal_features),
])

full_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", LogisticRegression()),
])
```

### Target Encoding (with cross-validation, leak-free)

```python
from category_encoders import TargetEncoder
from sklearn.model_selection import cross_val_score

# Diqqat: oddiy TargetEncoder leak qiladi (target ni preprocessor ko'radi)
# To'g'ri yo'l — Pipeline ichida

pipeline = Pipeline([
    ("encoder", TargetEncoder(cols=["city", "category"])),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])

# CV ichida har fold uchun encoder qayta fit qilinadi
scores = cross_val_score(pipeline, X, y, cv=5)
```

### PCA — Dimensionality Reduction

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Scale (PCA scaling'ga sezgir)
X_scaled = StandardScaler().fit_transform(X)

# 95% variance saqlanadigan komponentlar
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

print(f"Original features: {X.shape[1]}")
print(f"PCA components:    {X_pca.shape[1]}")
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.3f}")

# Scree plot
import matplotlib.pyplot as plt
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel("Number of components")
plt.ylabel("Cumulative explained variance")
plt.axhline(0.95, color="r", linestyle="--")
plt.show()
```

### Feature Selection misoli

```python
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier

# 1. SelectKBest (filter)
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()]

# 2. RFE (wrapper)
rfe = RFE(estimator=RandomForestClassifier(random_state=42), n_features_to_select=10)
rfe.fit(X, y)
selected_rfe = X.columns[rfe.support_]

# 3. Feature importance (embedded)
rf = RandomForestClassifier(random_state=42)
rf.fit(X, y)
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_,
}).sort_values("importance", ascending=False)
```

### Domain-based feature creation

```python
# E-commerce datasetda yangi feature'lar
df["price_per_item"] = df["total_price"] / df["quantity"]
df["discount_pct"] = (df["original_price"] - df["price"]) / df["original_price"]
df["is_weekend"] = df["order_date"].dt.dayofweek.isin([5, 6]).astype(int)
df["days_since_signup"] = (df["order_date"] - df["signup_date"]).dt.days
df["customer_lifetime_orders"] = df.groupby("customer_id")["order_id"].transform("count")
df["avg_order_value"] = df.groupby("customer_id")["total_price"].transform("mean")
```

## 🔌 Backend integratsiyasi

### Feature Store pattern

```python
# Backend'da feature engineering — Django service
class FeatureService:
    def compute_user_features(self, user_id: int) -> dict:
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user=user)
        
        return {
            "user_age_days": (timezone.now() - user.created_at).days,
            "total_orders": orders.count(),
            "avg_order_value": orders.aggregate(Avg("amount"))["amount__avg"] or 0,
            "days_since_last_order": (
                timezone.now() - orders.latest("created_at").created_at
            ).days if orders.exists() else 999,
            "preferred_category": orders.values("category")
                .annotate(n=Count("id")).order_by("-n").first()["category"]
                if orders.exists() else None,
        }

# FastAPI'da
@app.post("/predict/")
def predict(user_id: int):
    features = feature_service.compute_user_features(user_id)
    pipeline = joblib.load("model.joblib")  # ColumnTransformer + model
    
    df = pd.DataFrame([features])
    prediction = pipeline.predict(df)[0]
    return {"prediction": float(prediction)}
```

### Feature versioning

```python
# config.py
FEATURE_SCHEMA_V1 = {
    "version": "1.0",
    "numeric": ["age", "income"],
    "categorical": ["city", "department"],
}

# Model bilan birga schema'ni saqlash
joblib.dump({
    "pipeline": full_pipeline,
    "feature_schema": FEATURE_SCHEMA_V1,
    "trained_at": datetime.now().isoformat(),
}, "model_bundle.joblib")
```

## 📚 Resurslar

- **"Feature Engineering for Machine Learning"** — Alice Zheng, Amanda Casari (O'Reilly)
- **scikit-learn Preprocessing docs** — [scikit-learn.org/stable/modules/preprocessing.html](https://scikit-learn.org/stable/modules/preprocessing.html)
- **category_encoders docs** — [contrib.scikit-learn.org/category_encoders](https://contrib.scikit-learn.org/category_encoders/)
- **"Feature Engineering A-Z"** — Kaggle tutorial
- **Feast (Feature Store)** — [feast.dev](https://feast.dev/) — production feature storage

## 🏋️ Mashqlar

### 🟢 Easy
1. `StandardScaler`, `MinMaxScaler`, `RobustScaler` ni outlier'lar bilan datasetda solishtiring.
2. `OneHotEncoder` va `OrdinalEncoder` farqini misol bilan ko'rsating.
3. `pd.cut` ishlatib continuous `age` ni `[child, teen, adult, senior]` bin'larga ajrating.

### 🟡 Medium
1. **Datetime FE**: NYC Taxi datasetda `pickup_datetime`dan 10+ ta yangi feature yarating (hour, weekday, season, holiday, rush_hour, h.k.).
2. **Target Encoding leak'ni ko'rish**: target encoding'ni CV ichida va tashqarisida qilib R² farqini ko'ring.
3. **PCA + classification**: yuqori o'lchamli digit dataset'da PCA bilan dimensionality'ni 20'ga kamaytirib, classifier'ning accuracy va training time o'zgarishini ko'ring.

### 🔴 Hard
1. **Production feature store**: Django'da `FeatureService` class yarating — har user uchun real-time feature'larni hisoblaydi, Redis'da cache qiladi (TTL=1h), ML pipeline bilan integratsiya.
2. **Auto FE**: AutoML kutubxonalaridan biri (`featuretools`, `tsfresh`) bilan automatic feature engineering qilib, manual FE bilan solishtiring.

## 🚀 Capstone

`notebooks/month-02/04_feature_engineering.ipynb`:
- Telco Churn datasetni qayta oching
- 30+ ta yangi feature yarating (datetime, ratios, aggregations, interactions)
- Feature importance ranking
- PCA bilan eksperiment
- Original vs FE qilingan model — accuracy farqini ko'rsating

## ✅ Tekshirish ro'yxati

- [ ] Feature Engineering ML'ning eng muhim qismi ekanini tushunaman
- [ ] 4 ta scaler turini bilaman, qaysi qachon ishlatishni
- [ ] Categorical encoding turlarini va high cardinality muammosini bilaman
- [ ] Datetime'dan kamida 10 ta feature yarata olaman
- [ ] PCA va dimensionality reduction nima uchun kerakligini tushunaman
- [ ] Feature selection uchun 3 ta usulni bilaman
- [ ] ColumnTransformer + Pipeline bilan to'liq preprocessing yozaman
- [ ] Target encoding'da leak muammosini bilaman

[Model Evaluation](./06-model-evaluation.md) ga o'tamiz.
