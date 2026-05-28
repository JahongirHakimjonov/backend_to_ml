# Model Monitoring

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- ML model monitoring DevOps monitoring'dan qanday farq qilishini bilasiz
- Data drift va Concept drift'ni aniqlay olasiz
- Evidently AI bilan production monitoring qurishasiz
- Business KPI'larni model performance bilan bog'lay olasiz
- Alerts va retraining trigger'lar yarata olasiz

## 📖 Nimani o'rganish kerak

- **3 darajadagi monitoring** — infrastructure, model, business
- **Data drift** — feature distribution o'zgarishi
- **Concept drift** — input → output relationship o'zgarishi
- **Prediction drift** — output distribution o'zgarishi
- **Performance metrics** — accuracy/loss vaqt o'tishi bilan
- **Evidently AI** — open source monitoring
- **WhyLabs, Arize** — managed alternatives
- **Prometheus + Grafana** — infrastructure
- **Alerts va retraining triggers**

## 🧠 ML monitoring nima uchun maxsus?

### DevOps monitoring (backend dev'lar biladi)
- Server CPU/RAM
- Request latency
- Error rate
- Throughput

### ML monitoring qo'shimcha
- **Input data quality** — schema, missing, range
- **Feature distribution** — drift!
- **Prediction distribution** — drift!
- **Performance vaqt o'tishi bilan** — accuracy/loss
- **Business KPI** — revenue impact, user satisfaction

### Misol — drift muammosi

```
Day 1 (training):  age distribution = N(35, 10)
Day 30 (prod):     age distribution = N(45, 12)  ← drift!

Model accuracy:
- Day 1:   92%
- Day 30:  75%  ← muammo!

Aniqlash: feature drift early warning
Yechim:   yangi data bilan retraining
```

## 🧠 Drift turlari

### 1. Data drift (Covariate shift)
Input distribution o'zgaradi (P(X) o'zgaradi).
- Misol: yangi xil mijozlar paydo bo'ldi (yoshroq, boshqa region)

### 2. Concept drift
Input ↔ Output relationship o'zgaradi (P(Y|X) o'zgaradi).
- Misol: bir xil features lekin javob boshqa (COVID kabi external event)

### 3. Prediction drift
Model output distribution o'zgaradi (P(Ŷ) o'zgaradi).
- Misol: 1% spam → 5% spam predict qilmoqda

### 4. Label drift (training set'da)
Ground truth distribution o'zgaradi.

## 💻 Kod misollari

### Evidently AI — quick start

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently import ColumnMapping
import pandas as pd

# Reference (training) va Current (production) data
reference = pd.read_csv("data/training_data.csv")
current = pd.read_csv("data/production_data_last_week.csv")

# Column mapping
column_mapping = ColumnMapping(
    target="churned",
    prediction="prediction",
    numerical_features=["age", "income", "tenure_months"],
    categorical_features=["plan_type", "country"],
)

# Run data drift report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)

# Save report
report.save_html("reports/data_drift.html")

# Programmatic access
result = report.as_dict()
print(result["metrics"][0]["result"]["dataset_drift"])  # True/False
```

### Classification monitoring

```python
from evidently.metric_preset import ClassificationPreset

report = Report(metrics=[ClassificationPreset()])
report.run(
    reference_data=reference,    # baseline (training)
    current_data=current,         # production
    column_mapping=column_mapping,
)

# Output: accuracy, precision, recall, ROC, etc.
# Reference vs Current comparison
report.save_html("classification_report.html")
```

### Real-time monitoring (production stream)

```python
from evidently.test_suite import TestSuite
from evidently.tests import (
    TestNumberOfColumnsWithMissingValues,
    TestNumberOfRowsWithMissingValues,
    TestNumberOfConstantColumns,
    TestNumberOfDuplicatedRows,
    TestColumnsType,
)

# Daily test suite
test_suite = TestSuite(tests=[
    TestNumberOfColumnsWithMissingValues(),
    TestNumberOfRowsWithMissingValues(),
    TestNumberOfConstantColumns(),
    TestNumberOfDuplicatedRows(),
    TestColumnsType(),
])

test_suite.run(reference_data=reference, current_data=daily_batch)

if not test_suite.as_dict()["summary"]["all_passed"]:
    send_alert(test_suite.as_dict())
```

### Custom drift detection

```python
from scipy import stats
import numpy as np

def detect_drift_ks(reference: np.ndarray, current: np.ndarray, alpha: float = 0.05) -> dict:
    """Kolmogorov-Smirnov test for distribution drift."""
    ks_stat, p_value = stats.ks_2samp(reference, current)
    return {
        "ks_statistic": float(ks_stat),
        "p_value": float(p_value),
        "drift_detected": p_value < alpha,
    }

