# Airflow va Prefect

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Workflow orchestration nima va nima uchun kerakligini bilasiz
- Apache Airflow bilan ML pipeline yozasiz
- Prefect alternative bilan tanish bo'lasiz
- ML uchun maxsus DAG patternlarini bilasiz
- Scheduled retraining, ETL pipeline'lar qura olasiz

## Nimani o'rganish kerak

- **Workflow orchestration** — nima va nima uchun
- **Apache Airflow** — DAG, Operators, Tasks, Sensors
- **Airflow concepts** — XCom, Pools, Variables, Connections
- **Prefect** — modern alternative
- **Dagster** — data-aware orchestrator
- **ML pipeline patterns** — ETL, training, inference batch
- **Backfilling**va idempotency

## Kutubxonalar

```bash
# Airflow (Docker bilan tavsiya)
docker pull apache/airflow:2.10.0

# Yoki Python
pip install apache-airflow==2.10.0

# Prefect (oddiyroq)
pip install prefect
```

## Workflow orchestration nima?

### Problem
ML loyihada ko'p bog'liq task'lar:
```
1. Yangi data fetch (har kun 03:00)
2. Data validation
3. Feature engineering
4. Train model
5. Validate model
6. If good → register in MLflow
7. If great → deploy
8. Send report
```

**Qo'lda bajarish — ko'p xato. Cron'da yozish — debugging qiyin. Yechim — orchestrator.**

### Orchestrator nima beradi?
- **DAG**(Directed Acyclic Graph) — task'lar ketma-ketligi
- **Retry** — fail bo'lsa avtomatik takrorlash
- **Scheduling** — cron-like, lekin yaxshiroq
- **Monitoring** — UI'da kuzatish
- **Backfilling** — eski sanalar uchun ishga tushirish
- **Alerts** — failure'da notification

## Airflow vs Prefect vs Dagster

| | Airflow | Prefect | Dagster |
|---|---------|---------|---------|
| **Age** | 2014 (mature) | 2018 (modern) | 2019 (newest) |
| **Style** | Imperative DAG | Pythonic flow | Asset-based |
| **Setup** | Complex | Easy | Medium |
| **UI** | Good | Modern | Excellent |
| **Community** | Largest | Growing | Smaller |
| **Cloud** | Self-host / Managed | Cloud-first | Self-host / Cloud |
| **ML-specific** | General | General | Data-aware |
| **Job market** | Most demand | Growing | Growing |

**Tavsiya:**Production'da **Airflow**(industry standard), kichik loyihalar uchun **Prefect**.

## Apache Airflow

### Local Docker setup

```yaml
# docker-compose.yml
version: "3.9"

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  airflow-init:
    image: apache/airflow:2.10.0
    depends_on: [postgres]
    environment: &airflow-common-env
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__LOAD_EXAMPLES: "false"
      _AIRFLOW_DB_MIGRATE: "true"
      _AIRFLOW_WWW_USER_CREATE: "true"
      _AIRFLOW_WWW_USER_USERNAME: admin
      _AIRFLOW_WWW_USER_PASSWORD: admin
    command: version
  
  airflow-webserver:
    image: apache/airflow:2.10.0
    depends_on: [postgres, airflow-init]
    environment: *airflow-common-env
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: webserver
  
  airflow-scheduler:
    image: apache/airflow:2.10.0
    depends_on: [postgres, airflow-init]
    environment: *airflow-common-env
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: scheduler

volumes:
  postgres-data:
```

```bash
docker-compose up -d
# UI: http://localhost:8080  (admin/admin)
```

### Birinchi DAG — ML retraining

