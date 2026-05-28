# Classification

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Classification masalasini regression'dan ajrata olasiz
- Logistic Regression, KNN, SVM, Decision Tree algoritmlarini bilasiz
- Imbalanced data muammosini taniysiz va yechimlarini bilasiz
- Confusion matrix, Precision, Recall, F1, ROC-AUC ni to'g'ri talqin qilasiz
- Binary va multi-class classification farqini tushunasiz

## 📖 Nimani o'rganish kerak

- **Logistic Regression** — nomi "regression" lekin classification uchun
- **K-Nearest Neighbors (KNN)** — lazy learning
- **Support Vector Machines (SVM)** — kernel trick
- **Decision Trees** — qoidalar daraxti
- **Naive Bayes** — text classification uchun klassik
- **Imbalanced classes** — SMOTE, class_weight, undersampling
- **Multi-class strategies** — OvR (One-vs-Rest), OvO (One-vs-One)
- **Probability calibration** — `predict_proba` ishonchli bo'lishi uchun
- **Threshold tuning** — `0.5` har doim eng yaxshi emas

## 📦 Kutubxonalar

```bash
pip install scikit-learn imbalanced-learn
```

- **scikit-learn** — asosiy modellar
- **imbalanced-learn** — SMOTE va boshqa imbalance strategiyalari

## 🧠 Muhim mavzular

### Algoritm tanlash hujjati

| Algoritm | Tezligi | Interpretability | Imbalanced'ga bardosh | Qachon ishlatish |
|----------|---------|------------------|---------------------|------------------|
| **Logistic Regression** | ⚡⚡⚡ | ⭐⭐⭐ | O'rta | Baseline, lineer feature'lar |
| **KNN** | 🐌 | ⭐⭐ | Past | Kichik dataset, intuition |
| **SVM (linear)** | ⚡⚡ | ⭐⭐ | Yaxshi (class_weight) | O'rta dataset |
| **SVM (RBF)** | 🐌 | ⭐ | Yaxshi | Murakkab pattern, kichik dataset |
| **Decision Tree** | ⚡⚡⚡ | ⭐⭐⭐⭐ | Yaxshi | Boshlash uchun, interpretability |
| **Naive Bayes** | ⚡⚡⚡ | ⭐⭐⭐ | O'rta | Text classification, baseline |

### Logistic Regression — qanday ishlaydi?

1. Linear kombinatsiya: `z = w₀ + w₁x₁ + ... + wₙxₙ`
2. Sigmoid funksiya: `p = 1 / (1 + e^(-z))` → natija (0, 1) oralig'ida
3. Threshold: `p > 0.5` bo'lsa class 1, aks holda class 0

```
sigmoid(z):
   1 |        ___________
     |       /
   0.5|------/
     |     /
   0 |____/_____________
       -∞    0    +∞
```

### Confusion Matrix

```
                 Predicted
                  0     1
Actual    0     [TN]  [FP]
          1     [FN]  [TP]
```

- **TP (True Positive):** to'g'ri ravishda 1 deb topgan
- **TN (True Negative):** to'g'ri ravishda 0 deb topgan
- **FP (False Positive):** noto'g'ri ravishda 1 dedik (Type I error)
- **FN (False Negative):** noto'g'ri ravishda 0 dedik (Type II error)

### Metrik'lar — qaysi qachon?

| Metrik | Formula | Qachon muhim |
|--------|---------|--------------|
| **Accuracy** | `(TP+TN)/N` | Class'lar balansli bo'lganda |
| **Precision** | `TP/(TP+FP)` | False Positive xavfli (spam → siz muhim email'ni yo'qotmaysiz) |
| **Recall** | `TP/(TP+FN)` | False Negative xavfli (kasallik aniqlash — kasalni qoldirmaslik) |
| **F1** | `2*P*R/(P+R)` | P va R muvozanati |
| **ROC-AUC** | curve area | Threshold-independent, balansli baholash |
| **PR-AUC** | precision-recall area | Imbalanced data uchun yaxshiroq |

### Real misol — Precision vs Recall tradeoff

