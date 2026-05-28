# CI/CD for ML

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- ML CI/CD ning klassik backend CI/CD'dan farqini bilasiz
- Code testing, data testing, model testing'ni qila olasiz
- Continuous Training (CT) pipeline qura olasiz
- GitHub Actions, GitLab CI bilan ML deployment
- CML (Continuous Machine Learning) tool'ni ishlatishni bilasiz

## Nimani o'rganish kerak

- **CI vs CD vs CT**(Continuous Training)
- **ML-specific testing** — data, features, model
- **GitHub Actions for ML**
- **GitLab CI/CD pipelines**
- **CML (Continuous Machine Learning)** — DVC team'ning toolu
- **Deployment strategies** — blue-green, canary, shadow
- **Rollback mechanisms**
- **Approval workflows** — manual review oldidan production

## ML CI/CD ning specialligi

### Klassik DevOps CI/CD
```
Code change
  → Unit tests
  → Build Docker
  → Deploy
```

### ML CI/CD
```
Code change          OR      Data change
  ↓                            ↓
  Unit tests              Data validation
  ↓                            ↓
  Train model             Retrain model
  ↓                            ↓
  Test model              Test model
  ↓                            ↓
  Deploy + Monitor        Deploy + Monitor
```

### Uchta darajadagi testing

#### 1. Code Tests (klassik)
```python
def test_preprocess_function():
    assert preprocess("Hello") == "hello"

def test_feature_engineering():
    df = pd.DataFrame({"price": [100, 200]})
    result = add_features(df)
    assert "price_log" in result.columns
```

#### 2. Data Tests
```python
def test_data_schema():
    df = pd.read_csv("data/train.csv")
    assert df.shape[1] == 20
    assert df["age"].dtype == "int64"
    assert df["age"].min() >= 0

def test_data_quality():
    df = pd.read_csv("data/train.csv")
    assert df.isna().sum().sum() / len(df) < 0.05  # <5% missing
    assert df["target"].value_counts(normalize=True).max() < 0.95  # not too imbalanced
```

#### 3. Model Tests
```python
def test_model_performance():
    """Yangi model baseline'dan yaxshi bo'lsin."""
    model = train_model(X_train, y_train)
    accuracy = evaluate(model, X_test, y_test)
    assert accuracy > BASELINE_ACCURACY  # 0.85

def test_model_invariance():
    """Aniq inputlarda model determinist bo'lishi kerak."""
    pred1 = model.predict(X_sample)
    pred2 = model.predict(X_sample)
    np.testing.assert_array_equal(pred1, pred2)

def test_model_perturbation():
    """Kichik input o'zgarishi → kichik output o'zgarishi."""
    pred_original = model.predict(X_sample)
    pred_perturbed = model.predict(X_sample + np.random.normal(0, 0.01, X_sample.shape))
    diff = np.abs(pred_original - pred_perturbed).mean()
    assert diff < 0.1  # ish

def test_model_bias():
    """Modelda fairness — turli demografik guruhlar uchun"""
    male_acc = evaluate(model, X[gender == "M"], y[gender == "M"])
    female_acc = evaluate(model, X[gender == "F"], y[gender == "F"])
    assert abs(male_acc - female_acc) < 0.05  # 5% farqdan kam
```

## Kod misollari

### GitHub Actions — to'liq ML pipeline

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"

jobs:
  # 1. Code quality
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff mypy
      - run: ruff check src/ tests/
      - run: mypy src/
  
  # 2. Unit tests
  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest tests/ -v --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
  
  # 3. Data + Model tests (data needed)
  ml-tests:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt
      
      - name: Pull data via DVC
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          pip install dvc[s3]
          dvc pull
      
      - run: pytest tests/data/ tests/model/ -v
  
  # 4. Build Docker
  build:
    runs-on: ubuntu-latest
    needs: ml-tests
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker registry
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            myregistry/ml-api:${{ github.sha }}
            myregistry/ml-api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
  
  # 5. Deploy to staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > ~/.kube/config
      
      - name: Deploy
        run: |
          kubectl set image deployment/ml-api api=myregistry/ml-api:${{ github.sha }} -n staging
          kubectl rollout status deployment/ml-api -n staging --timeout=5m
  
  # 6. Integration tests on staging
  integration-tests:
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest httpx
      - name: Run integration tests
        env:
          API_URL: https://ml-api-staging.example.com
        run: pytest tests/integration/ -v
  
  # 7. Deploy to production (manual approval)
  deploy-production:
    runs-on: ubuntu-latest
    needs: integration-tests
    environment: production  # GitHub'da manual approval set qilish
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > ~/.kube/config
      
      - name: Canary deploy (10% traffic)
        run: |
          kubectl set image deployment/ml-api-canary api=myregistry/ml-api:${{ github.sha }} -n production
          # Monitoring 10 daqiqa
          sleep 600
      
      - name: Full rollout
        run: |
          kubectl set image deployment/ml-api api=myregistry/ml-api:${{ github.sha }} -n production
          kubectl rollout status deployment/ml-api -n production --timeout=10m
