# Regression

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Regression masalasi nima ekanini, qachon ishlatish kerakligini bilasiz
- Linear, Polynomial, Ridge, Lasso, ElasticNet farqini tushunasiz
- Regression metrik'larini (RMSE, MAE, R²) to'g'ri talqin qilasiz
- Real datasetda regression model qurib, FastAPI'da serve qilasiz

## Nimani o'rganish kerak

- **Linear Regression** — eng asosiy algoritm, har ML inj-ri biladi
- **Polynomial Regression** — noziq egilishlar
- **Regularization** — Ridge (L2), Lasso (L1), ElasticNet (L1+L2)
- **Feature scaling**ning regression'ga ta'siri
- **Multicollinearity** — feature'lar bir-biriga bog'liq bo'lganda
- **Assumption'lar** — linearity, normality, homoscedasticity (sodda darajada)
- **Metrik'lar** — MSE, RMSE, MAE, R², MAPE
- **Robust regression** — outlier'lar mavjud bo'lganda

## Kutubxonalar

```bash
pip install scikit-learn statsmodels
```

- **scikit-learn** — asosiy
- **statsmodels** — statistik tafsilotlar (p-value, confidence interval) kerak bo'lsa

## Muhim mavzular

### Linear Regression intuitsiyasi

Maqsad — `y = w₀ + w₁x₁ + w₂x₂ +... + wₙxₙ` shaklidagi chiziq topish:
- Faktiklarga (`y_true`) imkon qadar yaqin
- "Yaqinlik" o'lchovi — odatda **MSE**(Mean Squared Error)

Optimizatsiya: **Ordinary Least Squares (OLS)**yoki **Gradient Descent**.

### Regularization nima uchun kerak?

Agar feature'lar ko'p (ko'pincha kuzatuvlardan ko'p) yoki ular bir-biriga bog'liq bo'lsa, model `overfitting` qiladi. Yechim — **regularization**:

- **Ridge (L2):**`loss + λ * Σwᵢ²` — feature'larni nolga yaqinlashtiradi
- **Lasso (L1):**`loss + λ * Σ|wᵢ|` — ba'zi feature'larni **aniq nol qiladi**(feature selection)
- **ElasticNet:**ikkalasining aralashmasi

```
λ kichik (0)         λ o'rta              λ katta
Overfitting          Optimal               Underfitting
(model murakkab)                          (model oddiy)
```

### Linear assumption'lar

1. **Linearity** — y va X orasidagi munosabat haqiqatdan chiziqlimi?
2. **Independence** — kuzatuvlar mustaqil (time series uchun bu buziladi)
3. **Homoscedasticity** — xato variance'i bir xil (residual plot bilan tekshirish)
4. **Normality** — xatolar normal taqsimotda (Q-Q plot)
5. **No multicollinearity** — feature'lar bir-biriga juda bog'liq emas (VIF)

**Backend dev maslahat:**Bu assumption'larni bizga business uchun har doim tekshirish shart emas — `random forest` yoki `XGBoost` bularsiz ham ishlaydi. Lekin Linear Regression'da chiroyli natija olish uchun foydali.

### Metrik'lar — qaysi qachon?

| Metrik | Formula | Interpretatsiya | Qachon |
|--------|---------|-----------------|--------|
| **MAE** | `mean(|y - ŷ|)` | O'rtacha xato, xuddi o'lchov birligida | Outlier'larga bardoshli |
| **MSE** | `mean((y - ŷ)²)` | Kvadrat xato — katta xatolarni jazolaydi | Loss function uchun |
| **RMSE** | `sqrt(MSE)` | O'lchov birligida | Eng keng tarqalgan |
| **R²** | `1 - SSres/SStot` | 0..1 (yoki manfiy) — ma'lumotning necha % tushuntirilgan | Modelni baholash |
| **MAPE** | `mean(|y - ŷ| / |y|)` | Foizda — biznesga qulay | y > 0 bo'lganda |

## Kod misollari

### Linear Regression — California Housing

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

# 1. Data
data = fetch_california_housing(as_frame=True)
X, y = data.data, data.target  # y = uyning median narxi ($100k)

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("lr", LinearRegression()),
])
pipeline.fit(X_train, y_train)

# 4. Predict va metrik
y_pred = pipeline.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.3f}")  # 0.745
print(f"MAE:  {mae:.3f}")   # 0.533
print(f"R²:   {r2:.3f}")    # 0.576

# 5. Coefficient'lar
coefs = dict(zip(X.columns, pipeline.named_steps["lr"].coef_))
for name, c in sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {name}: {c:+.3f}")
```

### Ridge, Lasso, ElasticNet

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet

models = {
    "LinearRegression": LinearRegression(),
    "Ridge (L2)":       Ridge(alpha=1.0, random_state=42),
    "Lasso (L1)":       Lasso(alpha=0.01, random_state=42),
    "ElasticNet":       ElasticNet(alpha=0.01, l1_ratio=0.5, random_state=42),
}

for name, model in models.items():
    pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
    pipe.fit(X_train, y_train)
    score = pipe.score(X_test, y_test)  # R²
    print(f"{name:20s}  R² = {score:.4f}")
```

### Polynomial Regression

