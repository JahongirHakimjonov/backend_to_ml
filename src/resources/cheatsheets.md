# Cheatsheets

## Python

### NumPy cheatsheet
```python
import numpy as np

# Yaratish
a = np.array([1, 2, 3])
zeros = np.zeros((3, 4))
ones = np.ones((2, 2))
eye = np.eye(5)
rng = np.arange(0, 10, 2)
lin = np.linspace(0, 1, 5)
rand = np.random.rand(3, 3)
randn = np.random.randn(3, 3)  # normal

# Shape
arr.shape, arr.dtype, arr.ndim, arr.size
arr.reshape(2, 6)
arr.T  # transpose
arr.flatten()

# Slicing va Indexing
arr[1:3]
arr[arr > 5]  # boolean
arr[[0, 2, 4]]  # fancy
arr[:, 1]  # 2-ustun

# Math
np.dot(a, b), a @ b, np.matmul(a, b)
arr.sum(axis=0), arr.mean(), arr.std()
np.exp, np.log, np.sqrt
np.where(condition, x, y)

# Linear algebra
np.linalg.inv(A)
np.linalg.det(A)
np.linalg.eig(A)
np.linalg.svd(A)
np.linalg.norm(v)
```

### Pandas cheatsheet
```python
import pandas as pd

# I/O
df = pd.read_csv("file.csv")
df = pd.read_parquet("file.parquet")
df.to_csv("out.csv", index=False)

# Inspection
df.head(), df.tail(), df.sample(5)
df.info(), df.describe(), df.shape
df.dtypes, df.columns
df.isna().sum()

# Selection
df["col"], df[["col1", "col2"]]
df.iloc[0:5, 1:3]
df.loc[df.age > 30, "name"]
df.query("age > 30 and country == 'UZ'")

# Filtering
df[df["age"] > 18]
df.drop(columns=["col1"])
df.dropna(subset=["col"])
df.fillna(0)

# Groupby
df.groupby("col").agg({"value": "sum"})
df.groupby(["a", "b"]).agg(
    avg=("value", "mean"),
    cnt=("id", "count"),
)

# Merge
df1.merge(df2, on="key", how="left")
pd.concat([df1, df2], axis=0)

# Apply
df["new"] = df["col"].apply(lambda x: x * 2)
df["new"] = df.apply(lambda row: row["a"] + row["b"], axis=1)

# Time series
df["date"] = pd.to_datetime(df["date"])
df.set_index("date").resample("D").sum()
df["col"].rolling(window=7).mean()
```

### Matplotlib + Seaborn
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib OO API
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label="series")
ax.scatter(x, y)
ax.bar(categories, values)
ax.hist(data, bins=30)
ax.set_title("Title")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("plot.png", dpi=150, bbox_inches="tight")

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(...)

# Seaborn
sns.set_theme(style="whitegrid")
sns.scatterplot(data=df, x="a", y="b", hue="cat")
sns.histplot(df, x="col", bins=30)
sns.boxplot(data=df, x="cat", y="val")
sns.heatmap(corr, annot=True, cmap="coolwarm")
sns.pairplot(df, hue="target")
```

## Scikit-learn

```python
# Imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, mean_squared_error

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

# ColumnTransformer
preproc = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

# Train
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
y_proba = pipe.predict_proba(X_test)[:, 1]

# Evaluate
accuracy_score(y_test, y_pred)
classification_report(y_test, y_pred)
mean_squared_error(y_test, y_pred, squared=False)  # RMSE

# Cross-validation
scores = cross_val_score(pipe, X, y, cv=5, scoring="f1")

# GridSearch
gs = GridSearchCV(pipe, param_grid={"model__C": [0.1, 1, 10]}, cv=5)
gs.fit(X_train, y_train)
gs.best_params_, gs.best_score_

# Save/Load
import joblib
joblib.dump(pipe, "model.joblib")
pipe = joblib.load("model.joblib")
```

## PyTorch

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Device
device = "cuda" if torch.cuda.is_available() else (
    "mps" if torch.backends.mps.is_available() else "cpu"
)

# Tensor
x = torch.tensor([1.0, 2.0, 3.0])
x = torch.randn(3, 4)
x = torch.zeros(3, 4)
x = x.to(device)
x.requires_grad_(True)

# Model
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

model = Net().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Training loop
for epoch in range(epochs):
    model.train()
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
    
    # Eval
    model.eval()
    with torch.no_grad():
        for X, y in val_loader:
            # ...

# Save/Load
torch.save(model.state_dict(), "model.pt")
model.load_state_dict(torch.load("model.pt"))
```

## Docker

