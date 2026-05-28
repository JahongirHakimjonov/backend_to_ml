# Model Evaluation

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Modelni baholashning to'g'ri usullarini bilasiz
- Cross-validation strategiyalarini (KFold, Stratified, TimeSeriesSplit) qo'llay olasiz
- Confusion matrix, ROC, PR curve, learning curves chiza olasiz
- Hyperparameter tuning (Grid, Random, Bayesian search) qila olasiz
- Bias-variance tradeoff'ni amaliyotda ko'ra olasiz

## Nimani o'rganish kerak

- **Train/Validation/Test methodology**
- **Cross-validation strategiyalari**: KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit
- **Classification metrics**: accuracy, precision, recall, F1, ROC-AUC, PR-AUC, log loss
- **Regression metrics**: MSE, RMSE, MAE, R², MAPE, Huber loss
- **Learning curves** — bias vs variance vizual
- **Validation curves** — bitta hyperparameter ta'siri
- **Hyperparameter tuning**: GridSearchCV, RandomizedSearchCV, Optuna
- **Calibration** — probability'lar to'g'rimi (Platt, Isotonic)

## Kutubxonalar

```bash
pip install scikit-learn yellowbrick optuna
```

## Muhim mavzular

### Cross-validation strategiyalari

```
KFold (standart)
[1][2][3][4][5]  → Test=[1], Train=[2,3,4,5]
[1][2][3][4][5]  → Test=[2], Train=[1,3,4,5]
...
Mos: balansli classification, regression

StratifiedKFold
Har fold'da class nisbati saqlanadi
Mos: imbalanced classification (default Sklearn'da)

GroupKFold
Bir guruh (masalan, bir user'ning barcha record'lari) faqat bir fold'da
Mos: data leakage'ni oldini olish

TimeSeriesSplit
Train doim test'dan oldin
[1][2][3][4][5]
Train=[1],     Test=[2]
Train=[1,2],   Test=[3]
Train=[1,2,3], Test=[4]
Mos: time series
```

### Hyperparameter tuning yondashuvlari

| Yondashuv | Tezligi | Sifat | Qachon |
|-----------|---------|-------|--------|
| **GridSearchCV** | Sekin | ⭐⭐⭐⭐ | Kam parametr (2-3 ta) |
| **RandomizedSearchCV** | Tez | ⭐⭐⭐ | Ko'p parametr, mas'uliyatlimas qidiruv |
| **Optuna (Bayesian)** | Juda tez | ⭐⭐⭐⭐⭐ | Production, smart qidiruv |
| **HalvingGridSearch** | Juda tez | ⭐⭐⭐ | Successive halving |

### Learning Curves — bias vs variance

```
Training error vs Validation error (training set size'ga qarab):

High bias (underfit):
Training error   ────────────── (yuqori)
Validation error ──────────────
                  Train size

High variance (overfit):
Validation error \              
                  \             
Training error    \____________ (juda past)
                  ─────────────
                   Train size
                   
Just right:
Validation error ──────────────
Training error   ──────────────
(ikkalasi yaqin va past)
```

### Calibration nima va nima uchun kerak?

Default `predict_proba` chiqaradigan ehtimollik **to'g'ri kalibrlanmagan**bo'lishi mumkin:
- Model `0.8` chiqaradi, lekin haqiqatda **70%**to'g'ri
- Bu — biznes qarorlari uchun muhim (masalan, "70% > 0.6 threshold")

**Yechim:**`CalibratedClassifierCV` — Platt scaling yoki Isotonic regression.

## Kod misollari

### Cross-validation comprehensive

```python
from sklearn.model_selection import (
    cross_validate, KFold, StratifiedKFold, 
    TimeSeriesSplit, cross_val_score,
)
from sklearn.linear_model import LogisticRegression

# Multiple metrics
scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = cross_validate(
    LogisticRegression(max_iter=1000),
    X, y, cv=cv, scoring=scoring, return_train_score=True,
)

for metric in scoring:
    test_scores = results[f"test_{metric}"]
    train_scores = results[f"train_{metric}"]
    print(f"{metric:12s}  Train: {train_scores.mean():.3f}±{train_scores.std():.3f}  "
          f"Test: {test_scores.mean():.3f}±{test_scores.std():.3f}")
```

### Time Series CV

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5, test_size=30)  # 30 days test

for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Fold {fold}: Train size={len(train_idx)}, Test size={len(test_idx)}, "
          f"Score={score:.3f}")
```

### GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [None, 10, 20, 50],
    "min_samples_split": [2, 5, 10],
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1,  # barcha CPU'lardan foydalanish
    verbose=2,
)
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV F1: {grid.best_score_:.3f}")
print(f"Test F1: {grid.score(X_test, y_test):.3f}")
```

### Optuna — Bayesian Optimization

```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
        "max_depth": trial.suggest_int("max_depth", 3, 30),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
    }
    model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring="f1").mean()
    return score

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50, show_progress_bar=True)

print(f"Best params: {study.best_params}")
print(f"Best score: {study.best_value:.3f}")
```

### Learning curve

```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

train_sizes, train_scores, val_scores = learning_curve(
    LogisticRegression(max_iter=1000),
    X, y, cv=5, scoring="accuracy",
    train_sizes=np.linspace(0.1, 1.0, 10),
    n_jobs=-1,
)

train_mean = train_scores.mean(axis=1)
val_mean = val_scores.mean(axis=1)

plt.plot(train_sizes, train_mean, "o-", label="Train")
plt.plot(train_sizes, val_mean, "o-", label="Validation")
plt.xlabel("Training set size")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Learning Curve")
plt.show()

# Interpretatsiya:
# - Train va Val yaqin va past → underfit (model murakkabroq kerak)
# - Train yuqori, Val past, gap katta → overfit
# - Ikkalasi yuqori va yaqin → 
```

