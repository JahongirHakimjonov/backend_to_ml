# Docker va Kubernetes

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- ML-specific Docker best practices (kichik image, layer caching)
- Multi-stage build bilan kichik production image
- Docker Compose bilan to'liq stack
- Kubernetes asoslari (Deployment, Service, Ingress)
- ML uchun K8s (KServe, Kubeflow)
- HPA (autoscaling) va resource limits

## Nimani o'rganish kerak

- **Docker** — multi-stage builds, layer caching,.dockerignore
- **Docker Compose** — local development stack
- **Kubernetes basics** — Pod, Deployment, Service, Ingress, ConfigMap, Secret
- **K8s resource management** — requests, limits, QoS
- **Horizontal Pod Autoscaler (HPA)**
- **KServe / Seldon** — K8s-native model serving
- **GPU on K8s** — NVIDIA device plugin
- **Helm charts** — packaging
- **GitOps** — ArgoCD, Flux

## ML-specific Docker challenges

### Muammolar
1. **Katta image** — sklearn 200MB, PyTorch 2GB, with CUDA 5GB+
2. **Slow builds** — dependencies cache'lash qiyin
3. **GPU access** — CUDA + cuDNN versioning
4. **Model fayllari** — image'ga embed yoki runtime download?

### Yechimlar
- Multi-stage build
- `pip install --no-cache-dir`
- Slim base images
- Model'ni runtime'da S3/MinIO'dan yuklash
- Layer caching uchun requirements alohida COPY

## Kod misollari

### Optimal Dockerfile (ML uchun)

```dockerfile
# syntax=docker/dockerfile:1.6
# Multi-stage build

# === Stage 1: Builder ===
FROM python:3.11-slim AS builder

WORKDIR /build

# System deps (compile uchun)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install in virtual env
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Requirements (cache layer)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# === Stage 2: Runtime ===
FROM python:3.11-slim AS runtime

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Non-root user (xavfsizlik)
RUN useradd -m -u 1000 mluser
USER mluser
WORKDIR /app

# Code
COPY --chown=mluser:mluser src/ ./src/
COPY --chown=mluser:mluser models/ ./models/

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s \
    CMD curl -f http://localhost:8000/health/ready || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### .dockerignore (juda muhim!)

```
# .dockerignore
__pycache__/
*.pyc
*.pyo
*.egg-info/
.git/
.github/
.dvc/cache/
.pytest_cache/
.mypy_cache/
.venv/
venv/
*.ipynb
.idea/
.vscode/
.env
.env.local
notebooks/
data/raw/
data/interim/
mlruns/
docs/
README.md
LICENSE
tests/
*.md
```

### GPU Dockerfile

```dockerfile
FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Python install
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# PyTorch with CUDA
RUN pip install --no-cache-dir \
    torch==2.4.0 torchvision \
    --index-url https://download.pytorch.org/whl/cu121

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY models/ /app/models/
WORKDIR /app

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# GPU run
docker run --gpus all -p 8000:8000 my-ml-image
```

### Docker Compose — to'liq stack

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_URI=models:/churn_predictor/Production
      - MLFLOW_TRACKING_URI=http://mlflow:5000
      - DATABASE_URL=postgresql://ml:ml@postgres:5432/mldb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mlflow
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/ready"]
      interval: 30s
  
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    command: >
      mlflow server
      --backend-store-uri postgresql://ml:ml@postgres:5432/mlflow
      --default-artifact-root s3://mlflow-artifacts/
      --host 0.0.0.0
      --port 5000
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_S3_ENDPOINT_URL=http://minio:9000
      - AWS_ACCESS_KEY_ID=minioadmin
      - AWS_SECRET_ACCESS_KEY=minioadmin
    depends_on:
      - postgres
      - minio
  
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ml
      POSTGRES_PASSWORD: ml
      POSTGRES_DB: mldb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
  
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  minio_data:
  grafana_data:
```

```bash
# Start
docker-compose up -d

# Logs
docker-compose logs -f api

# Stop
docker-compose down
```

## Kubernetes basics

### Asosiy tushunchalar

```
Pod          — eng kichik unit (1 yoki ko'p container)
Deployment   — N ta pod'ni boshqaradi (rolling updates)
Service      — pod'larga endpoint beradi (load balancing)
Ingress      — tashqi HTTP traffic (Nginx, Traefik)
ConfigMap    — non-secret config
Secret       — passwords, keys
PVC          — persistent volume (data storage)
HPA          — auto-scaling
```

### Local Kubernetes setup

```bash
# Variant 1: minikube
brew install minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Variant 2: kind
brew install kind
kind create cluster

# Variant 3: k3s (production-grade lightweight)
curl -sfL https://get.k3s.io | sh -

# Variant 4: Docker Desktop K8s (oddiy)
# Settings → Kubernetes → Enable
```

