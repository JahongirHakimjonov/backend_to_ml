# FastAPI + ML Serving

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- ML modellarni production'a olib chiqishning to'liq picture'sini bilasiz
- FastAPI + custom server, BentoML, TorchServe, Triton farqlarini bilasiz
- Async va batching bilan throughput'ni 10x oshirasiz
- ONNX, quantization bilan latency'ni kamaytirasiz
- Production patterns: lifecycle management, health checks, graceful shutdown

## 📖 Nimani o'rganish kerak

- **Serving frameworks** — FastAPI, BentoML, TorchServe, TF Serving, Triton, Ray Serve, vLLM
- **Inference optimization** — ONNX, quantization, batching
- **Async patterns** — async endpoints, background tasks
- **Lifecycle management** — startup, shutdown, model loading
- **Health checks** — readiness, liveness probes
- **Request validation** — Pydantic schemas
- **Versioning** — A/B testing, shadow deployment
- **Streaming** — SSE, WebSocket for LLM
- **GPU serving** — multi-GPU, batch optimization

## 📦 Kutubxonalar

```bash
pip install fastapi uvicorn[standard] gunicorn
pip install onnx onnxruntime onnxruntime-gpu  # ONNX
pip install bentoml                            # alternative server
pip install ray[serve]                         # distributed serving
```

## 🧠 Serving frameworks comparison

| | **FastAPI custom** | **BentoML** | **TorchServe** | **Triton** | **Ray Serve** | **vLLM** |
|---|-------------------|-------------|----------------|------------|---------------|----------|
| **Use case** | Universal | Python ML | PyTorch | GPU prod | Distributed | LLM only |
| **Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Batching** | Manual | ✅ Built-in | ✅ | ✅ | ✅ | ✅ |
| **Multi-model** | Manual | ✅ | ✅ | ✅ | ✅ | ❌ |
| **GPU** | Manual | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| **Production** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Tavsiyalar:**
- Klassik ML (sklearn, XGBoost) → **FastAPI + custom**
- Modern Python ML stack → **BentoML**
- PyTorch production → **TorchServe** yoki **Triton**
- LLM inference → **vLLM** (eng tez)
- Distributed → **Ray Serve**

## 💻 Kod misollari

### Production FastAPI ML service template

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import joblib
import numpy as np
import logging
import time
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

logger = logging.getLogger(__name__)

# Metrics
prediction_counter = Counter("ml_predictions_total", "Total predictions", ["model_version", "status"])
prediction_duration = Histogram("ml_prediction_duration_seconds", "Prediction duration")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading model...")
    app.state.model = joblib.load("models/model_v1.joblib")
    app.state.model_version = "v1.2.3"
    app.state.warmup()  # ba'zi modellar lazy init
    logger.info(f"Model {app.state.model_version} loaded")
    yield
    # Shutdown
    logger.info("Shutting down")

app = FastAPI(
    title="ML Prediction Service",
    version="1.0.0",
    lifespan=lifespan,
)

# Pydantic schemas
class Features(BaseModel):
    age: int = Field(..., ge=0, le=120)
    income: float = Field(..., gt=0)
    tenure_months: int = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {"age": 35, "income": 50000, "tenure_months": 24}
        }

class Prediction(BaseModel):
    prediction: int
    probability: float
    model_version: str
    latency_ms: float

# Health checks
@app.get("/health/live")
def liveness():
    """K8s liveness probe — server ishlayaptimi?"""
    return {"status": "alive"}

@app.get("/health/ready")
def readiness():
    """K8s readiness probe — request qabul qila olamizmi?"""
    if not hasattr(app.state, "model"):
        raise HTTPException(503, "Model not loaded")
    return {"status": "ready", "model_version": app.state.model_version}

# Metrics
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

# Main endpoint
@app.post("/predict", response_model=Prediction)
async def predict(features: Features):
    start = time.perf_counter()
    
    try:
        X = np.array([[features.age, features.income, features.tenure_months]])
        prediction = int(app.state.model.predict(X)[0])
        probability = float(app.state.model.predict_proba(X)[0].max())
        
        latency = (time.perf_counter() - start) * 1000
        
        prediction_counter.labels(model_version=app.state.model_version, status="success").inc()
        prediction_duration.observe(latency / 1000)
        
        logger.info(
            "Prediction successful",
            extra={
                "features": features.dict(),
                "prediction": prediction,
                "probability": probability,
                "latency_ms": latency,
                "model_version": app.state.model_version,
            },
        )
        
        return Prediction(
            prediction=prediction,
            probability=probability,
            model_version=app.state.model_version,
            latency_ms=latency,
        )
    
    except Exception as e:
        prediction_counter.labels(model_version=app.state.model_version, status="error").inc()
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(500, "Internal prediction error")