### Calibration

```python
from sklearn.calibration import CalibratedClassifierCV, calibration_curve

# Asosiy model
clf = SVC(probability=True)

# Calibrated wrapper
calibrated = CalibratedClassifierCV(clf, method="sigmoid", cv=5)
calibrated.fit(X_train, y_train)

# Reliability diagram
proba = calibrated.predict_proba(X_test)[:, 1]
prob_true, prob_pred = calibration_curve(y_test, proba, n_bins=10)

plt.plot(prob_pred, prob_true, "o-", label="Calibrated")
plt.plot([0, 1], [0, 1], "k--", label="Perfectly calibrated")
plt.xlabel("Predicted probability")
plt.ylabel("True probability")
plt.legend()
plt.show()
```

### Custom metric

```python
from sklearn.metrics import make_scorer

def custom_business_score(y_true, y_pred):
    """Biznes uchun: TP=$100 daromad, FP=$10 zarar, FN=$50 missed."""
    tp = ((y_true == 1) & (y_pred == 1)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    return 100 * tp - 10 * fp - 50 * fn

scorer = make_scorer(custom_business_score, greater_is_better=True)
scores = cross_val_score(model, X, y, cv=5, scoring=scorer)
```

## Backend integratsiyasi

### Model validation endpoint

```python
from fastapi import FastAPI, UploadFile
from sklearn.metrics import classification_report
import pandas as pd

app = FastAPI()

@app.post("/validate/")
async def validate_model(test_csv: UploadFile, model_version: str = "v1"):
    """Yangi modelni production'a chiqarishdan oldin test."""
    df = pd.read_csv(test_csv.file)
    X_test = df.drop("target", axis=1)
    y_test = df["target"]
    
    model = joblib.load(f"models/{model_version}.joblib")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Threshold: yangi versiya prod'dan yaxshi bo'lishi kerak
    PROD_F1 = 0.85
    can_deploy = report["1"]["f1-score"] >= PROD_F1
    
    return {
        "model_version": model_version,
        "metrics": report,
        "auc": roc_auc_score(y_test, y_proba),
        "can_deploy": can_deploy,
        "message": "OK" if can_deploy else f"F1 ({report['1']['f1-score']:.3f}) < threshold ({PROD_F1})",
    }
```

### MLflow integration (preview)

```python
# Bu Oy 6'da chuqurroq, lekin boshlash uchun:
import mlflow

with mlflow.start_run():
    mlflow.log_params({"n_estimators": 100, "max_depth": 10})
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    score = cross_val_score(model, X_train, y_train, cv=5).mean()
    mlflow.log_metric("cv_accuracy", score)
    
    mlflow.sklearn.log_model(model, "model")
```

## Resurslar

- **Scikit-learn Model Evaluation** — [scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html)
- **Optuna docs** — [optuna.org](https://optuna.org/)
- **"Evaluating Machine Learning Models"** — Alice Zheng (O'Reilly)
- **Yellowbrick** — vizual diagnostika: [scikit-yb.org](https://www.scikit-yb.org/)
- **Andrew Ng — "Machine Learning Yearning"**(bepul) — practical tips

## 🏋️ Mashqlar

### 🟢 Easy
1. KFold va StratifiedKFold ni imbalanced datasetda solishtiring — fold'larda class nisbati farq qiladimi?
2. Bitta hyperparameter (`C` Logistic Regression'da) bo'yicha `validation_curve` chizing.
3. `GridSearchCV` natijasini `pd.DataFrame(grid.cv_results_)` ga aylantirib analiz qiling.

### 🟡 Medium
1. **TimeSeriesSplit demo**: sun'iy time series data yarating, KFold va TimeSeriesSplit natijalarini solishtiring.
2. **Optuna vs GridSearch**: bir xil parameter space'da ikkalasini solishtiring (vaqt + sifat).
3. **Calibration**: oddiy `LogisticRegression` natijasi va `CalibratedClassifierCV` natijasini `calibration_curve` bilan vizualizatsiya qiling.

### 🔴 Hard
1. **A/B test backend**: ikki modelni serve qiladigan FastAPI. Har request uchun random model tanlash, natijani DB'ga yozish, oxirida statistik test (scipy.stats.chi2_contingency) bilan qaysi yaxshiroq ekanini aniqlash.
2. **Custom CV strategy**: imbalanced + temporal data uchun custom CV class yarating (sklearn `BaseCrossValidator` dan inherit qiluvchi).

## Capstone

`notebooks/month-02/05_model_evaluation.ipynb`:
- Telco Churn datasetda 5 ta turli model
- Har birini `cross_validate` bilan baholash (5 metric)
- Hyperparameter tuning (Optuna)
- Learning curves har bir model uchun
- Calibration check
- Biznes uchun custom metric (revenue impact)

## ✅ Tekshirish ro'yxati

- [ ] Cross-validation strategiyalari farqini bilaman
- [ ] Imbalanced data uchun StratifiedKFold ishlataman
- [ ] Time series uchun TimeSeriesSplit ishlataman
- [ ] Classification va regression metric'larini to'g'ri tanlayman
- [ ] GridSearchCV va RandomizedSearchCV ishlataman
- [ ] Optuna bilan Bayesian optimization qila olaman
- [ ] Learning curves chizib bias/variance'ni interpret qilaman
- [ ] Model calibration nima ekanini bilaman

[Ensemble Methods](./07-ensemble-methods.md) ga o'tamiz — Klassik ML'ning eng kuchli qismiga.
