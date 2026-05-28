# Oy 6 — MLOps va Production

## 🎯 Bu oydagi maqsad

**Bu oy — sizning asosiy maqsadingiz uchun eng muhim oy.** ML Engineer / MLOps Engineer bo'lish uchun shu oy bilim sizning **portfolio**ngizning markazi bo'ladi.

Oy oxirida siz quyidagilarni qila olasiz:
- MLOps lifecycle'ni boshidan oxirigacha bilasiz
- MLflow bilan eksperimentlarni track qilasiz va modellarni versioning qilasiz
- DVC bilan data versioning va reproducibility ta'minlaysiz
- FastAPI + BentoML/TorchServe bilan ML modellarni serve qilasiz
- Docker + Kubernetes'da ML deployment
- Prometheus + Grafana + Evidently AI bilan monitoring va drift detection
- Apache Airflow bilan ML pipeline'larni orkestrlaysiz
- GitHub Actions bilan ML CI/CD

## 📅 Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | MLOps intro + MLflow + DVC | 10-12 soat |
| **Hafta 2** | FastAPI serving + Docker + K8s | 12-15 soat |
| **Hafta 3** | Monitoring + CI/CD | 10-12 soat |
| **Hafta 4** | Airflow + End-to-End capstone | 12-15 soat |

## 📖 Boblar tartibi

1. [MLOps ga kirish](./01-mlops-intro.md)
2. [MLflow — Experiment tracking](./02-mlflow.md)
3. [DVC — Data Versioning](./03-dvc-data-versioning.md)
4. [FastAPI + ML Serving](./04-fastapi-ml-serving.md)
5. [Docker va Kubernetes](./05-docker-kubernetes.md)
6. [Model Monitoring](./06-model-monitoring.md)
7. [CI/CD for ML](./07-ci-cd-ml.md)
8. [Airflow va Prefect](./08-airflow-prefect.md)
9. [Mashqlar](./exercises.md)

## 🎓 Oy oxirida nima qila olasiz?

- To'liq production ML system qurish: training → versioning → serving → monitoring
- ML model deployment Kubernetes'da
- Drift detection bilan model degradation'ni avtomatik aniqlash
- CI/CD pipeline ML uchun (test, validate, deploy)
- Airflow DAG bilan haftalik retraining
- Job descriptionlarda yozilgan **MLOps Engineer** talablariga javob bera olish

## 💡 Backend Dev uchun maslahat — bu oy sizning oltin oyingiz!

Sizning **mavjud bilim**laringiz aynan shu oyda **kuchli ustunlik** beradi:

| Backend bilim | MLOps'da qo'llanish |
|---------------|---------------------|
| **Docker, docker-compose** | ML containers |
| **PostgreSQL** | Feature store, prediction logs |
| **Redis** | Model cache, feature cache |
| **Celery, Kafka** | Async inference, streaming |
| **GitHub Actions / GitLab CI** | ML CI/CD |
| **Nginx, load balancing** | ML model serving |
| **Prometheus, Grafana** | ML monitoring |
| **REST API design** | ML inference endpoints |
| **Async/await** | Concurrent inference |
| **Microservices** | ML services architecture |

Aksariyat ML Engineerlar (data scientist'lardan kelganlar) bu narsalarni **nol darajadan** o'rganishadi. Sizning **boshlang'ich darajangiz** ulardan ancha yuqori.

## 💰 Cloud Cost (ixtiyoriy)

Bu oy uchun cloud xizmatlari kerak bo'ladi. Variantlar:

1. **AWS Free Tier** ($300 credit yangi accountlar)
2. **GCP Free Tier** ($300 credit)
3. **DigitalOcean** ($200 credit student/coupon)
4. **Hetzner** — eng arzon (€5/oy server)
5. **Lokal Kubernetes** (minikube, kind, k3s) — bepul, kichik loyihalar uchun yetadi

**Maslahat:** Asosiy mashqlar lokal Docker + minikube bilan, faqat capstone uchun real cloud.

## 🚀 Boshlash

[MLOps ga kirish](./01-mlops-intro.md) bilan boshlang.