```python
from sklearn.preprocessing import PolynomialFeatures

poly_pipeline = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
    ("lr", LinearRegression()),
])
poly_pipeline.fit(X_train, y_train)
print(f"Polynomial R²: {poly_pipeline.score(X_test, y_test):.4f}")
```

### Hyperparameter tuning — GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

ridge_pipe = Pipeline([("scaler", StandardScaler()), ("ridge", Ridge())])

param_grid = {"ridge__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}

gs = GridSearchCV(ridge_pipe, param_grid, cv=5, scoring="neg_root_mean_squared_error")
gs.fit(X_train, y_train)

print(f"Best alpha: {gs.best_params_['ridge__alpha']}")
print(f"Best CV RMSE: {-gs.best_score_:.3f}")
```

## Backend integratsiyasi

### Price prediction API (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.model = joblib.load("models/california_housing_v1.joblib")
    yield

app = FastAPI(lifespan=lifespan, title="California Housing Price Predictor")

class HouseFeatures(BaseModel):
    MedInc: float = Field(..., gt=0, description="Median income (10k USD)")
    HouseAge: float = Field(..., ge=0, le=100)
    AveRooms: float = Field(..., gt=0)
    AveBedrms: float = Field(..., gt=0)
    Population: float = Field(..., gt=0)
    AveOccup: float = Field(..., gt=0)
    Latitude: float
    Longitude: float

class PricePrediction(BaseModel):
    predicted_price_100k: float
    predicted_price_usd: float

@app.post("/predict/", response_model=PricePrediction)
def predict_price(features: HouseFeatures):
    X = np.array([[
        features.MedInc, features.HouseAge, features.AveRooms,
        features.AveBedrms, features.Population, features.AveOccup,
        features.Latitude, features.Longitude,
    ]])
    pred = float(app.state.model.predict(X)[0])
    return PricePrediction(
        predicted_price_100k=pred,
        predicted_price_usd=pred * 100_000,
    )
```

### Logging va monitoring (boshlang'ich)

```python
import logging
from datetime import datetime

logger = logging.getLogger("ml_service")

@app.post("/predict/", response_model=PricePrediction)
def predict_price(features: HouseFeatures):
    start = datetime.now()
    X = np.array([list(features.dict().values())])
    pred = float(app.state.model.predict(X)[0])
    duration_ms = (datetime.now() - start).total_seconds() * 1000
    
    logger.info(
        "prediction",
        extra={
            "input": features.dict(),
            "prediction": pred,
            "duration_ms": duration_ms,
            "model_version": "v1",
        },
    )
    return PricePrediction(predicted_price_100k=pred, predicted_price_usd=pred * 100_000)
```

## Resurslar

- **Scikit-learn Regression** — [scikit-learn.org/stable/supervised_learning.html#regression](https://scikit-learn.org/stable/supervised_learning.html)
- **StatQuest — Linear Regression**([YouTube](https://www.youtube.com/watch?v=nk2CQITm_eo))
- **StatQuest — Ridge, Lasso, ElasticNet**(3 ta alohida video)
- **"Introduction to Statistical Learning"**(ISLR) — bepul PDF, regression chuqur
- **Andrew Ng — ML Specialization Course 1**(Linear Regression module)

## 🏋️ Mashqlar

### 🟢 Easy
1. `sklearn.datasets.load_diabetes()` da Linear Regression train qiling, R² chiqaring.
2. Ridge'da `alpha = [0.001, 0.01, 0.1, 1, 10, 100]` ni sinab, R² qanday o'zgarishini chizing.
3. Train va test R² ni solishtiring — qachon overfitting bo'lyapti?

### 🟡 Medium
1. **California Housing**: Linear, Ridge, Lasso, ElasticNet, Polynomial — barchasini solishtiring jadval shaklida.
2. **Manual gradient descent**: Linear Regression'ni numpy bilan o'zingiz yozing (sklearn ishlatmasdan).
3. **Residual analysis**: `y_test - y_pred` ni vizualizatsiya qiling. Pattern bormi? (homoscedasticity check)

### 🔴 Hard
1. **Production servis**: California Housing modelini Docker + FastAPI + Postgres (predictions log uchun). Healthcheck, Prometheus metrics (`request_count`, `prediction_duration`).
2. **A/B test infra**: bir vaqtda ikkita model serve qiling (`v1` va `v2`), traffic'ni 50/50 bo'ling, har biri uchun alohida metric'lar yig'ing.

## Capstone

`notebooks/month-02/01_regression.ipynb`:
- **Kaggle — House Prices: Advanced Regression Techniques**competition
- Birinchi marta submit qiling
- Maqsad: top 50% (RMSE log <= 0.16)
- Steps: EDA → preprocessing → Ridge bilan baseline → feature engineering → Lasso bilan feature selection → submission

## ✅ Tekshirish ro'yxati

- [ ] Linear Regression'ning matematik formulasini tushunaman (y = wx + b)
- [ ] Ridge va Lasso farqini bilaman (L1 vs L2)
- [ ] RMSE va MAE'ni qachon ishlatishni bilaman
- [ ] R² ning ma'nosini biznesga tushuntira olaman
- [ ] Pipeline yarata olaman (scaler + model)
- [ ] GridSearchCV bilan hyperparameter tune qilaman
- [ ] FastAPI'da regression model serve qildim
- [ ] Birinchi Kaggle submission qildim

[Classification](./03-classification.md) ga o'tamiz.