```

### CML — Continuous ML

```yaml
# .github/workflows/cml.yml
name: CML Report

on: [pull_request]

jobs:
  train-and-report:
    runs-on: ubuntu-latest
    container: ghcr.io/iterative/cml:0-dvc2-base1
    steps:
      - uses: actions/checkout@v4
      
      - name: Train model
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          pip install -r requirements.txt
          dvc pull
          dvc repro
      
      - name: Create CML report
        env:
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Metrics comparison
          echo "## Model Metrics" >> report.md
          echo "" >> report.md
          dvc metrics diff main >> report.md
          
          # Plots
          dvc plots diff main --show-vega target > plot.json
          cml publish plot.json --md >> report.md
          
          # Post comment to PR
          cml comment create report.md
```

PR'ga avtomatik ko'rinadi:
```
## Model Metrics

| Metric    | Old    | New    | Change |
|-----------|--------|--------|--------|
| accuracy  | 0.85   | 0.89   | +0.04  |
| f1        | 0.82   | 0.87   | +0.05  |

[Confusion Matrix Plot]
```

### Deployment strategies

#### 1. Blue-Green deployment
```yaml
# blue (current production) ishlamoqda
# green (new version) tayyorlanadi
# Switch — load balancer routing'ni o'zgartirish

apiVersion: v1
kind: Service
metadata:
  name: ml-api
spec:
  selector:
    app: ml-api
    color: blue   # green'ga o'zgartirsangiz — instant switch
```

#### 2. Canary deployment
```yaml
# v1 — 90% traffic
# v2 — 10% traffic
# Sekin-asta v2 traffic'ni 100%'ga oshirish

# Istio yoki Nginx ingress bilan
nginx.ingress.kubernetes.io/canary: "true"
nginx.ingress.kubernetes.io/canary-weight: "10"
```

#### 3. Shadow deployment
```python
# Production prediction qaytariladi
# Lekin yangi model ham ishlaydi (response'siz)
# Comparison logged

@app.post("/predict")
async def predict(features: Features, background: BackgroundTasks):
    prod_pred = production_model.predict(features)
    
    # Shadow (async, foydalanuvchiga ko'rinmaydi)
    background.add_task(shadow_predict, features, prod_pred)
    
    return {"prediction": prod_pred}
```

### Continuous Training (CT)

```python
# scheduled retrain.py (Airflow yoki cron)
def continuous_training_pipeline():
    # 1. Check drift
    drift_score = check_drift(reference_data, recent_production_data)
    
    # 2. Decide: retrain kerakmi?
    if drift_score < 0.1 and current_accuracy > 0.85:
        log.info("No retraining needed")
        return
    
    # 3. Trigger retraining
    log.info("Drift detected, starting retraining")
    
    # 4. DVC + MLflow pipeline
    subprocess.run(["dvc", "repro"], check=True)
    
    # 5. Validate new model
    new_metrics = load_latest_metrics()
    old_metrics = load_production_metrics()
    
    if new_metrics["accuracy"] < old_metrics["accuracy"]:
        log.warning("New model worse than current. Skipping deployment.")
        return
    
    # 6. Register in MLflow
    register_model_in_mlflow()
    
    # 7. Trigger CI/CD
    subprocess.run(["gh", "workflow", "run", "deploy.yml"], check=True)
```

### Testing patterns

```python
# tests/test_model.py
import pytest
import joblib
import numpy as np

@pytest.fixture(scope="module")
def model():
    return joblib.load("models/model.pkl")

def test_model_accuracy(model):
    """Production threshold check."""
    X_test, y_test = load_test_data()
    accuracy = model.score(X_test, y_test)
    assert accuracy >= 0.85, f"Accuracy {accuracy} below threshold 0.85"

