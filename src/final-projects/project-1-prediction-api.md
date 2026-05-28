# Loyiha 1: Prediction API

## 🎯 Maqsad

Klassik ML modelni production'a olib chiqadigan to'liq backend servis. Bu loyiha sizning birinchi to'liq portfolio loyihangiz bo'ladi va MLOps'ning asosiy patternlarini ko'rsatadi.

## 📋 Tavsiya etilgan use case'lar (bittasini tanlang)

| Use case | Dataset | Difficulty |
|----------|---------|------------|
| **Customer Churn Prediction** | Telco Customer Churn (Kaggle) | ⭐⭐ |
| **Loan Default Prediction** | LendingClub data | ⭐⭐⭐ |
| **House Price Estimation** | Ames Housing | ⭐⭐ |
| **Insurance Premium** | Kaggle insurance dataset | ⭐⭐ |
| **Employee Attrition** | IBM HR Analytics | ⭐⭐⭐ |
| **O'zbek dataset** | data.gov.uz dataset (extra credit) | ⭐⭐⭐⭐ |

**Maslahat:** Birinchi marta — **Churn** yoki **House Prices**.

## 🏗 Architecture

```
┌─────────────┐      ┌──────────────┐
│  Browser    │─────>│  Streamlit   │
│  Mobile     │      │  Frontend    │
└─────────────┘      └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  FastAPI     │◄─────┐
                     │  Backend     │      │
                     └──────┬───────┘      │
                            │              │
                ┌───────────┼──────────┐   │
                ▼           ▼          ▼   │
        ┌─────────┐  ┌─────────┐  ┌──────────┐
        │ Postgres│  │  Redis  │  │ Sklearn  │
        │ (data)  │  │ (cache) │  │  Model   │
        └─────────┘  └─────────┘  └────┬─────┘
                                       │
                                       ▼
                              ┌──────────────┐
                              │  Prometheus  │
                              │  + Grafana   │
                              └──────────────┘
```

## 📦 Tech Stack

### Required
- **Backend:** FastAPI + Pydantic v2
- **ML:** scikit-learn + XGBoost
- **Database:** PostgreSQL
- **Cache:** Redis
- **Container:** Docker + docker-compose
- **CI/CD:** GitHub Actions

