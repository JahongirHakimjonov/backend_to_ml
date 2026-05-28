# Month 06 — MLOps Notebooks

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `01_mlops_intro.ipynb` | Project setup | [MLOps intro](../../src/month-06-mlops-production/01-mlops-intro.md) |
| `02_mlflow.ipynb` | Experiment tracking | [MLflow](../../src/month-06-mlops-production/02-mlflow.md) |
| `03_dvc.ipynb` | Data versioning | [DVC](../../src/month-06-mlops-production/03-dvc-data-versioning.md) |
| `04_fastapi_serving.ipynb` | API serving | [FastAPI](../../src/month-06-mlops-production/04-fastapi-ml-serving.md) |
| `05_monitoring.ipynb` | Drift detection | [Monitoring](../../src/month-06-mlops-production/06-model-monitoring.md) |

## 🛠 Dependencies

```bash
# MLOps + Backend stack
uv sync --group month-06

# GPU ONNX runtime (Linux/Windows + NVIDIA)
uv sync --group month-06 --group onnx-gpu

uv run jupyter lab
```

Tarkibida: mlflow, dvc, prometheus-client, evidently, prefect, bentoml, onnx, fastapi, uvicorn, sqlalchemy, redis, celery, boto3, minio va h.k.

## 🐳 Docker bilan

Bu oydagi ko'p ishlash Docker'da bo'ladi:

```bash
# MLflow Server
docker run -p 5000:5000 ghcr.io/mlflow/mlflow

# MinIO (S3 alternative)
docker run -p 9000:9000 minio/minio server /data

# Prometheus + Grafana
docker compose -f monitoring/docker-compose.yml up

# Airflow (Hafta 4)
docker compose -f airflow/docker-compose.yml up
```

## ☸️ Kubernetes setup

```bash
# Local minikube
brew install minikube
minikube start --cpus=4 --memory=8192

# Yoki k3s
curl -sfL https://get.k3s.io | sh -
```

[Asosiy bob](../../src/month-06-mlops-production/README.md).
