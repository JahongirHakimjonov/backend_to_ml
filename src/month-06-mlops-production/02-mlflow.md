# MLflow — Experiment Tracking

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- MLflow'ning 4 ta komponentini bilasiz (Tracking, Models, Registry, Projects)
- Har bir eksperiment uchun avtomatik logging qila olasiz
- Model Registry bilan production model versioning'ni boshqarasiz
- MLflow'ni production environment'da deploy qila olasiz
- W&B kabi alternativlar bilan ham tanish bo'lasiz

## Nimani o'rganish kerak

- **MLflow Tracking** — eksperimentlarni log qilish
- **MLflow Models** — model formatining standart'i
- **MLflow Model Registry** — versioning, staging, production
- **MLflow Projects** — reproducible runs
- **Backend store** — SQLite, MySQL, Postgres
- **Artifact store** — local, S3, GCS, Azure Blob
- **MLflow UI**va REST API
- **Auto-logging**(PyTorch, sklearn, XGBoost)
- **Alternatives** — W&B, Neptune

## Kutubxonalar

```bash
pip install mlflow
pip install boto3                    # S3 artifact store uchun
pip install psycopg2-binary          # Postgres backend uchun
```

## MLflow komponentlari

```
1. Tracking — har run uchun:
   - Params (hyperparameters)
   - Metrics (accuracy, loss)
   - Artifacts (model file, plots, datasets)
   - Tags (experiment metadata)
   
2. Models — universal format:
   - sklearn, PyTorch, TF, XGBoost, LightGBM
   - Serving uchun standart interface
   
3. Model Registry — production lifecycle:
   - Staging → Production → Archived
   - Version control
   - Webhooks
   
4. Projects — reproducible runs:
   - MLproject file
   - Conda/Docker environments
```

## Kod misollari

### Basic tracking

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.datasets import load_breast_cancer

# Tracking URI (local SQLite + local artifacts)
mlflow.set_tracking_uri("sqlite:///mlruns.db")
mlflow.set_experiment("breast_cancer_classification")

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run(run_name="rf_baseline"):
    # 1. Log params
    n_estimators = 100
    max_depth = 10
    mlflow.log_params({
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "model_type": "RandomForest",
    })
    
    # 2. Train
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
    )
    model.fit(X_train, y_train)
    
    # 3. Log metrics
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    mlflow.log_metrics({"accuracy": accuracy, "f1_score": f1})
    
    # 4. Log model
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="breast_cancer_rf",  # Registry'ga ham
    )
    
    # 5. Log additional artifacts
    report = classification_report(y_test, y_pred, output_dict=False)
    with open("/tmp/report.txt", "w") as f:
        f.write(report)
    mlflow.log_artifact("/tmp/report.txt")
    
    # 6. Tags
    mlflow.set_tag("team", "ml-engineering")
    mlflow.set_tag("version", "v1")
```

### MLflow UI

```bash
mlflow ui --backend-store-uri sqlite:///mlruns.db
# http://localhost:5000 — Tracking dashboard
```

### Auto-logging (oson yo'l)

```python
import mlflow

mlflow.sklearn.autolog()  # Auto-tracking
# yoki: mlflow.pytorch.autolog()
# yoki: mlflow.xgboost.autolog()

# Endi har model.fit() chaqirilganda — barcha params/metrics avtomatik log

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)
# Avtomatik log qilinadi!
```

### Comparing runs (programmatic)

```python
client = mlflow.tracking.MlflowClient()

experiment = client.get_experiment_by_name("breast_cancer_classification")
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_score DESC"],
    max_results=10,
)

for run in runs:
    print(f"Run: {run.info.run_name}")
    print(f"  F1: {run.data.metrics.get('f1_score'):.4f}")
    print(f"  Params: {run.data.params}")
```

### Model loading

```python
# By run ID
model_uri = f"runs:/{run_id}/model"
loaded = mlflow.sklearn.load_model(model_uri)

# From registry (latest version)
model_uri = "models:/breast_cancer_rf/latest"
loaded = mlflow.sklearn.load_model(model_uri)

# Specific version
model_uri = "models:/breast_cancer_rf/3"
loaded = mlflow.sklearn.load_model(model_uri)

# Production stage
model_uri = "models:/breast_cancer_rf/Production"
loaded = mlflow.sklearn.load_model(model_uri)

# Predict
predictions = loaded.predict(X_test)
```

### Model Registry workflow

```python
client = mlflow.tracking.MlflowClient()

# 1. Register model (run.log_model bilan avtomatik)
# yoki manual:
result = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="breast_cancer_rf",
)
print(f"Version: {result.version}")

# 2. Transition stages
client.transition_model_version_stage(
    name="breast_cancer_rf",
    version=result.version,
    stage="Staging",          # None → Staging → Production → Archived
)

# 3. Production'a chiqarish (validation o'tgandan keyin)
client.transition_model_version_stage(
    name="breast_cancer_rf",
    version=result.version,
    stage="Production",
    archive_existing_versions=True,  # eski production → archived
)

# 4. Description, tags
client.update_model_version(
    name="breast_cancer_rf",
    version=result.version,
    description="Improved F1 by 3%, added new features",
)
client.set_model_version_tag(
    name="breast_cancer_rf",
    version=result.version,
    key="trained_by",
    value="ali@company.com",
)
```

### PyTorch + MLflow

```python
import torch
import mlflow.pytorch

mlflow.pytorch.autolog()  # auto-tracking

with mlflow.start_run():
    model = MyPyTorchModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    for epoch in range(10):
        # Training loop
        train_loss = train_epoch(model, train_loader, optimizer)
        val_loss = validate(model, val_loader)
        
        # Manual log (autolog bilan birga)
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
        }, step=epoch)
    
    # Save model
    mlflow.pytorch.log_model(
        model,
        "model",
        registered_model_name="my_pytorch_model",
    )
