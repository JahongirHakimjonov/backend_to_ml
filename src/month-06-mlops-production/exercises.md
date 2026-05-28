# Oy 6 — Mashqlar to'plami

## 🟢 Easy

### MLflow
1. SQLite + MLflow + 5 ta run.
2. `mlflow.sklearn.autolog()` ishlatish.
3. Model Registry: register → Staging → Production.

### DVC
1. `dvc init` + bitta CSV versioning.
2. Local DVC remote.
3. 2 ta data versiya, eski versiyaga qaytish.

### FastAPI Serving
1. Sklearn modelni FastAPI'ga olib chiqish.
2. Health checks.
3. Prometheus metric'lar.

### Docker / K8s
1. Multi-stage Dockerfile.
2. Docker Compose: API + Postgres.
3. minikube setup.

### Monitoring
1. Evidently AI birinchi report.
2. PSI calculation.
3. Custom Prometheus gauge.

### CI/CD
1. GitHub Actions pytest pipeline.
2. Code quality checks.
3. Docker build action.

### Airflow
1. Local Airflow Docker.
2. Birinchi DAG (hello world).
3. Daily scheduled task.

## 🟡 Medium

### Integrations
1. **MLflow + DVC**: ikkalasini birga loyihada.
2. **FastAPI + MLflow Registry**: production'dan model yuklash.
3. **Docker Compose**: API + MLflow + Postgres + MinIO.
4. **K8s + HPA**: load test bilan auto-scaling.
5. **Airflow + MLflow**: scheduled retraining DAG.

### Real workflows
1. **Full retraining pipeline**: DVC repro + MLflow log + K8s update.
2. **Daily inference batch**: Airflow DAG, 100K users.
3. **Monitoring dashboard**: Grafana + Prometheus + Evidently.
4. **A/B test**: Istio yoki nginx canary deployment.
5. **CML report**: PR'ga avtomatik metrics comparison.

## 🔴 Hard (Production)

### 1. End-to-End MLOps Platform

**Talab:**
- Klassik ML modeli (regression yoki classification)
- DVC for data versioning (S3 yoki MinIO)
- MLflow for experiment tracking + Registry
- DVC + MLflow integration
- FastAPI serving + ONNX optimization
- Docker + K8s deployment (manifest yoki Helm)
- Prometheus + Grafana monitoring
- Evidently AI drift detection
- GitHub Actions CI/CD
- Airflow scheduled retraining
- Slack notifications

**Deliverables:**
- GitHub repo (public)
- README + architecture diagram
- Demo video (Loom)
- LinkedIn post

### 2. Multi-model Platform

**Talab:**
- 3+ ta turli model (classification, regression, NLP)
- Universal serving API (model-as-a-service)
- Per-model routing va versioning
- Centralized monitoring
- Cost tracking per model/user
- API rate limiting

### 3. Real-time Streaming ML

**Talab:**
- Kafka stream (yoki Redis Streams)
- Real-time feature engineering
- Low-latency inference (<50ms p95)
- Online learning (River library)
- Real-time monitoring dashboard

### 4. ML Platform as a Service (MLaaS)

**Talab:**
- User uploads CSV → auto-ML training
- BentoML packaging
- Auto-deployment to K8s
- Per-user namespaces
- Billing integration
- Admin dashboard

## Mini-loyihalar

### Mini-loyiha 1: Personal Health ML Platform
- Fitbit/Apple Health data
- Predict health metrics
- Daily inference + insights
- Telegram bot

### Mini-loyiha 2: E-commerce Recommendation MLOps
- Online learning (recommendations)
- Feature store (Feast)
- A/B test framework
- Real-time deployment

### Mini-loyiha 3: Fraud Detection System
- Streaming fraud detection
- Real-time monitoring
- Alert system
- Explainability dashboard

### Mini-loyiha 4: Computer Vision SaaS
- Multi-tenant CV API
- Image moderation, OCR, classification
- Usage tracking + billing
- Streamlit demo

## Quiz

### MLOps Fundamentals
1. MLOps va DevOps farqi?
2. ML Lifecycle 8 bosqichi?
3. MLOps Maturity Levels (0, 1, 2)?
4. Reproducibility'ning 3 ta asosiy talabi?
5. Why ML monitoring is harder than software monitoring?

### MLflow
1. Tracking, Models, Registry, Projects farqi?
2. Auto-logging qanday ishlaydi?
3. Model Registry stages workflow?
4. Production'ga yangi model qanday rollout qilinadi?
5. MLflow vs W&B vs Neptune?

### DVC
1. Git nima uchun ML data uchun yetmaydi?
2. `dvc.yaml` va `dvc.lock` ning vazifasi?
3. Remote storage variantlari?
4. `dvc repro` qaysi stage'larni qayta ishga tushiradi?
5. DVC vs LakeFS vs Pachyderm?

### Serving
1. FastAPI custom vs BentoML vs TorchServe — qaysi qachon?
2. Batching nima uchun GPU'da muhim?
3. ONNX nima uchun foydali?
4. Async inference patternlari?
5. Blue-green vs canary vs shadow deployment?

### Docker / K8s
1. Multi-stage build nima uchun?
2. K8s Pod, Deployment, Service?
3. Probes (liveness, readiness)?
4. HPA qaysi metric'lar bo'yicha?
5. KServe nima?

### Monitoring
1. Data drift, concept drift, prediction drift?
2. PSI vs KS test?
3. Evidently AI vs WhyLabs?
4. Prometheus Counter vs Histogram vs Gauge?
5. Retraining trigger logic?

### CI/CD
1. ML CI/CD da nima qo'shimcha (klassik DevOps'ga nisbatan)?
2. Code, data, model testing?
3. CML nima qiladi?
4. Deployment strategies?
5. Rollback mechanism?

### Airflow
1. DAG va Task farqi?
2. XCom nima uchun?
3. Sensor'lar?
4. TaskFlow API vs traditional Operators?
5. Airflow vs Prefect vs Dagster?

## ✅ Oy 6 oxiri checklist (eng muhim oy!)

- [ ] MLflow Tracking + Registry
- [ ] DVC data versioning
- [ ] FastAPI ML serving (production-ready)
- [ ] Docker Compose stack
- [ ] Local Kubernetes deployment
- [ ] Prometheus + Grafana monitoring
- [ ] Evidently AI drift detection
- [ ] GitHub Actions ML pipeline
- [ ] CML reports
- [ ] Airflow DAG for retraining
- [ ] End-to-end MLOps loyiha GitHub'da
- [ ] Architecture diagram
- [ ] LinkedIn post (sertifikat + GitHub link)
- [ ] CV'ni yangilash: "ML Engineer / MLOps Engineer"
- [ ] 5+ vakansiyaga ariza yuborish

**6 oy tugadi!**

Siz endi to'liq **ML Engineer / MLOps Engineer**siz. Keyingi bosqich:

1. **[Final Loyihalar](../final-projects/README.md)** — portfolio uchun 4 katta loyiha
2. **Job applications** — vakansiyalarga ariza
3. **Open source contributions** — MLflow, Evidently, DVC, va h.k. ga
4. **Speaking** — meetup'larda ML/MLOps haqida gapirish
5. **Mentor** — boshqalarga o'rgatish

Hamma narsa sizning qo'lingizda. Omad!