def detect_drift_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index (industry standard)."""
    breakpoints = np.linspace(reference.min(), reference.max(), bins + 1)
    
    ref_counts = np.histogram(reference, breakpoints)[0]
    cur_counts = np.histogram(current, breakpoints)[0]
    
    ref_pct = ref_counts / ref_counts.sum() + 1e-6
    cur_pct = cur_counts / cur_counts.sum() + 1e-6
    
    psi = ((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)).sum()
    
    # Interpretation:
    # PSI < 0.1   — no significant change
    # PSI 0.1-0.2 — moderate change
    # PSI > 0.2   — significant change
    
    return float(psi)

# Per-feature drift report
def feature_drift_report(reference_df, current_df, features):
    report = {}
    for feature in features:
        ref_values = reference_df[feature].dropna().values
        cur_values = current_df[feature].dropna().values
        
        report[feature] = {
            **detect_drift_ks(ref_values, cur_values),
            "psi": detect_drift_psi(ref_values, cur_values),
        }
    return report
```

### Prometheus metrics — production

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Counters
prediction_count = Counter(
    "ml_predictions_total",
    "Total predictions",
    ["model_version", "prediction_class"],
)

# Histograms (distribution)
prediction_latency = Histogram(
    "ml_prediction_latency_seconds",
    "Prediction latency",
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
)

# Gauges (current state)
model_accuracy = Gauge(
    "ml_model_accuracy",
    "Current model accuracy (rolling 1h)",
    ["model_version"],
)

drift_score = Gauge(
    "ml_feature_drift_psi",
    "PSI drift score per feature",
    ["feature"],
)

# Usage
@app.post("/predict")
async def predict(features: Features):
    start = time.perf_counter()
    
    pred = model.predict(features)
    
    prediction_latency.observe(time.perf_counter() - start)
    prediction_count.labels(
        model_version="v1.2",
        prediction_class=str(pred),
    ).inc()
    
    return {"prediction": int(pred)}

# Background job — update gauges
@app.on_event("startup")
async def schedule_drift_check():
    asyncio.create_task(periodic_drift_check())

async def periodic_drift_check():
    while True:
        await asyncio.sleep(3600)  # har soatda
        
        recent = await fetch_recent_predictions(hours=1)
        psi_scores = feature_drift_report(reference_data, recent, features)
        
        for feature, scores in psi_scores.items():
            drift_score.labels(feature=feature).set(scores["psi"])
            
            if scores["psi"] > 0.2:
                await send_alert(f"High drift on {feature}: PSI={scores['psi']:.3f}")
```

### Grafana dashboard JSON (snippet)

```json
{
  "panels": [
    {
      "title": "Prediction Latency (p95)",
      "type": "graph",
      "targets": [{
        "expr": "histogram_quantile(0.95, rate(ml_prediction_latency_seconds_bucket[5m]))",
      }]
    },
    {
      "title": "Predictions per second",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(ml_predictions_total[1m]))",
      }]
    },
    {
      "title": "Feature Drift (PSI)",
      "type": "heatmap",
      "targets": [{
        "expr": "ml_feature_drift_psi",
      }]
    },
    {
      "title": "Model Accuracy",
      "type": "graph",
      "targets": [{
        "expr": "ml_model_accuracy",
      }]
    }
  ]
}
```

### Alerts (Prometheus AlertManager)

```yaml
# alerts.yml
groups:
- name: ml_alerts
  interval: 30s
  rules:
  
  - alert: HighDriftDetected
    expr: ml_feature_drift_psi > 0.2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Feature drift detected on {{ $labels.feature }}"
      description: "PSI = {{ $value }}"
  
  - alert: ModelAccuracyDrop
    expr: ml_model_accuracy < 0.80
    for: 30m
    labels:
      severity: critical
    annotations:
      summary: "Model accuracy below 80%"
      action: "Consider retraining"
  
  - alert: HighLatency
    expr: histogram_quantile(0.95, rate(ml_prediction_latency_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
```

### Auto-retraining trigger

```python
async def check_and_retrain():
    """Drift detected'da avtomatik retraining trigger."""
    
    recent_data = await fetch_recent_predictions(days=7)
    drift = feature_drift_report(reference_data, recent_data, features)
    
    critical_drift = [f for f, s in drift.items() if s["psi"] > 0.2]
    
    if len(critical_drift) >= 3:  # 3+ feature drift bo'lsa
        # Trigger retraining DAG
        await trigger_airflow_dag("retrain_pipeline", config={
            "reason": "drift_detected",
            "drifted_features": critical_drift,
        })
        
        # Notify
        await send_slack_message(
            f"🚨 Retraining triggered due to drift on: {critical_drift}"
        )