```

### MLflow Server (production)

```bash
# Postgres backend + S3 artifacts
mlflow server \
    --backend-store-uri postgresql://user:pass@host:5432/mlflow \
    --default-artifact-root s3://my-bucket/mlflow-artifacts \
    --host 0.0.0.0 \
    --port 5000 \
    --workers 4
```

### Production-grade tracking

```python
import os
import mlflow

# Konfiguratsiya environment variables'dan
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow.internal:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://s3.amazonaws.com"
os.environ["AWS_ACCESS_KEY_ID"] = "..."
os.environ["AWS_SECRET_ACCESS_KEY"] = "..."

mlflow.set_experiment("production_models")

with mlflow.start_run(run_name=f"train_{datetime.now().isoformat()}"):
    # Authentication, environment
    mlflow.set_tag("git_commit", subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip())
    mlflow.set_tag("environment", "production")
    mlflow.set_tag("trained_by", os.getenv("USER", "unknown"))
    
    # Data version (DVC bilan)
    mlflow.log_param("data_hash", get_dvc_hash("data/processed.csv"))
    
    # Train...
```

## Backend integratsiyasi

### Production model loading

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import mlflow

@asynccontextmanager
async def lifespan(app):
    # Production model'ni MLflow Registry'dan yuklash
    model_name = "breast_cancer_rf"
    stage = "Production"
    model_uri = f"models:/{model_name}/{stage}"
    
    app.state.model = mlflow.pyfunc.load_model(model_uri)
    app.state.model_version = get_model_version(model_name, stage)
    print(f"Loaded {model_name} v{app.state.model_version}")
    yield

app = FastAPI(lifespan=lifespan)

class PredictionInput(BaseModel):
    features: list[float]

class PredictionOutput(BaseModel):
    prediction: int
    probability: float
    model_version: int

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    X = np.array([data.features])
    pred = app.state.model.predict(X)
    proba = app.state.model.predict_proba(X)
    
    return PredictionOutput(
        prediction=int(pred[0]),
        probability=float(proba[0].max()),
        model_version=app.state.model_version,
    )

@app.get("/model/info")
def model_info():
    return {
        "name": "breast_cancer_rf",
        "version": app.state.model_version,
        "stage": "Production",
    }
```

### Auto-deploy on registry change (webhook)

```python
@app.post("/webhooks/mlflow")
async def mlflow_webhook(payload: dict):
    """Yangi model 'Production'a o'tganda avtomatik reload."""
    
    if payload["event"] == "MODEL_VERSION_TRANSITIONED_STAGE":
        new_stage = payload["data"]["to_stage"]
        if new_stage == "Production":
            # Reload model (graceful)
            model_uri = f"models:/{payload['data']['name']}/Production"
            new_model = mlflow.pyfunc.load_model(model_uri)
            app.state.model = new_model
            app.state.model_version = payload["data"]["version"]
            
            return {"status": "model_reloaded"}
    
    return {"status": "ignored"}
```

### MLflow vs W&B vs Neptune

| | MLflow | Weights & Biases | Neptune.ai |
|---|--------|------------------|------------|
| **Open source** | ✅ | ❌ | ❌ |
| **Self-host** | ✅ | $$ | $$ |
| **UI quality** | O'rta | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Hyperparameter sweeps** | Manual | ✅ Built-in | ✅ |
| **Model Registry** | ✅ | ✅ | ✅ |
| **Collaboration** | O'rta | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Pricing** | Bepul | Free + paid | Free + paid |

**Tavsiya:**Boshlash uchun **MLflow**(open source, controllable). Team collaboration uchun **W&B**.

## Resurslar

- **MLflow docs** — [mlflow.org/docs](https://mlflow.org/docs/)
- **MLflow examples** — [github.com/mlflow/mlflow/tree/master/examples](https://github.com/mlflow/mlflow/tree/master/examples)
- **"Effective MLOps with MLflow"** — Anyscale Academy
- **W&B docs** — [docs.wandb.ai](https://docs.wandb.ai/)

## 🏋️ Mashqlar

### 🟢 Easy
1. SQLite + local MLflow setup, 5 ta run log qiling.
2. `mlflow.sklearn.autolog()` — manual'siz autotracking.
3. MLflow UI'da run'larni solishtiring (table view).

### 🟡 Medium
1. **GridSearchCV + MLflow**: har trial alohida run sifatida log.
2. **PyTorch tracking**: training loop'da har epoch metrics log.
3. **Model Registry workflow**: train → register → Staging → Production.

### 🔴 Hard
1. **Production MLflow server**: Postgres + S3 (MinIO) Docker'da.
2. **Auto-deploy pipeline**: webhook'ga javob beradigan FastAPI servisi.
3. **A/B test framework**: 2 model versiya bir vaqtda serve, traffic split.

## Capstone

`notebooks/month-06/02_mlflow.ipynb`:
- Klassik ML loyiha (Oy 2'dan)
- 10+ ta eksperiment (turli algoritmlar, hyperparams)
- Model Registry'ga eng yaxshisini Production qiling
- FastAPI'da MLflow'dan yuklab serve qiling
- Docker'ga oling

## ✅ Tekshirish ro'yxati

- [ ] MLflow Tracking, Models, Registry farqini bilaman
- [ ] Params, metrics, artifacts log qilishni bilaman
- [ ] Auto-logging ishlataman
- [ ] Model Registry workflow (Staging → Production)
- [ ] FastAPI'da MLflow'dan model yuklash
- [ ] MLflow Server production setup (Postgres + S3)
- [ ] W&B alternativasini bilaman

[DVC — Data Versioning](./03-dvc-data-versioning.md) ga o'tamiz.