# Batch endpoint
class BatchInput(BaseModel):
    items: list[Features]

@app.post("/predict/batch")
async def predict_batch(batch: BatchInput):
    X = np.array([[f.age, f.income, f.tenure_months] for f in batch.items])
    predictions = app.state.model.predict(X)
    probabilities = app.state.model.predict_proba(X)
    
    return {
        "predictions": [
            {"prediction": int(p), "probability": float(prob.max())}
            for p, prob in zip(predictions, probabilities)
        ]
    }
```

### Async batching middleware

```python
import asyncio
from collections import defaultdict

class BatchingMiddleware:
    """Bir nechta request'ni birlashtirib batch inference."""
    
    def __init__(self, max_batch_size: int = 32, max_wait_ms: int = 50):
        self.queue = []
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.lock = asyncio.Lock()
    
    async def predict(self, x: np.ndarray) -> tuple:
        future = asyncio.Future()
        
        async with self.lock:
            self.queue.append((x, future))
            
            if len(self.queue) >= self.max_batch_size:
                await self._flush()
        
        # Timeout
        try:
            return await asyncio.wait_for(future, timeout=self.max_wait_ms / 1000)
        except asyncio.TimeoutError:
            async with self.lock:
                if not future.done():
                    await self._flush()
            return await future
    
    async def _flush(self):
        if not self.queue:
            return
        
        batch = self.queue
        self.queue = []
        
        X_batch = np.vstack([x for x, _ in batch])
        predictions = self.model.predict(X_batch)
        probabilities = self.model.predict_proba(X_batch)
        
        for (_, future), pred, prob in zip(batch, predictions, probabilities):
            future.set_result((int(pred), float(prob.max())))
```

### ONNX export va serving

```python
# Export PyTorch → ONNX
import torch

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    opset_version=17,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
)

# Inference (ONNX Runtime — tez!)
import onnxruntime as ort

# CPU
sess = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])

# GPU (CUDA)
sess = ort.InferenceSession("model.onnx", providers=["CUDAExecutionProvider"])

# Optimize for production
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.intra_op_num_threads = 4
sess = ort.InferenceSession("model.onnx", sess_options, providers=["CPUExecutionProvider"])

# Predict
output = sess.run(None, {"input": input_array.astype(np.float32)})[0]
```

### Quantization (kichikroq + tezroq)

```python
# Dynamic quantization (PyTorch)
import torch.quantization

model.eval()
model_int8 = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear},        # qaysi layer'lar
    dtype=torch.qint8,
)
# 4x kichikroq, 2-3x tezroq, accuracy 1-2% pasayadi
```

### BentoML — Python-friendly framework

```python
# service.py
import bentoml
from bentoml.io import JSON
import numpy as np

# Save model
@bentoml.sklearn.save_model("churn_predictor", sklearn_model)

# Service
service = bentoml.Service("churn_service")

runner = bentoml.sklearn.get("churn_predictor:latest").to_runner()
service.add_runner(runner)

@service.api(input=JSON(), output=JSON())
async def predict(input_data: dict) -> dict:
    X = np.array([[input_data["age"], input_data["income"], input_data["tenure"]]])
    pred = await runner.predict.async_run(X)
    return {"prediction": int(pred[0])}
```

```bash
# Run
bentoml serve service:service --reload

# Docker container build
bentoml containerize churn_service:latest
docker run -p 3000:3000 churn_service:latest
```

### TorchServe — PyTorch production

```bash
# Model'ni archive qilish
torch-model-archiver \
    --model-name churn_pytorch \
    --version 1.0 \
    --serialized-file model.pt \
    --handler my_handler.py

# Start serving
torchserve --start --model-store ./model_store --models churn=churn_pytorch.mar

# REST API
curl -X POST http://localhost:8080/predictions/churn \
    -d '{"age": 35, "income": 50000}'
```

### Streaming endpoint (LLM-style)

```python
from fastapi.responses import StreamingResponse

