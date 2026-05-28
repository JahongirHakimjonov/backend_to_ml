# DVC — Data Versioning

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Data versioning nima uchun kerakligini bilasiz
- DVC'ni Git bilan birga ishlatishni bilasiz
- DVC pipeline yarata olasiz (`dvc.yaml`)
- Remote storage (S3, GCS) bilan ulashasiz
- DVC alternatives bilan tanish bo'lasiz (LakeFS, Pachyderm)

## 📖 Nimani o'rganish kerak

- **DVC asoslari** — `dvc init`, `dvc add`, `dvc push`, `dvc pull`
- **Remote storage** — S3, GCS, Azure, SSH
- **DVC pipelines** — `dvc.yaml`, stages
- **`dvc.lock`** — reproducibility
- **`dvc repro`** — pipeline avtomatik qayta ishga tushirish
- **DVC + MLflow** integratsiyasi
- **DVC + CI/CD**

## 📦 Kutubxonalar

```bash
pip install dvc
pip install "dvc[s3]"       # S3 uchun
pip install "dvc[gs]"       # GCS uchun
pip install "dvc[azure]"    # Azure uchun
```

## 🧠 Nima uchun DVC?

### Muammo
Git katta fayllar (datasets, modellar) bilan ishlay olmaydi:
- `git push` 100GB CSV — yo'q
- `git diff` binary file'larda foydasiz
- Repository tezda kattalashadi

### Yechim — DVC
```
Git tracks:        small files (code, configs, .dvc files)
DVC tracks:        large files (data, models, embeddings)
Storage:           S3, GCS, local NAS, SSH
```

```
my_project/
├── .git/                       # code versioning
├── .dvc/                       # DVC config
├── data/
│   └── train.csv               # .gitignore'da
├── data/train.csv.dvc          # ← bu kichik fayl Git'da
├── model.pkl                   # .gitignore'da
├── model.pkl.dvc               # ← bu kichik fayl Git'da
└── dvc.yaml                    # pipeline definition
```

## 💻 Kod misollari

### Initial setup

```bash
# 1. Loyihani init
cd my_project
git init
dvc init
git commit -m "Initialize DVC"

# 2. Remote storage qo'shish (S3 misol)
dvc remote add -d s3remote s3://my-bucket/dvc-storage
dvc remote modify s3remote endpointurl https://s3.amazonaws.com
dvc remote modify s3remote access_key_id "$AWS_ACCESS_KEY_ID"
dvc remote modify s3remote secret_access_key "$AWS_SECRET_ACCESS_KEY"

# yoki local storage (testing uchun)
dvc remote add -d localremote /Users/me/dvc-storage

# Konfiguratsiyani commit qilish
git add .dvc/config
git commit -m "Configure DVC remote"
```

### Data versioning

```bash
# 1. Data faylni DVC'ga qo'shish
dvc add data/train.csv

# Bu nima qiladi:
# - data/train.csv ni .dvc/cache ga ko'chiradi
# - data/train.csv.dvc yaratadi (kichik metadata fayl)
# - .gitignore ga data/train.csv qo'shadi

# 2. Git'ga commit
git add data/train.csv.dvc data/.gitignore
git commit -m "Add training data v1"

# 3. Remote'ga push
dvc push

# 4. O'zgartirishlar
# (data/train.csv ni o'zgartirsangiz)
dvc add data/train.csv
git add data/train.csv.dvc
git commit -m "Update training data to v2"
dvc push

# 5. Eski versiyaga qaytish (rollback)
git checkout HEAD~1 data/train.csv.dvc
dvc pull
```

### Boshqa kompyuterda (yoki CI'da)

```bash
git clone https://github.com/me/my_project.git
cd my_project
dvc pull         # remote storage'dan data yuklash
```