```dockerfile
# Multi-stage Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/deps

FROM python:3.11-slim
COPY --from=builder /deps /usr/local/lib/python3.11/site-packages
WORKDIR /app
COPY src/ ./src/
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

```bash
# Docker commands
docker build -t my-app .
docker run -p 8000:8000 my-app
docker run --gpus all my-gpu-app
docker exec -it container_name bash
docker logs container_name -f
docker compose up -d
docker compose down -v   # volumes ham
docker system prune -a   # cleanup
```

## Kubernetes

```bash
# Basic commands
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get nodes

kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml

kubectl logs pod-name -f
kubectl exec -it pod-name -- bash
kubectl describe pod pod-name

kubectl scale deployment/my-app --replicas=5
kubectl set image deployment/my-app api=my-image:v2
kubectl rollout status deployment/my-app
kubectl rollout undo deployment/my-app

# Port forward (local testing)
kubectl port-forward svc/my-svc 8080:80

# Context switching
kubectl config use-context prod
kubectl config get-contexts
```

## MLflow

```python
import mlflow

# Setup
mlflow.set_tracking_uri("sqlite:///mlruns.db")
mlflow.set_experiment("my-experiment")

# Auto-logging (easiest)
mlflow.sklearn.autolog()
# mlflow.pytorch.autolog()
# mlflow.xgboost.autolog()

# Manual
with mlflow.start_run(run_name="my-run"):
    mlflow.log_params({"lr": 0.01, "epochs": 10})
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_metrics({"f1": 0.85, "auc": 0.91}, step=epoch)
    mlflow.log_artifact("/tmp/plot.png")
    mlflow.set_tag("git_commit", "abc123")
    
    mlflow.sklearn.log_model(model, "model", registered_model_name="my_model")

# Load
model = mlflow.sklearn.load_model("models:/my_model/Production")

# Registry
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="my_model", version=3, stage="Production",
)
```

## DVC

```bash
# Setup
dvc init
dvc remote add -d myremote s3://bucket/path

# Versioning
dvc add data/file.csv
git add data/file.csv.dvc data/.gitignore
git commit -m "Add data"
dvc push

# Pull (boshqa kompyuterda)
dvc pull

# Pipeline
dvc repro                    # full pipeline
dvc repro train              # specific stage
dvc metrics show
dvc metrics diff main
dvc plots show
dvc plots diff main

# Experiments
dvc exp run --set-param train.lr=0.01
dvc exp show
dvc exp apply <exp-name>
```

## FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.model = load_model()
    yield
    # Shutdown

app = FastAPI(title="My API", version="1.0", lifespan=lifespan)

class Input(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    value: int = Field(..., ge=0, le=100)

class Output(BaseModel):
    result: str
    confidence: float

@app.post("/predict", response_model=Output)
async def predict(data: Input):
    if not data.text:
        raise HTTPException(400, "Empty text")
    # ...
    return Output(result="ok", confidence=0.95)

@app.get("/health")
def health():
    return {"status": "ok"}

# Streaming (SSE)
@app.post("/stream")
async def stream():
    async def generator():
        for i in range(10):
            yield f"data: {i}\n\n"
            await asyncio.sleep(0.1)
    return StreamingResponse(generator(), media_type="text/event-stream")

# File upload
@app.post("/upload")
async def upload(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# Background tasks
@app.post("/task")
async def create_task(background: BackgroundTasks):
    background.add_task(my_function, arg1, arg2)
    return {"status": "queued"}
```

## Common metrics

### Classification
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve,
)
```

### Regression
```python
from sklearn.metrics import (
    mean_squared_error,        # squared=True (MSE), False (RMSE)
    mean_absolute_error,        # MAE
    r2_score,                   # R²
    mean_absolute_percentage_error,  # MAPE
)
```

## Git workflow

```bash
# Daily
git status
git pull origin main
git checkout -b feature/my-feature
# ... work ...
git add .
git commit -m "feat: add feature X"
git push -u origin feature/my-feature
# Create PR on GitHub

# Maintenance
git fetch --prune
git branch -d feature/old-feature
git rebase -i HEAD~5     # interactive squash
git stash pop
git log --oneline --graph

# Undo
git reset --soft HEAD~1  # keep changes
git reset --hard HEAD~1  # discard
git revert <commit>      # safe revert
```

## Quick references

### Cron syntax
```
* * * * *
│ │ │ │ │
│ │ │ │ └── day of week (0-7, 0/7 = Sunday)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)

@daily   = 0 0 * * *
@hourly  = 0 * * * *
@weekly  = 0 0 * * 0
0 3 * * 1 = Every Monday at 03:00
*/5 * * * * = Every 5 minutes
```

### HTTP status codes
```
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

[Asosiy bo'limga qaytish](./README.md).