```

## 🔌 Backend integratsiyasi

### Prediction logging

```python
# Postgres'da har prediction'ni log qilish
async def log_prediction(features: dict, prediction, model_version: str):
    await db.execute("""
        INSERT INTO predictions (timestamp, features, prediction, model_version)
        VALUES ($1, $2, $3, $4)
    """, datetime.utcnow(), json.dumps(features), prediction, model_version)

@app.post("/predict")
async def predict(features: Features, background: BackgroundTasks):
    pred = model.predict(features)
    
    # Background log (response'ni ushlab turmaslik uchun)
    background.add_task(log_prediction, features.dict(), pred, "v1.2")
    
    return {"prediction": pred}

# Feedback endpoint (real outcome'ni qaytarish)
@app.post("/predict/{prediction_id}/feedback")
async def submit_feedback(prediction_id: int, actual: int):
    await db.execute(
        "UPDATE predictions SET actual = $1, feedback_at = NOW() WHERE id = $2",
        actual, prediction_id,
    )
```

### Daily monitoring job

```python
# scheduled via Airflow
def daily_monitoring():
    # 1. Fetch yesterday's predictions + actuals
    df = pd.read_sql("""
        SELECT * FROM predictions
        WHERE timestamp > NOW() - INTERVAL '24 hours'
          AND actual IS NOT NULL
    """, engine)
    
    # 2. Calculate metrics
    accuracy = (df["prediction"] == df["actual"]).mean()
    
    # 3. Compare with reference
    reference = pd.read_csv("reference_data.csv")
    drift_report = feature_drift_report(reference, df, FEATURES)
    
    # 4. Log to MLflow
    with mlflow.start_run(run_name=f"monitoring_{date.today()}"):
        mlflow.log_metric("daily_accuracy", accuracy)
        for f, s in drift_report.items():
            mlflow.log_metric(f"drift_{f}", s["psi"])
    
    # 5. Generate Evidently report
    report = Report(metrics=[DataDriftPreset(), ClassificationPreset()])
    report.run(reference_data=reference, current_data=df, column_mapping=column_mapping)
    report.save_html(f"reports/monitoring_{date.today()}.html")
    
    # 6. Send to S3
    upload_to_s3(f"reports/monitoring_{date.today()}.html")
    
    # 7. Alert if needed
    if accuracy < 0.80:
        send_alert(f"Daily accuracy: {accuracy:.2%}")
```

## 📚 Resurslar

- **Evidently AI docs** — [docs.evidentlyai.com](https://docs.evidentlyai.com/)
- **"Monitoring Machine Learning Models in Production"** — Towards Data Science
- **"A Survey on Concept Drift Adaptation"** — Gama et al.
- **WhyLabs docs** — [docs.whylabs.ai](https://docs.whylabs.ai/)
- **Prometheus best practices** — [prometheus.io/docs/practices](https://prometheus.io/docs/practices/)
- **"Building Machine Learning Pipelines"** — Hapke & Nelson

## 🏋️ Mashqlar

### 🟢 Easy
1. Evidently AI bilan oddiy drift report.
2. PSI calculation manual (numpy).
3. Prometheus metric'larini FastAPI'ga qo'shing.

### 🟡 Medium
1. **Full monitoring setup**: Evidently + Prometheus + Grafana lokal Docker'da.
2. **Drift simulation**: training data'dan distribution biroz o'zgartirib drift'ni kuzating.
3. **Daily monitoring job**: Airflow yoki cron bilan automated reports.

### 🔴 Hard
1. **End-to-end monitoring**: FastAPI + Postgres logs + Prometheus + Evidently + Slack alerts.
2. **Auto-retraining trigger**: drift detected → Airflow DAG trigger.
3. **A/B test analytics**: bir nechta model versiyalarini comparison dashboard.

## 🚀 Capstone

`notebooks/month-06/06_monitoring.ipynb` + `monitoring/`:
- Loyihangizdagi modelni monitoring bilan o'rab oling
- Prediction logging (Postgres)
- Daily Evidently reports
- Grafana dashboard
- Slack alert misol

## ✅ Tekshirish ro'yxati

- [ ] Data drift, concept drift, prediction drift farqi
- [ ] PSI metric'ni bilaman va hisoblay olaman
- [ ] Evidently AI bilan reports
- [ ] Prometheus metric'lar (Counter, Histogram, Gauge)
- [ ] Grafana dashboard
- [ ] AlertManager rules
- [ ] Auto-retraining trigger logic
- [ ] Production monitoring stack

[CI/CD for ML](./07-ci-cd-ml.md) ga o'tamiz.