```python
# dags/retrain_model.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

default_args = {
    "owner": "ml-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["ml-alerts@company.com"],
}

dag = DAG(
    "retrain_churn_model",
    default_args=default_args,
    schedule="0 3 * * 1",  # Har dushanba 03:00
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "training"],
)

def fetch_data(**context):
    """Postgres'dan oxirgi 30 kunlik data."""
    hook = PostgresHook(postgres_conn_id="prod_db")
    df = hook.get_pandas_df(
        "SELECT * FROM customer_events WHERE date >= NOW() - INTERVAL '30 days'"
    )
    
    output_path = f"/tmp/data_{context['ds']}.csv"
    df.to_csv(output_path, index=False)
    
    # XCom — task'lar orasida data uzatish
    return output_path

def validate_data(**context):
    """Data quality check."""
    input_path = context["ti"].xcom_pull(task_ids="fetch_data")
    df = pd.read_csv(input_path)
    
    assert len(df) > 1000, "Not enough data"
    assert df.isna().sum().sum() / df.size < 0.1, "Too many missing values"
    assert df["churn"].nunique() == 2, "Target not binary"
    
    return input_path

def train_model(**context):
    """Train + validate."""
    input_path = context["ti"].xcom_pull(task_ids="validate_data")
    df = pd.read_csv(input_path)
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import mlflow
    
    X = df.drop("churn", axis=1)
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    mlflow.set_experiment("scheduled_retraining")
    with mlflow.start_run(run_name=f"retrain_{context['ds']}"):
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)
        
        accuracy = accuracy_score(y_test, model.predict(X_test))
        mlflow.log_metric("accuracy", accuracy)
        
        # Save model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="churn_model",
        )
        
        return {"accuracy": accuracy, "run_id": mlflow.active_run().info.run_id}

def decide_deployment(**context):
    """Yangi model baseline'dan yaxshimi?"""
    metrics = context["ti"].xcom_pull(task_ids="train_model")
    
    BASELINE_ACCURACY = 0.85
    
    if metrics["accuracy"] > BASELINE_ACCURACY:
        return "promote_to_production"
    else:
        return "skip_deployment"

from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator

# Tasks
fetch_task = PythonOperator(
    task_id="fetch_data",
    python_callable=fetch_data,
    dag=dag,
)

validate_task = PythonOperator(
    task_id="validate_data",
    python_callable=validate_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    dag=dag,
)

decide_task = BranchPythonOperator(
    task_id="decide_deployment",
    python_callable=decide_deployment,
    dag=dag,
)

promote_task = BashOperator(
    task_id="promote_to_production",
    bash_command="python /scripts/promote_model.py {{ ti.xcom_pull(task_ids='train_model')['run_id'] }}",
    dag=dag,
)

skip_task = EmptyOperator(
    task_id="skip_deployment",
    dag=dag,
)

# Dependencies
fetch_task >> validate_task >> train_task >> decide_task
decide_task >> [promote_task, skip_task]
```

### TaskFlow API (modern Airflow 2.x)

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule="0 3 * * 1",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml"],
)
def ml_pipeline():
    
    @task
    def fetch_data():
        df = pd.read_sql(...)
        return df.to_dict()
    
    @task
    def validate(data: dict):
        df = pd.DataFrame(data)
        assert len(df) > 1000
        return df.to_dict()
    
    @task
    def train(data: dict):
        df = pd.DataFrame(data)
        model = RandomForestClassifier()
        model.fit(...)
        return {"accuracy": 0.89, "model_path": "..."}
    
    @task
    def deploy(metrics: dict):
        if metrics["accuracy"] > 0.85:
            # Deploy
            ...
    
    # Chain
    data = fetch_data()
    validated = validate(data)
    metrics = train(validated)
    deploy(metrics)

ml_pipeline()
```

### Sensors — wait for events

```python
from airflow.sensors.filesystem import FileSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

# Wait for S3 file
wait_for_data = S3KeySensor(
    task_id="wait_for_daily_data",
    bucket_name="ml-data",
    bucket_key="daily/data_{{ ds }}.csv",
    aws_conn_id="aws_default",
    timeout=3600,
    poke_interval=60,
)
```

### Inference batch job

```python
@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
)
def daily_inference():
    
    @task
    def load_users_to_score():
        users = pd.read_sql("SELECT * FROM users WHERE active = TRUE", conn)
        return users.to_dict()
    
    @task
    def batch_predict(users: dict):
        df = pd.DataFrame(users)
        model = mlflow.sklearn.load_model("models:/churn_model/Production")
        df["churn_probability"] = model.predict_proba(df[FEATURES])[:, 1]
        return df.to_dict()
    
    @task
    def save_predictions(predictions: dict):
        df = pd.DataFrame(predictions)
        df.to_sql("daily_predictions", conn, if_exists="replace", index=False)
    
    @task
    def alert_high_risk(predictions: dict):
        df = pd.DataFrame(predictions)
        high_risk = df[df["churn_probability"] > 0.8]
        send_to_crm(high_risk)
    
    users = load_users_to_score()
    preds = batch_predict(users)
    save_predictions(preds)
    alert_high_risk(preds)

daily_inference()
```

## Prefect — modern alternative

```python
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

@task(retries=3, retry_delay_seconds=60)
def fetch_data():
    df = pd.read_sql(...)
    return df

@task
def validate_data(df):
    assert len(df) > 1000
    return df

@task
def train_model(df):
    model = RandomForestClassifier()
    model.fit(...)
    return model

@flow(name="ml-pipeline", log_prints=True)
def ml_pipeline():
    df = fetch_data()
    df = validate_data(df)
    model = train_model(df)
    return model

