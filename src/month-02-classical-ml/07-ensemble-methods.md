# Ensemble Methods (XGBoost, LightGBM, CatBoost)

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Ensemble methods (Bagging, Boosting, Stacking) farqini tushunasiz
- Random Forest, XGBoost, LightGBM, CatBoost'ni qachon ishlatishni bilasiz
- Tabular data'da Kaggle competition'da yaxshi natija olishni bilasiz
- Gradient Boosting algoritmlarini production'da deploy qila olasiz

## 📖 Nimani o'rganish kerak

- **Bagging**: Random Forest, Extra Trees
- **Boosting**: AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost
- **Stacking**: meta-learner, blending
- **Voting**: hard vs soft voting
- **Feature importance** — Gini, permutation, SHAP
- **Hyperparameter tuning** — XGBoost/LightGBM uchun maxsus
- **Early stopping** — overfitting'ning oldini olish
- **Categorical handling** — CatBoost'ning afzalligi

## 📦 Kutubxonalar

```bash
pip install scikit-learn xgboost lightgbm catboost shap
```

## 🧠 Muhim mavzular

### Bagging vs Boosting

```
Bagging (Bootstrap Aggregating):
- Parallel: har model bir-biriga bog'liq emas
- Random Forest = Bagging + Decision Trees + random features
- Maqsad: variance kamaytirish (overfitting'ni)

Boosting:
- Sequential: har model oldingisining xatolarini tuzatishga harakat qiladi
- Gradient Boosting, XGBoost, LightGBM, CatBoost
- Maqsad: bias kamaytirish (underfitting'ni)
```

### Gradient Boosting algoritmi

```
1. F₀(x) = mean(y)  ← boshlang'ich bashorat
2. Repeat (M ta marta):
   a. r_i = y_i - F_{m-1}(x_i)   ← residual (xato)
   b. Yangi tree h_m(x) — r ni bashorat qilish uchun
   c. F_m(x) = F_{m-1}(x) + learning_rate * h_m(x)
3. Final: F_M(x)
```

### Qaysi gradient boosting?

| | XGBoost | LightGBM | CatBoost |
|---|---------|----------|----------|
| **Tezligi** | O'rta | ⚡⚡⚡ Eng tez | O'rta |
| **Aniqligi** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Categorical** | OneHot kerak | OneHot kerak | Avtomatik |
| **Memory** | O'rta | Past | O'rta |
| **Hyperparam** | Ko'p | Ko'p | Kam (yaxshi default) |
| **Documentation** | Ajoyib | Yaxshi | Yaxshi |
| **Industry adoption** | Eng katta | Katta | O'sib bormoqda |

**Maslahat:** Birinchi bo'lib **LightGBM** (tez), keyin **XGBoost** (stable), oxirida **CatBoost** (categorical ko'p bo'lsa).

### Eng muhim hyperparameter'lar (LightGBM/XGBoost)

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `n_estimators` | Tree'lar soni | 100 | 100-10000 |
| `learning_rate` | Qadam kattaligi | 0.1 | 0.01-0.3 |
| `max_depth` | Tree chuqurligi | -1 (unlimited) | 3-15 |
| `num_leaves` (LGBM) | Yaproq soni | 31 | 15-256 |
| `min_child_samples` | Yaproqda min samples | 20 | 1-100 |
| `subsample` | Row sampling | 1.0 | 0.5-1.0 |
| `colsample_bytree` | Feature sampling | 1.0 | 0.5-1.0 |
| `reg_alpha` (L1) | L1 regularization | 0 | 0-10 |
| `reg_lambda` (L2) | L2 regularization | 1 | 0-10 |

### Early Stopping

```python
# Validation loss yaxshilanmasa, training to'xtaydi
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,
)
# best_iteration ni saqlaydi
```

## 💻 Kod misollari

### Random Forest

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="sqrt",
    n_jobs=-1,
    random_state=42,
    class_weight="balanced",
)

scores = cross_val_score(rf, X, y, cv=5, scoring="f1")
print(f"F1: {scores.mean():.3f} ± {scores.std():.3f}")

# Feature importance
rf.fit(X, y)
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_,
}).sort_values("importance", ascending=False).head(10)
print(importance_df)
```

### XGBoost

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    eval_metric="logloss",
    early_stopping_rounds=50,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)

print(f"Best iteration: {model.best_iteration}")
print(f"Best score: {model.best_score:.4f}")
```

### LightGBM

```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=2000,
    learning_rate=0.05,
    num_leaves=63,
    max_depth=-1,
    min_child_samples=20,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced",
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric="auc",
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)],
)

print(f"Best iter: {model.best_iteration_}")
```

### CatBoost — Categorical Magic

```python
from catboost import CatBoostClassifier

cat_features = ["city", "department", "education"]  # ustun nomlari

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    l2_leaf_reg=3,
    cat_features=cat_features,  # automatic handling!
    early_stopping_rounds=50,
    random_seed=42,
    verbose=100,
)

model.fit(X_train, y_train, eval_set=(X_val, y_val))
```

### Optuna tuning (LightGBM uchun)

```python
import optuna
import lightgbm as lgb

def objective(trial):
    params = {
        "objective": "binary",
        "metric": "auc",
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 15, 256),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10, log=True),
        "n_estimators": 2000,
        "random_state": 42,
        "n_jobs": -1,
        "verbose": -1,
    }
    
    model = lgb.LGBMClassifier(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(50, verbose=False)],
    )
    
    return roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100, show_progress_bar=True)

print(f"Best params: {study.best_params}")
print(f"Best AUC: {study.best_value:.4f}")
```