### Nice to have
- **Frontend:** Streamlit (oson) yoki React (zo'r)
- **Tracking:** MLflow
- **Monitoring:** Prometheus + Grafana + Evidently
- **Documentation:** mkdocs

## 📋 Features (must)

### MVP (1-hafta)
- [ ] CSV training pipeline
- [ ] Sklearn model + serialization
- [ ] FastAPI `/predict` endpoint
- [ ] Pydantic input validation
- [ ] Docker container
- [ ] Basic README

### V2 (2-hafta)
- [ ] PostgreSQL — predictions log
- [ ] Redis caching (same input → cached result)
- [ ] Batch prediction endpoint
- [ ] Feedback endpoint (real outcome)
- [ ] Health checks (liveness, readiness)
- [ ] Prometheus metrics
- [ ] Unit + integration tests
- [ ] GitHub Actions CI

### V3 (3-hafta)
- [ ] MLflow integration (Registry'dan model)
- [ ] Streamlit dashboard
- [ ] Drift monitoring (Evidently)
- [ ] A/B test framework (2 model)
- [ ] Cloud deployment (Hetzner / Railway / Render)
- [ ] Blog post
- [ ] Demo video

## 📝 API spec

### `POST /predict`
```json
// Request
{
    "customer_id": "CUST_12345",
    "tenure_months": 24,
    "monthly_charges": 65.50,
    "total_charges": 1572.00,
    "contract_type": "month-to-month",
    "internet_service": true,
    "payment_method": "credit_card"
}

// Response
{
    "prediction_id": "uuid",
    "customer_id": "CUST_12345",
    "churn_prediction": true,
    "churn_probability": 0.78,
    "risk_level": "high",
    "recommended_action": "send_retention_offer",
    "model_version": "v1.2.3",
    "latency_ms": 23.4
}
```

### `POST /predict/batch`
```json
{
    "customers": [
        {"customer_id": "...", "features": {...}},
        // ...
    ]
}
```

### `POST /feedback`
```json
{
    "prediction_id": "uuid",
    "actual_outcome": true,
    "actual_date": "2026-06-15"
}
```

### `GET /model/info`
```json
{
    "model_name": "churn_predictor",
    "version": "v1.2.3",
    "training_date": "2026-05-15",
    "training_metrics": {
        "accuracy": 0.87,
        "f1": 0.82,
        "auc": 0.91
    },
    "features": [...]
}
```

### `GET /metrics` (Prometheus)
```
# HELP ml_predictions_total Total predictions
# TYPE ml_predictions_total counter
ml_predictions_total{model_version="v1.2.3",class="0"} 12453
ml_predictions_total{model_version="v1.2.3",class="1"} 3201
...
```

## 🗂 Project structure

```
prediction-api/
├── README.md
├── ARCHITECTURE.md
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── src/
│   ├── api/
│   │   ├── main.py                 # FastAPI app
│   │   ├── routes/
│   │   │   ├── predict.py
│   │   │   ├── feedback.py
│   │   │   └── health.py
│   │   └── schemas.py              # Pydantic models
│   ├── core/
│   │   ├── config.py               # Settings
│   │   └── logging.py
│   ├── data/
│   │   ├── database.py             # SQLAlchemy
│   │   └── models.py               # ORM models
│   ├── ml/
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── feature_engineering.py
│   │   └── model_registry.py
│   └── monitoring/
│       ├── metrics.py              # Prometheus
│       └── drift.py                # Evidently
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── data/
│   └── raw/data.csv                # DVC tracked
├── models/
│   └── churn_v1.joblib             # MLflow tracked
├── frontend/                       # Streamlit
│   └── app.py
├── monitoring/
│   ├── prometheus.yml
│   └── grafana-dashboards/
├── pyproject.toml
├── requirements.txt
└── Makefile
```

## 🚀 Implementatsiya plani (3 hafta)

### Hafta 1 — MVP
- Day 1-2: Dataset olish, EDA, feature engineering (notebook)
- Day 3-4: Model training, validation (notebook → script)
- Day 5: FastAPI endpoint + Pydantic
- Day 6: Docker + docker-compose
- Day 7: README + GitHub push

### Hafta 2 — Production features
- Day 8-9: PostgreSQL + SQLAlchemy + Alembic migrations
- Day 10: Redis caching
- Day 11: Tests (pytest)
- Day 12: GitHub Actions CI
- Day 13: Prometheus + Grafana
- Day 14: Demo video

### Hafta 3 — Polish + Deploy
- Day 15-16: MLflow integration
- Day 17: Streamlit frontend
- Day 18: Drift monitoring
- Day 19: Cloud deployment
- Day 20: Blog post
- Day 21: LinkedIn post + portfolio update

## 📊 Success metrics

### Texnik
- **Latency p95:** < 100ms
- **Throughput:** > 1000 req/s (load tested)
- **Test coverage:** > 70%
- **Docker image size:** < 500 MB
- **API documentation:** OpenAPI

### Mahsulot
- **Model accuracy:** Industry baseline (Telco: 80%, House: R² > 0.85)
- **Prediction confidence:** Calibrated
- **End-to-end demo:** Working video

## 📚 Resurslar

- **Customer Churn Tutorial** — Towards Data Science
- **FastAPI Best Practices** — [github.com/zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
- **MLflow Quickstart** — official docs
- **Docker for Python** — testdriven.io
- **Streamlit Gallery** — inspiration

## 🏆 Bonus (extra credit)

- Multi-language support
- API rate limiting (slowapi)
- JWT authentication
- WebSocket real-time predictions
- Admin panel
- Cost tracking (predictions $$$)
- Multi-model A/B testing
- Shadow deployment

## ✅ Submission checklist

- [ ] GitHub repo (public, clean history)
- [ ] README (badges, installation, usage)
- [ ] Architecture diagram (Mermaid)
- [ ] Docker Compose works (`make up`)
- [ ] Tests pass (`make test`)
- [ ] GitHub Actions green
- [ ] OpenAPI docs at `/docs`
- [ ] Demo video (Loom, 5-10 min)
- [ ] Blog post (Medium/dev.to)
- [ ] LinkedIn post (link to repo + post)
- [ ] CV updated

Tugatdingiz? [Loyiha 2: Computer Vision Service](./project-2-cv-service.md) ga o'ting.