### ML service Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
  labels:
    app: ml-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
    spec:
      containers:
      - name: api
        image: myregistry/ml-api:v1.2.3
        ports:
        - containerPort: 8000
        
        # Resource limits
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "2000m"
            memory: "2Gi"
        
        # Environment
        env:
        - name: MODEL_URI
          value: "models:/churn_predictor/Production"
        - name: MLFLOW_TRACKING_URI
          valueFrom:
            configMapKeyRef:
              name: ml-config
              key: mlflow_uri
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ml-secrets
              key: database_url
        
        # Probes
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        
        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["sleep", "10"]
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-api-svc
spec:
  selector:
    app: ml-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP   # yoki LoadBalancer for external
```

### Ingress (HTTP routing)

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ml-api-svc
            port:
              number: 80
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls
```

### HPA — auto-scaling

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  # Custom metric (Prometheus)
  - type: Pods
    pods:
      metric:
        name: prediction_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

### ConfigMap + Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ml-config
data:
  mlflow_uri: "http://mlflow.mlflow.svc.cluster.local:5000"
  model_name: "churn_predictor"
  batch_size: "32"
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ml-secrets
type: Opaque
stringData:
  database_url: "postgresql://user:pass@postgres:5432/ml"
  openai_api_key: "sk-..."
```

### Apply

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml

# Status
kubectl get pods
kubectl get deployments
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f

# Scale manually
kubectl scale deployment ml-api --replicas=10

# Rolling update
kubectl set image deployment/ml-api api=myregistry/ml-api:v1.3.0
kubectl rollout status deployment/ml-api
kubectl rollout undo deployment/ml-api   # rollback
```

### GPU on K8s

```yaml
# gpu-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-gpu-api
spec:
  template:
    spec:
      containers:
      - name: api
        image: myregistry/ml-gpu-api:latest
        resources:
          limits:
            nvidia.com/gpu: 1   # 1 ta GPU
      nodeSelector:
        accelerator: nvidia-tesla-t4   # optional
```

### KServe (K8s-native ML serving)

```yaml
# kserve-inference.yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: churn-predictor
spec:
  predictor:
    sklearn:
      storageUri: s3://my-bucket/models/churn/v1/
      resources:
        requests:
          cpu: "100m"
          memory: "256Mi"
        limits:
          cpu: "1000m"
          memory: "1Gi"
```

```bash
kubectl apply -f kserve-inference.yaml

# Auto-creates: deployment, service, ingress, scaler
# Endpoint:
curl http://churn-predictor.default.example.com/v1/models/churn-predictor:predict \
    -d '{"instances": [[1.0, 2.0, 3.0]]}'
```

## Backend integratsiyasi

### Helm chart structure

```
ml-api-chart/
├── Chart.yaml
├── values.yaml
├── values.production.yaml
├── values.staging.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── configmap.yaml
    └── secret.yaml
```

```yaml
# values.yaml
replicaCount: 3

image:
  repository: myregistry/ml-api
  tag: "1.2.3"
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

ingress:
  enabled: true
  host: api.example.com

env:
  MLFLOW_URI: http://mlflow:5000
```

```bash
# Deploy
helm install ml-api ./ml-api-chart -f values.production.yaml

# Upgrade
helm upgrade ml-api ./ml-api-chart --set image.tag=1.2.4

# Rollback
helm rollback ml-api
```

## Resurslar

- **Docker docs** — [docs.docker.com](https://docs.docker.com/)
- **Kubernetes Basics** — [kubernetes.io/docs/tutorials](https://kubernetes.io/docs/tutorials/)
- **"Kubernetes in Action"** — Marko Lukša
- **KServe docs** — [kserve.github.io/website](https://kserve.github.io/website/)
- **Kubeflow Pipelines** — [kubeflow.org/docs/components/pipelines](https://www.kubeflow.org/docs/components/pipelines/)
- **Helm docs** — [helm.sh/docs](https://helm.sh/docs/)

## 🏋️ Mashqlar

### 🟢 Easy
1. ML servisni Docker'da run qiling.
2. Multi-stage Dockerfile yozing (kichik image).
3. Docker Compose bilan API + Postgres + Redis.

### 🟡 Medium
1. **Full stack**: API + MLflow + Postgres + MinIO + Prometheus Compose.
2. **Local K8s**: minikube'da ML servisni deploy qiling.
3. **HPA**: load test bilan auto-scaling'ni ko'ring.

### 🔴 Hard
1. **Production K8s**: real cloud (DigitalOcean K8s yoki AWS EKS) — full deploy.
2. **KServe**: sklearn modelni KServe orqali Kubernetes'da serve.
3. **Helm chart**: o'z chart'ingizni yozing, GitHub'ga publish qiling.

## Capstone

`docker-compose.yml` + `k8s/`:
- Production-ready Docker stack
- Local Kubernetes (minikube/k3s) deployment
- HPA configured
- Prometheus + Grafana dashboard

## ✅ Tekshirish ro'yxati

- [ ] Multi-stage Dockerfile yozaman
- [ ] Docker Compose bilan to'liq stack
- [ ] Kubernetes Pod, Deployment, Service tushunaman
- [ ] Probes (liveness, readiness)
- [ ] HPA bilan auto-scaling
- [ ] ConfigMap va Secret
- [ ] Helm chart yozish asoslari
- [ ] KServe / Kubeflow asoslari

[Model Monitoring](./06-model-monitoring.md) ga o'tamiz.