def test_model_latency(model, benchmark):
    """Pytest-benchmark."""
    X = np.random.randn(1, 10)
    result = benchmark(model.predict, X)
    # Auto-fails if too slow

def test_model_handles_missing(model):
    """Edge case — missing values."""
    X = np.array([[np.nan, 1.0, 2.0]])
    pred = model.predict(X)
    assert not np.isnan(pred[0])

def test_model_handles_extreme_values(model):
    """Edge case — extreme inputs."""
    X = np.array([[1e9, -1e9, 0]])
    pred = model.predict(X)
    assert pred[0] in [0, 1]  # valid output

@pytest.mark.parametrize("noise", [0.01, 0.05, 0.1])
def test_model_robustness_to_noise(model, noise):
    """Kichik noise → kichik output o'zgarishi."""
    X_original = np.random.randn(100, 10)
    pred_original = model.predict(X_original)
    
    X_noisy = X_original + np.random.normal(0, noise, X_original.shape)
    pred_noisy = model.predict(X_noisy)
    
    diff = (pred_original != pred_noisy).mean()
    assert diff < noise * 5  # noise'ga proportsional o'zgarish
```

## Backend integratsiyasi

### Pre-deployment validation gate

```yaml
# .github/workflows/validate-model.yml
name: Validate New Model

on:
  workflow_call:
    inputs:
      model_version:
        required: true
        type: string

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Load model from MLflow
        run: |
          python scripts/load_model.py --version ${{ inputs.model_version }}
      
      - name: Run validation tests
        run: |
          pytest tests/model_validation/ -v --model-version=${{ inputs.model_version }}
      
      - name: Check business metrics
        run: |
          python scripts/business_validation.py
          # Bu script'da: false positive rate, revenue impact, h.k.
      
      - name: Compare with production
        run: |
          python scripts/compare_models.py \
            --new-version ${{ inputs.model_version }} \
            --prod-version $(python scripts/get_prod_version.py)
```

### Rollback workflow

```yaml
# .github/workflows/rollback.yml
name: Emergency Rollback

on:
  workflow_dispatch:
    inputs:
      target_version:
        description: "Version to rollback to"
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > ~/.kube/config
      
      - name: Rollback deployment
        run: |
          kubectl set image deployment/ml-api api=myregistry/ml-api:${{ inputs.target_version }} -n production
          kubectl rollout status deployment/ml-api -n production
      
      - name: Notify
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🚨 Production rollback to ${{ inputs.target_version }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Resurslar

- **GitHub Actions docs** — [docs.github.com/en/actions](https://docs.github.com/en/actions)
- **CML (Continuous ML)** — [cml.dev](https://cml.dev/)
- **"Continuous Delivery for Machine Learning"** — Martin Fowler
- **"ML Test Score"** — Google paper (testing rubric)
- **Great Expectations** — data testing framework
- **Pytest docs** — testing best practices

## 🏋️ Mashqlar

### 🟢 Easy
1. GitHub Actions'da pytest run qiluvchi pipeline.
2. Code quality (ruff, mypy) checks.
3. Docker build action.

### 🟡 Medium
1. **Full ML pipeline**: lint → test → train → docker → deploy (staging).
2. **CML report**: PR'ga avtomatik metrics comparison.
3. **Model validation**: accuracy, latency, robustness tests.

### 🔴 Hard
1. **Production CI/CD**: blue-green yoki canary deployment (real cloud).
2. **Continuous Training**: drift detection → auto-retrain → auto-deploy (with approval).
3. **Multi-environment**: dev/staging/prod, har biriga alohida config.

## Capstone

`.github/workflows/`:
- To'liq ML CI/CD pipeline
- Code → data → model tests
- Build → deploy → integration tests
- Production deployment manual approval bilan

## ✅ Tekshirish ro'yxati

- [ ] CI/CD ML uchun specific tomonlarini bilaman
- [ ] Code, data, model testing
- [ ] GitHub Actions ML pipeline yozaman
- [ ] CML bilan PR reports
- [ ] Deployment strategies (blue-green, canary, shadow)
- [ ] Continuous Training pipeline
- [ ] Rollback mechanism

[Airflow va Prefect](./08-airflow-prefect.md) ga o'tamiz — oxirgi bobga.
