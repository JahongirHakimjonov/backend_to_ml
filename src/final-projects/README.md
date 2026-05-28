# Final Loyihalar (Portfolio)

## 🎯 Maqsad

6 oy davomida o'rgangan bilimlaringizni amaliyotda ko'rsatadigan **4 ta katta loyiha**. Bular sizning:
- GitHub portfoliongiz
- CV'dagi "Projects" bo'limi
- Interviewlar uchun materialingiz
- LinkedIn postlaringiz

## 4 ta loyiha

| # | Loyiha | Asosiy texnologiyalar | Davomiyligi |
|---|--------|----------------------|-------------|
| **1** | [Prediction API](./project-1-prediction-api.md) | Klassik ML + FastAPI + Postgres + Docker | 2-3 hafta |
| **2** | [Computer Vision Service](./project-2-cv-service.md) | YOLO + FastAPI + Celery + S3 | 2-3 hafta |
| **3** | [RAG Chatbot](./project-3-rag-chatbot.md) | LLM + Qdrant + LangChain + Streamlit | 2-3 hafta |
| **4** | [MLOps Pipeline](./project-4-mlops-pipeline.md) | DVC + MLflow + Airflow + K8s | 3-4 hafta |

## Har bir loyiha uchun talablar (minimum)

### Texnik
- [ ] **GitHub'da public repo**(clear README)
- [ ] **Docker + docker-compose** — bir buyruq bilan ishga tushadigan
- [ ] **Tests** — pytest, kamida 50% coverage
- [ ] **CI/CD** — GitHub Actions
- [ ] **API documentation** — OpenAPI/Swagger
- [ ] **Architecture diagram**(Mermaid yoki Excalidraw)
- [ ] **Environment variables** — `.env.example` faylda

### Code Quality
- [ ] **Type hints** — Pythonda hamma yerda
- [ ] **Linting** — ruff yoki flake8
- [ ] **Formatting** — black yoki ruff format
- [ ] **Pre-commit hooks**

### Documentation
- [ ] **README** — installation, usage, API examples
- [ ] **Architecture explanation** — qaror sabablari
- [ ] **Demo video** — Loom (5-10 daqiqa)
- [ ] **Blog post** — Medium/dev.to (har biri uchun)

### Production
- [ ] **Healthcheck endpoint** — `/health`
- [ ] **Logging** — structured (JSON)
- [ ] **Error handling** — Sentry yoki shunga o'xshash
- [ ] **Rate limiting** — slowapi yoki nginx
- [ ] **Security** — API keys, CORS, input validation

## Nima uchun aynan bu 4 ta?

### Loyiha 1 — Klassik ML (oson, lekin to'liq)
- **Maqsad:**End-to-end ML lifecycle'ni ko'rsatish
- **Highlight:**Reproducibility, monitoring
- **Vakansiyalar:**"Junior ML Engineer", "Data Scientist"

### Loyiha 2 — Computer Vision (Deep Learning)
- **Maqsad:**DL'ni production'da ishlata olishni ko'rsatish
- **Highlight:**GPU optimization, async processing
- **Vakansiyalar:**"Computer Vision Engineer", "ML Engineer"

### Loyiha 3 — RAG/LLM (Modern AI)
- **Maqsad:**AI Product engineering ko'nikmasi
- **Highlight:**LLM expertise, vector DB, system design
- **Vakansiyalar:**"AI Engineer", "LLM Engineer", "GenAI Engineer"

### Loyiha 4 — MLOps Platform (eng murakkab)
- **Maqsad:**Sizning asosiy maqsadingiz — MLOps Engineer
- **Highlight:**Sistema arxitekturasi, multi-tool integration
- **Vakansiyalar:**"MLOps Engineer", "ML Platform Engineer", "Senior ML Engineer"

## Standart loyiha strukturasi

```
project-name/
├── README.md                       # Asosiy
├── ARCHITECTURE.md                 # System design
├── docker-compose.yml
├── Dockerfile
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── src/
│   ├── api/                        # FastAPI endpoints
│   ├── core/                       # Business logic
│   ├── data/                       # Data layer
│   ├── ml/                         # ML/model code
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── notebooks/                      # Exploration
├── data/                           # DVC tracked
├── models/                         # MLflow tracked
├── k8s/ (yoki helm/)               # Deployment manifests
├── monitoring/                     # Prometheus, Grafana configs
├── docs/                           # Additional docs
├── scripts/                        # Utility scripts
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── .dockerignore
└── Makefile                        # Common commands
```

## Loyiha boshlash checklist

Yangi loyihani boshlashdan oldin:

- [ ] GitHub repo yarating (public)
- [ ] Initial README (loyihaning maqsadi)
- [ ] Architecture diagram
- [ ] Tech stack tanlash (sabablar bilan)
- [ ] User stories yoki use cases
- [ ] MVP definition (1 hafta uchun)
- [ ] Roadmap (haftalik milestones)

## Portfolio prezentatsiyasi

Loyiha tugagandan keyin:

1. **LinkedIn post**(template):
```
🚀 Yangi loyiha: [LOYIHA NOMI]

Vazifa: [bir gap]

Tech stack:
🔹 [tech 1]
🔹 [tech 2]
🔹 [tech 3]

Key achievements:
✅ [natija 1]
✅ [natija 2]
✅ [natija 3]

GitHub: [link]
Demo: [link]
Blog: [link]

#MLOps #MachineLearning #Python

cc: @jahongir-hakimjonov — "Backend to ML Roadmap" muallifi
(loyihangizni LinkedIn'da ulashganda muallifni tag qiling — yordam yoki review kerak bo'lsa, javob beraman)
```

2. **CV'ga qo'shish:**
```
Project: [LOYIHA NOMI] (date)
- Tech: Python, FastAPI, Docker, K8s, MLflow, ...
- Built end-to-end ML system: [bir gap haqida]
- Achieved [aniq metric]
- GitHub: [link]
```

3. **Portfolio website:** [yourname.dev](https://yourname.dev)
 - 4 ta loyihaning galereyasi
 - Har biri uchun: image, description, links

## Interview preparation

Har bir loyiha haqida shu savollarga javob tayyorlang:

- **Why this project?**(motivatsiya)
- **What's the architecture?**(tushuntirish + diagram)
- **What were the challenges?**(texnik)
- **What would you do differently?**(refleksiya)
- **How would you scale it 10x?**(sistema dizayni)
- **What metrics define success?**(mahsulot tushunchasi)
- **Show me the code**(jonli)

## Mukammal natija uchun maslahatlar

1. **Sifat > Miqdor** — 4 ta zo'r loyiha 10 ta o'rtachadan yaxshiroq
2. **Real-world data** — toy datasets'dan tashqari
3. **Documentation** — coddan ham muhim
4. **Demo video** — recruiter'lar README o'qimaydi, lekin video ko'radi
5. **Open source** — pull request'lar qabul qiling
6. **Blogging** — har loyihaga texnik post yozing
7. **GitHub README** — emoji, badges, diagrams, screenshots

## Boshlash

[Loyiha 1: Prediction API](./project-1-prediction-api.md) bilan boshlang.