**Cancer detection** modeli:
- Recall = 99% → kasallarning 99% topiladi
- Precision = 60% → "kasal" deb topilganlarning 60% haqiqatdan kasal
- Bu **maqbul** — kasalni qoldirmaslik muhimroq

**Spam filter**:
- Precision = 99% → spam deb topilganlar 99% haqiqatdan spam
- Recall = 80% → 20% spam o'tib ketadi
- Bu **maqbul** — muhim email'ni yo'qotmaslik kerak

### Imbalanced data muammosi

Agar 95% data — class 0, 5% — class 1, model **doim 0** bashorat qilsa **95% accuracy**! Lekin bu **foydasiz**.

**Yechimlar:**
1. **`class_weight='balanced'`** (sklearn modellarda)
2. **SMOTE** — sintetik minority samples yaratish (imbalanced-learn)
3. **Undersampling** — majority class'dan ba'zilarni olib tashlash
4. **Stratified sampling** — train/test split'da nisbat saqlanadi
5. **Threshold tuning** — 0.5 dan past threshold (recall oshadi)
6. **Boshqa metrik** — accuracy o'rniga F1, PR-AUC

## 💻 Kod misollari

### Logistic Regression — Breast Cancer

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)

# 1. Data
data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target  # 0 = malignant, 1 = benign

# 2. Split (stratify MUHIM!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, random_state=42)),
])
pipe.fit(X_train, y_train)