### DVC Pipeline — `dvc.yaml`

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python src/data/make_dataset.py
    deps:
      - src/data/make_dataset.py
      - data/raw/data.csv
    outs:
      - data/processed/train.csv
      - data/processed/test.csv
    params:
      - prepare.test_size
      - prepare.random_state

  features:
    cmd: python src/features/build_features.py
    deps:
      - src/features/build_features.py
      - data/processed/train.csv
    outs:
      - data/features/train.parquet
    params:
      - features.feature_set

  train:
    cmd: python src/models/train.py
    deps:
      - src/models/train.py
      - data/features/train.parquet
    outs:
      - models/model.pkl
    metrics:
      - metrics/train_metrics.json:
          cache: false
    plots:
      - plots/learning_curve.png:
          cache: false
    params:
      - train.n_estimators
      - train.max_depth
      - train.learning_rate
```

### `params.yaml` — hyperparameters

```yaml
# params.yaml
prepare:
  test_size: 0.2
  random_state: 42

features:
  feature_set: "v2"

train:
  n_estimators: 200
  max_depth: 10
  learning_rate: 0.1
```

### Pipeline ishga tushirish

```bash
# Pipeline'ni reproduce qilish
dvc repro

# DVC sezgir — faqat o'zgargan stage'lar qayta ishlaydi!
# Masalan: faqat params.yaml o'zgartirilsa → faqat train stage ishga tushadi

# Force re-run
dvc repro -f

# Specific stage
dvc repro train

# Metrics ko'rish
dvc metrics show

# Plots ko'rish (HTML report)
dvc plots show
```

### DVC + Git workflow

```bash
# 1. Experiment
git checkout -b experiment-1
# (params.yaml o'zgartirish)
dvc repro
dvc push

# 2. Metrics solishtirish
dvc metrics diff main
# Output:
# Path                            Metric    main    workspace    change
# metrics/train_metrics.json      accuracy  0.85    0.89         0.04

# 3. Yaxshi bo'lsa — merge
git add params.yaml dvc.lock metrics/
git commit -m "Improved accuracy to 89%"
git checkout main
git merge experiment-1
dvc push
```

### Experiments (DVC 2.0+)

```bash
# Quick experiments (commit'siz)
dvc exp run --set-param train.n_estimators=500
dvc exp run --set-param train.n_estimators=1000
dvc exp run --set-param train.max_depth=20

# Solishtirish
dvc exp show

# Eng yaxshisini commit
dvc exp apply <exp-name>
git add .
git commit -m "Best params"
```

### Python API

```python
import dvc.api

# DVC tracked faylni o'qish
with dvc.api.open("data/processed/train.csv", repo=".") as f:
    df = pd.read_csv(f)

# Yoki URL bilan (remote'dan)
url = dvc.api.get_url(
    path="data/processed/train.csv",
    repo="https://github.com/me/my_project.git",
)
df = pd.read_csv(url)

# Params
import yaml
params = yaml.safe_load(open("params.yaml"))
n_estimators = params["train"]["n_estimators"]
```

### Metrics tracking (DVC + MLflow integration)

```python
# src/models/train.py
import json
import mlflow
from sklearn.ensemble import RandomForestClassifier

# DVC params
params = yaml.safe_load(open("params.yaml"))["train"]

mlflow.set_experiment("dvc_pipeline")
with mlflow.start_run():
    mlflow.log_params(params)
    
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    metrics = {
        "accuracy": accuracy_score(y_test, model.predict(X_test)),
        "f1": f1_score(y_test, model.predict(X_test)),
    }
    
    mlflow.log_metrics(metrics)
    
    # MLflow log
    mlflow.sklearn.log_model(model, "model")
    
    # DVC metrics file
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/train_metrics.json", "w") as f:
        json.dump(metrics, f)
```

## 🔌 Backend integratsiyasi

### CI/CD: GitHub Actions + DVC

```yaml
# .github/workflows/dvc-train.yml
name: Train Model

