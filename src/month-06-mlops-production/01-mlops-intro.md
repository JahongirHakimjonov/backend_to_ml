# MLOps ga kirish

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- MLOps nima ekanini, DevOps'dan farqini bilasiz
- ML lifecycle'ning to'liq pictureasini bilasiz
- MLOps maturity levellarini va kompaniyaning qaysi darajadaligini baholash mumkin bo'ladi
- Eng muhim tool ekosistemasini bilasiz

## Nimani o'rganish kerak

- **MLOps tushunchasi**va paydo bo'lishi
- **ML Lifecycle** — data → train → deploy → monitor
- **DevOps vs DataOps vs MLOps**
- **ML Maturity Levels**(Google MLOps levels 0-2)
- **MLOps challenges** — reproducibility, drift, scaling
- **Tool landscape** — open source vs managed services
- **Team structure** — Data Engineer, ML Engineer, Data Scientist

## MLOps — nima va nima uchun?

### Klassik ML loyihaning hayotiy davri

```
Data Scientist Jupyter notebook'da:
  1. Pandas bilan data oladi
  2. Model train qiladi
  3. "model.pkl" saqlab beradi
  4. Aytadi: "Production'ga qo'ying"

Backend Engineer:
  1. .pkl yuklaydi
  2. FastAPI'ga qo'shadi
  3. Deploy qiladi
  4. Hammasi yaxshi... bir necha hafta

Ikki oydan keyin:
  - Model accuracy tushib ketdi (drift!)
  - Data scientist yangi model yuborib turibdi (yangi format)
  - Hech kim asl natijani reproduce qila olmaydi
  - Audit logs yo'q
  - A/B test ham yo'q
  - Production'da xato qilsa, hech kim sezmaydi
```

**MLOps shu muammolarni hal qiladi.**

### DevOps vs MLOps

```
DevOps:
  Code → Test → Build → Deploy → Monitor

MLOps:
  Data → Validate → Train → Test → Register → Deploy → Monitor → Retrain
  ↑                                                                    ↓
  └──────────────── Feedback loop ────────────────────────────────────┘
```