# 4. Evaluation
y_pred = pipe.predict(X_test)
y_proba = pipe.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=["malignant", "benign"]))
print(f"\nROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
```

### Imbalanced data + class_weight

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

# Sun'iy imbalanced data
from sklearn.datasets import make_classification
X, y = make_classification(
    n_samples=10_000, n_features=20, n_informative=10,
    weights=[0.95, 0.05], random_state=42,
)
# 95% class 0, 5% class 1

# Variant 1: default (accuracy = yuqori, recall = past)
m1 = LogisticRegression(max_iter=1000).fit(X, y)

# Variant 2: class_weight balanced
m2 = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X, y)

# Variant 3: manual weights
m3 = LogisticRegression(max_iter=1000, class_weight={0: 1, 1: 19}).fit(X, y)
```

### SMOTE bilan oversampling

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# imblearn Pipeline (sklearn Pipeline ichida SMOTE ishlamaydi!)
pipe = ImbPipeline([
    ("scaler", StandardScaler()),
    ("smote", SMOTE(random_state=42)),
    ("clf", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)
```

### Threshold tuning

```python
import numpy as np

y_proba = pipe.predict_proba(X_test)[:, 1]

# Default threshold 0.5
y_pred_default = (y_proba >= 0.5).astype(int)

# Custom threshold for higher recall
y_pred_recall = (y_proba >= 0.3).astype(int)

# Optimal threshold (F1 maximizing)
from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * precisions * recalls / (precisions + recalls + 1e-9)
best_threshold = thresholds[np.argmax(f1_scores)]
print(f"Best threshold for F1: {best_threshold:.3f}")
```

### Multi-class classification

```python
from sklearn.datasets import load_digits
from sklearn.svm import SVC

X, y = load_digits(return_X_y=True)  # 10 classes (0..9)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="rbf", probability=True, random_state=42)),
])
pipe.fit(X_train, y_train)

# Multi-class metric
from sklearn.metrics import classification_report
print(classification_report(y_test, pipe.predict(X_test)))
```

## 🔌 Backend integratsiyasi

### Churn prediction API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(title="Customer Churn Predictor")
model = joblib.load("models/churn_v1.joblib")

class CustomerFeatures(BaseModel):
    tenure_months: int = Field(..., ge=0)
    monthly_charges: float = Field(..., gt=0)
    total_charges: float = Field(..., ge=0)
    contract_type: int = Field(..., ge=0, le=2)  # 0=monthly, 1=1yr, 2=2yr
    has_internet: bool
    payment_method: int = Field(..., ge=0, le=3)

class ChurnPrediction(BaseModel):
    will_churn: bool
    churn_probability: float
    risk_level: str  # low / medium / high
    recommended_action: str

@app.post("/predict/churn", response_model=ChurnPrediction)
def predict_churn(customer: CustomerFeatures):
    X = np.array([list(customer.dict().values())])
    proba = float(model.predict_proba(X)[0, 1])
    
    # Custom business threshold
    if proba > 0.7:
        risk, action = "high", "immediate_retention_call"
    elif proba > 0.4:
        risk, action = "medium", "send_discount_offer"
    else:
        risk, action = "low", "monitor"
    
    return ChurnPrediction(
        will_churn=proba > 0.5,
        churn_probability=proba,
        risk_level=risk,
        recommended_action=action,
    )
```

### Batch prediction endpoint

```python
class BatchInput(BaseModel):
    customers: list[CustomerFeatures]

@app.post("/predict/churn/batch")
def predict_batch(payload: BatchInput):
    X = np.array([list(c.dict().values()) for c in payload.customers])
    probas = model.predict_proba(X)[:, 1]
    return {
        "predictions": [
            {"index": i, "churn_proba": float(p), "will_churn": bool(p > 0.5)}
            for i, p in enumerate(probas)
        ],
        "summary": {
            "total": len(probas),
            "at_risk": int((probas > 0.5).sum()),
            "high_risk": int((probas > 0.7).sum()),
        },
    }
```

## 📚 Resurslar

- **Scikit-learn Classification** — [scikit-learn.org/stable/supervised_learning.html](https://scikit-learn.org/stable/supervised_learning.html)
- **StatQuest — Logistic Regression** (YouTube playlist)
- **Imbalanced-learn docs** — [imbalanced-learn.org](https://imbalanced-learn.org/)
- **Andrew Ng — Course 2: Advanced Learning Algorithms**
- **Maqola:** "Beyond Accuracy: Precision and Recall" — Towards Data Science

## 🏋️ Mashqlar

### 🟢 Easy
1. `load_iris()` da 4 ta classifier'ni (LogReg, KNN, SVM, Tree) solishtiring.
2. Breast cancer datasetda Confusion Matrix chizing (`ConfusionMatrixDisplay`).
3. KNN'da `k` ni `[1, 3, 5, 10, 50]` qiymatlar bilan sinang.

### 🟡 Medium
1. **Imbalanced demo**: `make_classification` bilan 95/5 imbalanced data yarating. Default vs `class_weight='balanced'` vs SMOTE — har birining precision/recall'ini solishtiring.
2. **ROC curve**: 3 ta modelning ROC curve'larini bitta chart'da chizing.
3. **Threshold tuning**: Telco Churn datasetda F1-maximizing threshold'ni toping.

### 🔴 Hard
1. **Production churn service**: Docker + FastAPI + Postgres'da to'liq churn prediction servis. `/predict`, `/feedback` (real natija qaytarish uchun), `/metrics` (Prometheus) endpoint'lar.
2. **Online learning**: `SGDClassifier` ishlatib, har yangi feedback'da modelni partial_fit qiling — drift'ga moslashish.

## 🚀 Capstone

`notebooks/month-02/02_classification_models.ipynb`:
- **Kaggle — Telco Customer Churn**
- EDA → preprocessing → 5 ta classifier solishtirish
- Class imbalance bilan ishlash
- ROC, PR curve chizish
- Eng yaxshi modelni Docker'da deploy

## ✅ Tekshirish ro'yxati

- [ ] Classification va Regression farqini bilaman
- [ ] Confusion Matrix'ni o'qiy olaman
- [ ] Precision, Recall, F1 ni biznesga tushuntira olaman
- [ ] ROC-AUC va PR-AUC farqini bilaman
- [ ] Imbalanced data uchun 3 ta strategiya bilaman
- [ ] `predict_proba` ni `predict`'dan ajrata olaman
- [ ] Custom threshold bilan natijani moslashtira olaman
- [ ] FastAPI'da classification model serve qildim

[Clustering](./04-clustering.md) ga o'tamiz.