### SHAP — Model interpretation

```python
import shap

# Tree-based modellar uchun TreeExplainer (tez)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Global importance
shap.summary_plot(shap_values, X_test, plot_type="bar")
shap.summary_plot(shap_values, X_test)  # beeswarm plot

# Local explanation (bitta prediction uchun)
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### Stacking — Multiple models birlashtirish

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

estimators = [
    ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
    ("xgb", xgb.XGBClassifier(n_estimators=200, random_state=42)),
    ("lgb", lgb.LGBMClassifier(n_estimators=200, random_state=42, verbose=-1)),
]

stack = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(),
    cv=5,
    n_jobs=-1,
)

stack.fit(X_train, y_train)
```

## 🔌 Backend integratsiyasi

### XGBoost FastAPI serving

```python
from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np

app = FastAPI()
model = xgb.XGBClassifier()
model.load_model("models/xgb_v1.json")  # XGBoost native format (tezroq)

class Features(BaseModel):
    feature_vector: list[float]

@app.post("/predict")
def predict(input_data: Features):
    X = np.array([input_data.feature_vector])
    proba = float(model.predict_proba(X)[0, 1])
    return {
        "prediction": int(proba > 0.5),
        "probability": proba,
    }
```

### ONNX export — Cross-platform

```python
# LightGBM/XGBoost → ONNX → har joyda ishlaydi (C++, Java, Go, .NET)
from onnxmltools import convert_lightgbm
from skl2onnx.common.data_types import FloatTensorType

initial_types = [("input", FloatTensorType([None, X_train.shape[1]]))]
onnx_model = convert_lightgbm(model, initial_types=initial_types)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Serving (ONNX Runtime)
import onnxruntime as ort
session = ort.InferenceSession("model.onnx")
predictions = session.run(None, {"input": X_test.astype("float32")})[0]
```

### Batch prediction with Celery

```python
from celery import Celery

celery_app = Celery("ml_tasks", broker="redis://localhost:6379")

@celery_app.task
def batch_predict(file_path: str):
    df = pd.read_csv(file_path)
    model = joblib.load("model.joblib")
    
    predictions = model.predict_proba(df)[:, 1]
    df["churn_probability"] = predictions
    df["risk_segment"] = pd.cut(predictions, bins=[0, 0.3, 0.7, 1.0],
                                 labels=["low", "medium", "high"])
    
    output_path = file_path.replace(".csv", "_predictions.csv")
    df.to_csv(output_path, index=False)
    
    return {"file": output_path, "n_predictions": len(df)}
```

## 📚 Resurslar

- **XGBoost docs** — [xgboost.readthedocs.io](https://xgboost.readthedocs.io/)
- **LightGBM docs** — [lightgbm.readthedocs.io](https://lightgbm.readthedocs.io/)
- **CatBoost docs** — [catboost.ai](https://catboost.ai/)
- **"XGBoost: A Scalable Tree Boosting System"** — Chen & Guestrin (paper)
- **SHAP docs** — [shap.readthedocs.io](https://shap.readthedocs.io/)
- **Kaggle Learn — Intermediate ML** (XGBoost'ga bag'ishlangan)
- **"Effective XGBoost"** — Matt Harrison (kitob)

## 🏋️ Mashqlar

### 🟢 Easy
1. RandomForest va LogisticRegression solishtiring (Titanic).
2. XGBoost'da `n_estimators` ni 100, 500, 1000 qilib solishtiring.
3. Feature importance'ni 3 ta turli modeldan oling.

### 🟡 Medium
1. **3-way comparison**: bir xil datasetda XGBoost, LightGBM, CatBoost — accuracy + training time solishtiring.
2. **Optuna**: LightGBM uchun 100 ta trial bilan tuning, default vs tuned solishtiring.
3. **SHAP**: o'rgatgan modelingiz uchun SHAP summary plot, top 10 feature.

### 🔴 Hard
1. **Stacking ensemble**: 5+ ta base model + meta-learner. Kaggle'ga submit qiling.
2. **ONNX serving**: XGBoost'ni ONNX'ga export, Go yoki Node.js'da serving (chuqurroq backend integration).
3. **Custom objective**: business-aware objective function yozing (masalan, asimmetric loss: FN $50, FP $10).

## 🚀 Capstone — Kaggle Competition

`notebooks/month-02/06_kaggle_competition.ipynb`:
- **Kaggle — Titanic** yoki **Spaceship Titanic**
- To'liq pipeline: EDA → FE → 3+ model → ensemble → submission
- Maqsad: top 30% (Titanic'da ~0.80 accuracy, Spaceship Titanic'da ~0.81)
- Notebook'ni Kaggle'ga ham yuklang (publik notebook)
- GitHub'ga commit, README'da `Kaggle Profile` link

## ✅ Tekshirish ro'yxati

- [ ] Bagging va Boosting farqini bilaman
- [ ] Random Forest, XGBoost, LightGBM ni qachon ishlatishni bilaman
- [ ] Early stopping bilan ishlay olaman
- [ ] Optuna bilan hyperparameter tuning qilaman
- [ ] CatBoost categorical handling afzalligini bilaman
- [ ] SHAP bilan modelni interpret qila olaman
- [ ] ONNX'ga export va loading bilan tanishman
- [ ] Kaggle competition'da submit qildim (top 30%)

🎉 **Oy 2 tugadi!** [Mashqlar](./exercises.md) ni ko'rib chiqing va [Oy 3 — Deep Learning](../month-03-deep-learning/README.md) ga o'ting.