on:
  push:
    paths:
      - "src/**"
      - "data/**.dvc"
      - "params.yaml"

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Configure DVC + AWS
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          dvc remote modify s3remote access_key_id "$AWS_ACCESS_KEY_ID"
          dvc remote modify s3remote secret_access_key "$AWS_SECRET_ACCESS_KEY"
      
      - name: Pull data
        run: dvc pull
      
      - name: Run pipeline
        run: dvc repro
      
      - name: Push artifacts
        run: dvc push
      
      - name: Comment metrics on PR
        if: github.event_name == 'pull_request'
        uses: iterative/cml-action@v1
        run: |
          dvc metrics diff main >> report.md
          cml comment create report.md
```

### Production data pipeline

```python
# scheduled retrain.py
import subprocess
from datetime import datetime

def retrain_pipeline():
    # 1. Pull latest data
    subprocess.run(["dvc", "pull", "data/raw/data.csv.dvc"], check=True)
    
    # 2. Update data (new day's data)
    update_raw_data()
    
    # 3. Track new version
    subprocess.run(["dvc", "add", "data/raw/data.csv"], check=True)
    
    # 4. Reproduce pipeline (auto train if changes)
    subprocess.run(["dvc", "repro"], check=True)
    
    # 5. Check metrics
    with open("metrics/train_metrics.json") as f:
        metrics = json.load(f)
    
    # 6. If improved, push + register
    if metrics["accuracy"] > THRESHOLD:
        subprocess.run(["dvc", "push"], check=True)
        subprocess.run(["git", "commit", "-am", f"Auto-retrain {datetime.now()}"], check=True)
        register_model_in_mlflow()
```

## 📚 Resurslar

- **DVC docs** — [dvc.org/doc](https://dvc.org/doc)
- **DVC tutorials** — [dvc.org/doc/start](https://dvc.org/doc/start)
- **CML (Continuous Machine Learning)** — DVC team CI/CD: [cml.dev](https://cml.dev/)
- **"DVC: A New Tool for Versioning Data"** — Towards Data Science
- **Alternatives**:
  - **LakeFS** — [lakefs.io](https://lakefs.io/) — Git for data lakes
  - **Pachyderm** — Kubernetes-native data versioning
  - **lakeFS** — data lake versioning

## 🏋️ Mashqlar

### 🟢 Easy
1. `dvc init` + `dvc add` bilan bitta CSV fayl uchun versioning.
2. Local DVC remote setup.
3. 2 ta versiya yarating, eski versiyaga qaytish.

### 🟡 Medium
1. **Full pipeline**: `prepare → train → evaluate` stage'lari `dvc.yaml`'da.
2. **DVC + MLflow**: ikkalasini birga ishlatish.
3. **DVC experiments**: 5 ta turli hyperparam experiment.

### 🔴 Hard
1. **Production DVC + S3**: AWS S3 yoki MinIO bilan, GitHub Actions CI/CD.
2. **Multi-stage pipeline**: 5+ stage, parametrized, plots, metrics.
3. **Distributed**: katta dataset (100GB+) bilan ishlash strategiyalari.

## 🚀 Capstone

`notebooks/month-06/03_dvc.ipynb` + `dvc.yaml` faylida:
- ML loyiha + DVC + MLflow + GitHub Actions
- Pipeline: prepare → features → train → evaluate
- Metrics, plots tracking
- S3 (yoki MinIO) remote

## ✅ Tekshirish ro'yxati

- [ ] DVC nima uchun kerakligini bilaman
- [ ] `dvc add`, `dvc push`, `dvc pull` ishlataman
- [ ] Remote storage (S3 yoki shunga o'xshash) setup qilaman
- [ ] `dvc.yaml` pipeline yozaman
- [ ] `dvc repro` orqali avtomatik retraining
- [ ] DVC + MLflow integratsiya
- [ ] GitHub Actions'da DVC pipeline
- [ ] Alternatives (LakeFS) haqida tushuncha

[FastAPI + ML Serving](./04-fastapi-ml-serving.md) ga o'tamiz — sizning kuchli tomoningiz.