**Asosiy farqlar:**
- **Data**ham versioning kerak (kod ham)
- **Model** — bu artifact, har retraining'da yangisi
- **Performance**vaqt o'tishi bilan **degradatsiyaga**uchraydi (drift)
- **Reproducibility** — bir xil natijani qayta olish qiyin (randomness, data o'zgarishi)
- **Testing** — accuracy yoki business metric'lar

### Google MLOps Maturity Levels

#### Level 0 — Manual
```
Data scientist: kompyuterda manual
Production: oddiy script, manual deploy
Monitoring: yo'q yoki kam
```
✅ Yangi loyihalar, MVP, kichik kompaniyalar
❌ Production-grade emas

#### Level 1 — ML pipeline automation
```
Training pipeline avtomatik (Airflow yoki shunga o'xshash)
Data validation, model validation, automated retraining
Hali deployment manual yoki semi-automatic
```
✅ O'rta kompaniyalar
✅ Aksariyat real-world ML loyihalar shu darajada

#### Level 2 — CI/CD pipeline
```
Hammasi avtomatik:
- Code/data CI: validation, testing
- ML pipeline CD: yangi model avtomatik deploy
- Monitoring orqali retraining trigger
- A/B testing infrastructure
```
✅ Yetuk MLOps madaniyati (Google, Netflix, Uber)

## MLOps Tool Ecosystem (2024-2026)

### Experiment Tracking
- **MLflow** ⭐⭐⭐⭐⭐ — open source, eng keng tarqalgan
- **Weights & Biases** — managed, ajoyib UI
- **Neptune.ai** — managed alternative
- **Comet** — alternative

### Data Versioning
- **DVC** ⭐⭐⭐⭐⭐ — Git for data
- **LakeFS** — data warehouse
- **Pachyderm** — kubernetes-native
- **Delta Lake** — Databricks ekosistemasi

### Feature Store
- **Feast** ⭐⭐⭐⭐ — open source
- **Tecton** — managed (Feast'dan paydo bo'lgan)
- **Hopsworks** — alternative

### Model Serving
- **FastAPI**+ custom — sodda, fleksibel
- **TorchServe** — PyTorch native
- **TensorFlow Serving** — TF native
- **BentoML** ⭐⭐⭐⭐ — Python-friendly, fleksibel
- **Ray Serve** — distributed
- **Triton (NVIDIA)** — production-grade GPU serving
- **vLLM** — LLM-specific, juda tez

### Workflow Orchestration
- **Apache Airflow** ⭐⭐⭐⭐⭐ — bibliya
- **Prefect** — modern, Pythonic
- **Dagster** — data-aware
- **Kubeflow Pipelines** — k8s-native
- **Metaflow** — Netflix'dan

### Monitoring
- **Prometheus + Grafana** — infrastructure
- **Evidently AI** ⭐⭐⭐⭐⭐ — data/model drift
- **WhyLabs** — managed alternative
- **Arize, Fiddler** — enterprise

### Deployment Platforms
- **Kubernetes**+ custom — flexibility
- **AWS SageMaker** — managed
- **GCP Vertex AI** — managed
- **Azure ML** — managed
- **Databricks** — unified analytics

### LLMOps (specific to LLM)
- **Langfuse** ⭐⭐⭐⭐⭐ — open source observability
- **LangSmith** — LangChain ekosistemasi
- **Helicone** — proxy + analytics
- **Phoenix**(Arize) — open source

## ML Lifecycle batafsil

```
1. PROBLEM DEFINITION
   - Business problem → ML problem
   - Success metrics (online + offline)
   
2. DATA COLLECTION
   - Source identification
   - Sampling strategy
   - Privacy/compliance
   
3. DATA PREPARATION  
   - Cleaning, transformation
   - Feature engineering
   - Train/val/test split
   - Data versioning (DVC)
   
4. MODEL DEVELOPMENT
   - Algorithm selection
   - Hyperparameter tuning
   - Experiment tracking (MLflow)
   - Reproducibility
   
5. MODEL EVALUATION
   - Offline metrics
   - Bias/fairness analysis
   - Edge cases testing
   - Stakeholder review
   
6. MODEL DEPLOYMENT
   - Containerization (Docker)
   - Orchestration (K8s)
   - Serving framework (FastAPI/BentoML)
   - API design
   
7. MODEL MONITORING
   - Performance metrics
   - Data drift detection
   - Concept drift detection
   - Business KPIs
   
8. CONTINUOUS IMPROVEMENT
   - A/B testing
   - Shadow deployment
   - Champion-challenger
   - Automated retraining
```

## Tipik MLOps loyiha strukturasi

```
ml_project/
├── data/                       # Raw data (DVC tracked, not git)
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/                  # Exploration
│   └── 01_eda.ipynb
├── src/                        # Source code
│   ├── data/
│   │   ├── make_dataset.py
│   │   └── validate.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   └── api/
│       └── main.py             # FastAPI
├── tests/
│   ├── test_data.py
│   ├── test_features.py
│   └── test_model.py
├── configs/
│   ├── config.yaml
│   └── model_v1.yaml
├── dvc.yaml                    # DVC pipeline
├── params.yaml                 # Hyperparameters
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/
│   ├── ci.yml
│   ├── train.yml
│   └── deploy.yml
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
├── airflow/dags/               # Workflow orchestration
│   └── retrain_dag.py
├── monitoring/
│   ├── prometheus.yml
│   └── grafana_dashboard.json
├── requirements.txt
├── pyproject.toml
├── README.md
└── Makefile                    # Common commands
```

## Backend dev → MLOps Engineer: skill mapping

Sizda allaqachon bor:
- ✅ REST API (FastAPI, DRF)
- ✅ Docker, docker-compose
- ✅ PostgreSQL, Redis
- ✅ Celery (async tasks)
- ✅ CI/CD (GitHub Actions / GitLab CI)
- ✅ Linux, basic Kubernetes
- ✅ Monitoring (Prometheus/Grafana)
- ✅ Git workflow
- ✅ Testing (pytest)

Yangi o'rganish kerak:
- ML lifecycle thinking
- Experiment tracking (MLflow)
- Data versioning (DVC)
- Model serving frameworks (BentoML)
- Drift detection (Evidently)
- Workflow orchestration (Airflow)
- Feature stores (Feast)

**Bu 6 ta narsani 4 hafta'da o'rganish realistik.**

## Resurslar

### Kitoblar (must)
- **"Designing Machine Learning Systems"** — Chip Huyen (eng yaxshi MLOps kitobi)
- **"Machine Learning Engineering"** — Andriy Burkov
- **"Building Machine Learning Pipelines"** — Hannes Hapke & Catherine Nelson
- **"Practical MLOps"** — Noah Gift

### Online kurslar (must)
- **MLOps Zoomcamp** — DataTalks.Club ([github.com/DataTalksClub/mlops-zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)) — **MUST DO**, bepul
- **Made With ML** — Goku Mohandas (bepul)
- **Full Stack Deep Learning** — Berkeley course
- **DeepLearning.AI MLOps Specialization** — Andrew Ng

### Blog'lar
- **Chip Huyen's blog** — [huyenchip.com/blog](https://huyenchip.com/blog/)
- **Eugene Yan's blog** — [eugeneyan.com](https://eugeneyan.com/)
- **Neptune.ai blog** — MLOps articles
- **Towards Data Science** — MLOps section

### Communities
- **MLOps Community Slack** — [mlops.community](https://mlops.community/)
- **DataTalks.Club Slack**
- **Reddit r/MachineLearning, r/MLOps**

## 🏋️ Mashqlar

### 🟢 Easy
1. Yuqoridagi tool landscape'dagi 10 ta toolni Google qiling, har birining qisqa tavsifini yozing.
2. O'z kompaniyangiz/loyihangiz MLOps maturity level qaysi darajada — baholang.
3. ML Lifecycle'ning 8 ta bosqichini o'z so'zlaringiz bilan tushuntiring.

### 🟡 Medium
1. Mavjud Django/FastAPI loyihangizga ML integratsiya plani yozing (qaerda, qanday, qaysi tool'lar).
2. ChatGPT yoki Claude bilan suhbat — "MLOps Engineer interviewdagi 20 ta savol va javob".
3. Job posting saytlardan 5 ta "MLOps Engineer" vakansiyani tahlil qiling, qaysi tool'lar talab qilinadi.

### 🔴 Hard
1. **Plan template**: ML loyiha uchun to'liq ML Engineering Document yarating (problem statement → success metrics → architecture).
2. **Tool comparison**: BentoML vs TorchServe vs Triton — POC bilan solishtirish.

## Capstone

`notebooks/month-06/01_mlops_intro.ipynb`:
- Bitta sodda klassik ML loyiha (masalan, churn prediction)
- To'liq strukturani yarating (yuqoridagi struktura bo'yicha)
- Hozircha tool'lar yo'q, lekin kelajak bo'limlarda har birini qo'shamiz

## ✅ Tekshirish ro'yxati

- [ ] MLOps va DevOps farqini bilaman
- [ ] ML Lifecycle 8 bosqichini bilaman
- [ ] MLOps Maturity Levels (0, 1, 2)
- [ ] Asosiy tool landscape'ni bilaman
- [ ] Tipik MLOps loyiha strukturasini bilaman
- [ ] Mavjud backend bilimimning MLOps'da qanday foyda berishini ko'rdim

[MLflow — Experiment tracking](./02-mlflow.md) ga o'tamiz.