@app.post("/generate/stream")
async def generate_stream(prompt: str):
    async def event_stream():
        for token in llm.stream(prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Gunicorn production setup

```python
# gunicorn_conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
keepalive = 5
timeout = 30

# Memory optimization
max_requests = 1000
max_requests_jitter = 100
preload_app = True  # Model bir marta yuklanadi (shared memory)
```

```bash
gunicorn -c gunicorn_conf.py main:app
```

## 🔌 Backend integratsiyasi

### Multi-model serving

```python
@asynccontextmanager
async def lifespan(app):
    # Several models with router
    app.state.models = {
        "v1": joblib.load("models/v1.joblib"),
        "v2": joblib.load("models/v2.joblib"),
        "experimental": joblib.load("models/experimental.joblib"),
    }
    yield

@app.post("/predict/{version}")
def predict(version: str, features: Features):
    if version not in app.state.models:
        raise HTTPException(404, f"Model {version} not found")
    model = app.state.models[version]
    # ... predict
```

### A/B test infrastructure

```python
import random

@app.post("/predict")
def predict(features: Features, request: Request):
    # 90% production, 10% experimental
    if random.random() < 0.1:
        version = "experimental"
    else:
        version = "v2"
    
    model = app.state.models[version]
    prediction = model.predict(...)
    
    # Log assignment for analysis
    await log_ab_assignment(
        user_id=request.headers.get("X-User-ID"),
        version=version,
        prediction=prediction,
    )
    
    return {"prediction": prediction, "model_version": version}
```

### Shadow deployment (yangi modelni real traffic'da sinash)

```python
@app.post("/predict")
async def predict(features: Features, background: BackgroundTasks):
    # Production prediction
    production_pred = app.state.production_model.predict(...)
    
    # Shadow prediction (response'ga ta'sir qilmaydi)
    background.add_task(shadow_predict, features, production_pred)
    
    return {"prediction": production_pred}

async def shadow_predict(features, production_pred):
    shadow_pred = app.state.shadow_model.predict(...)
    
    # Compare
    if shadow_pred != production_pred:
        await log_disagreement(features, production_pred, shadow_pred)
```

## 📚 Resurslar

- **FastAPI docs** — [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **BentoML docs** — [docs.bentoml.com](https://docs.bentoml.com/)
- **TorchServe docs** — [pytorch.org/serve](https://pytorch.org/serve/)
- **NVIDIA Triton** — [github.com/triton-inference-server/server](https://github.com/triton-inference-server/server)
- **Ray Serve docs** — [docs.ray.io/en/latest/serve](https://docs.ray.io/en/latest/serve/)
- **"Building Machine Learning Pipelines"** — Hapke & Nelson

## 🏋️ Mashqlar

### 🟢 Easy
1. Sklearn modelni FastAPI'ga olib chiqing.
2. Pydantic validation bilan input check.
3. Health checks (`/health/live`, `/health/ready`).

### 🟡 Medium
1. **Batching**: async batching middleware bilan throughput o'lchang.
2. **ONNX export**: PyTorch → ONNX → ONNX Runtime, latency solishtirish.
3. **A/B test**: 2 model bir vaqtda, traffic split, Postgres log.

### 🔴 Hard
1. **Production-grade service**: FastAPI + ONNX + batching + Prometheus + Sentry + Docker + tests.
2. **TorchServe deployment**: PyTorch model TorchServe'da, custom handler.
3. **BentoML migration**: mavjud FastAPI servisni BentoML'ga ko'chiring, farqlarni baholang.

## 🚀 Capstone

`notebooks/month-06/04_fastapi_serving.ipynb` + `src/api/main.py`:
- Oy 2/3/5 dan biror modelni production-ready FastAPI servisga aylantiring
- Batching + ONNX + Prometheus
- Load test (Locust): 100 req/s ga chiday oladigan optimization
- Docker'ga olib, Postman'da test

## ✅ Tekshirish ro'yxati

- [ ] FastAPI'da ML model serving
- [ ] Lifecycle (startup, shutdown) management
- [ ] Health checks (K8s probes)
- [ ] Prometheus metrics
- [ ] Async batching
- [ ] ONNX export va inference
- [ ] BentoML basics
- [ ] A/B test va shadow deployment patterns

[Docker va Kubernetes](./05-docker-kubernetes.md) ga o'tamiz.