if __name__ == "__main__":
    # Local run
    ml_pipeline()

# Deploy with schedule
deployment = Deployment.build_from_flow(
    flow=ml_pipeline,
    name="weekly-retrain",
    schedule=CronSchedule(cron="0 3 * * 1"),
)
deployment.apply()
```

### Prefect afzalliklari (Airflow'ga nisbatan)
- **Pythonic** — DAG'lar emas, oddiy decorator'lar
- **Dynamic** — runtime'da task'lar yaratish oson
- **Modern UI** — yaxshi UX
- **Cloud-first** — Prefect Cloud bepul

## Backend integratsiyasi

### Airflow + MLflow + DVC + K8s — full pipeline

```python
@dag(schedule="@weekly", catchup=False)
def full_ml_pipeline():
    
    @task
    def dvc_pull():
        subprocess.run(["dvc", "pull"], check=True)
    
    @task
    def update_data():
        # New data from production DB
        df = pd.read_sql("SELECT ...", conn)
        df.to_csv("data/raw/new_data.csv")
        subprocess.run(["dvc", "add", "data/raw/new_data.csv"], check=True)
    
    @task
    def dvc_repro():
        result = subprocess.run(["dvc", "repro"], capture_output=True)
        return result.returncode == 0
    
    @task
    def evaluate_new_model():
        with open("metrics/train_metrics.json") as f:
            metrics = json.load(f)
        return metrics
    
    @task.branch
    def decide_deployment(metrics: dict):
        if metrics["accuracy"] > 0.85 and metrics["f1"] > 0.80:
            return "deploy_to_k8s"
        return "skip"
    
    @task
    def deploy_to_k8s():
        # MLflow'ga register
        subprocess.run(["python", "scripts/register_model.py"], check=True)
        
        # K8s deployment update
        subprocess.run([
            "kubectl", "set", "image",
            "deployment/ml-api", "api=myregistry/ml-api:latest",
        ], check=True)
    
    @task
    def skip():
        print("New model not deployed (insufficient accuracy)")
    
    pull = dvc_pull()
    update = update_data()
    repro = dvc_repro()
    metrics = evaluate_new_model()
    branch = decide_deployment(metrics)
    deploy = deploy_to_k8s()
    skip_task = skip()
    
    pull >> update >> repro >> metrics >> branch
    branch >> [deploy, skip_task]

full_ml_pipeline()
```

## Resurslar

- **Airflow docs** — [airflow.apache.org/docs](https://airflow.apache.org/docs/)
- **"Data Pipelines with Apache Airflow"** — Bas Harenslak & Julian de Ruiter
- **Astronomer Academy** — bepul Airflow kurslari
- **Prefect docs** — [docs.prefect.io](https://docs.prefect.io/)
- **Dagster docs** — [docs.dagster.io](https://docs.dagster.io/)

## 🏋️ Mashqlar

### 🟢 Easy
1. Local Airflow Docker setup, birinchi DAG.
2. Simple ETL: read CSV → transform → save Postgres.
3. Daily scheduled task with retry.

### 🟡 Medium
1. **ML retraining DAG**: weekly schedule, MLflow log, conditional deployment.
2. **Batch inference**: daily user scoring + CRM alert.
3. **Prefect alternative**: bir xil DAG'ni Prefect'da yozing.

### 🔴 Hard
1. **Full ML platform DAG**: DVC + MLflow + K8s deployment + monitoring + alerts.
2. **Multi-DAG dependencies**: training DAG'i tugasa, inference DAG'i ishga tushadi.
3. **Production setup**: Astronomer yoki MWAA (AWS) — managed Airflow.

## Capstone — Final MLOps Pipeline

`dags/full_ml_pipeline.py`:
- Weekly retraining
- DVC + MLflow + K8s
- Drift-based conditional retraining
- Slack notifications
- Rollback mechanism

## ✅ Tekshirish ro'yxati

- [ ] Workflow orchestration nima uchun kerakligini bilaman
- [ ] Airflow DAG yozaman (Operator va TaskFlow API)
- [ ] Sensors va branching
- [ ] XCom — task'lar orasida data
- [ ] Schedules va backfilling
- [ ] Prefect alternative bilan tanish
- [ ] ML-specific DAG patternlari
- [ ] Production deployment (managed yoki self-hosted)

 **Oy 6 tugadi!**

**Tabriklayman!**Siz endi to'liq **ML Engineer / MLOps Engineer**siz. [Mashqlar](./exercises.md) ni ko'rib chiqing va [Final Loyihalar](../final-projects/README.md) ga o'ting.
