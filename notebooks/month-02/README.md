# Month 02 — Klassik ML Notebooks

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `00_ml_intro.ipynb` | Pipeline va sklearn | [ML intro](../../src/month-02-classical-ml/01-ml-intro.md) |
| `01_regression.ipynb` | Linear, Ridge, Lasso | [Regression](../../src/month-02-classical-ml/02-regression.md) |
| `02_classification_models.ipynb` | LogReg, SVM, Trees | [Classification](../../src/month-02-classical-ml/03-classification.md) |
| `03_clustering.ipynb` | K-Means, DBSCAN | [Clustering](../../src/month-02-classical-ml/04-clustering.md) |
| `04_feature_engineering.ipynb` | FE patterns | [Feature Engineering](../../src/month-02-classical-ml/05-feature-engineering.md) |
| `05_model_evaluation.ipynb` | CV, hyperparams | [Model Evaluation](../../src/month-02-classical-ml/06-model-evaluation.md) |
| `06_kaggle_competition.ipynb` | Capstone | [Ensembles](../../src/month-02-classical-ml/07-ensemble-methods.md) |

## 🛠 Dependencies

```bash
# uv bilan (loyiha root'idan)
uv sync --group month-02
uv run jupyter lab
```

Tarkibida: scikit-learn, xgboost, lightgbm, catboost, imbalanced-learn, optuna, category-encoders, shap, yellowbrick.

## 📚 Asosiy datasetlar

- **Titanic** — Kaggle (binary classification)
- **House Prices** — Kaggle (regression)
- **Telco Customer Churn** — Kaggle (imbalanced binary)
- **Wine, Iris, Breast Cancer** — sklearn.datasets

Notebook'larni asosiy bobdan keyin yarating: [Oy 2 — Klassik ML](../../src/month-02-classical-ml/README.md).
