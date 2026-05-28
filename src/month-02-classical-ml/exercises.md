# Oy 2 — Mashqlar to'plami

## 🟢 Easy

### Algoritmlar
1. `load_iris()`, `load_wine()`, `load_breast_cancer()` — har biri uchun 3 ta turli model train qiling va accuracy solishtiring.
2. `LogisticRegression`, `KNN`, `SVM`, `DecisionTree`, `RandomForest` — barchasini `cross_val_score` bilan baholang.
3. Feature scaling kerakmi yoki yo'qmi har model uchun aniqlang (Pipeline + StandardScaler bilan va siz solishtiring).

### Metrics
1. Confusion matrix'ni ko'lda hisoblang va `sklearn.metrics.confusion_matrix` bilan tekshiring.
2. Precision, Recall, F1 ni formula bilan qo'lda hisoblang.
3. `predict` va `predict_proba` farqini ko'rsating, threshold o'zgartirib accuracy ni o'zgartiring.

### Pipeline
1. `Pipeline([scaler, model])` yarating va `fit_predict` qiling.
2. `ColumnTransformer` bilan numerik va categorical ustunlarni alohida ishlang.
3. Pipeline'ni `joblib.dump` bilan saqlang va qaytadan yuklang.

## 🟡 Medium

### Real datasets
1. **Titanic**: Pipeline + Random Forest bilan 80%+ accuracy oling.
2. **House Prices**: Lasso + Ridge solishtiring, R² 0.85+ oling.
3. **Telco Churn**: imbalanced data bilan kurashing, F1 0.6+ oling.
4. **Wine Quality**: regression vs classification yondashuvini solishtiring.

### Feature Engineering
1. NYC Taxi: datetime'dan 10+ feature yarating va RF accuracy yaxshilanishini ko'ring.
2. Text feature engineering: bitta categorical ustunni `n-gram` bilan boyiting.
3. Polynomial features: degree=2 bilan eksperiment, overfitting'ni kuzating.

### Hyperparameter Tuning
1. `GridSearchCV` bilan XGBoost 3 ta parametr — 100 trial vaqt necha?
2. `RandomizedSearchCV` bilan bir xil narsa — vaqt va sifat farqi?
3. `Optuna` bilan 100 trial — eng yaxshi va eng tez!

### Ensembles
1. RF vs XGBoost vs LightGBM vs CatBoost — bir xil datasetda solishtiring (jadval).
2. Voting Classifier (3 model) — har birining alohida natijasidan yaxshiroqmi?
3. Stacking — base + meta yaratish.

## 🔴 Hard (Production)

### 1. Churn Prediction Service

**To'liq talab:**
- Django REST Framework yoki FastAPI
- PostgreSQL'da `customer` jadval (50+ feature)
- `/api/v1/predict/churn/{customer_id}` — DB'dan feature olish + prediction
- `/api/v1/predict/churn/batch` — CSV upload + Celery background
- `/api/v1/feedback` — real natija qaytarish (model improvement uchun)
- `/api/v1/metrics` — Prometheus format
- Docker + docker-compose
- GitHub Actions CI/CD

### 2. AutoML Service

Datasetni yuklab, avtomatik ravishda:
- EDA report (ydata-profiling)
- 5+ algoritm taqqoslash
- Best model'ni saqlash
- Prediction endpoint avtomatik tayyor

Inspirator: H2O AutoML, PyCaret.

### 3. A/B Testing Backend

- Ikki model serve qilish (`v1` va `v2`)
- Random traffic split (60/40 yoki configurable)
- Har prediction Postgres'ga log
- Statistik test bilan qaysi model yaxshi ekanini avtomatik aniqlash
- Slack notification: "Model v2 wins!"

### 4. Real-time Anomaly Detection

- Kafka consumer (transaction stream)
- IsolationForest yoki DBSCAN bilan online anomaly detection
- Anomaliyalarni alohida Kafka topic'ga jo'natish
- Grafana dashboard

## 🏆 Mini-loyihalar

### Mini-loyiha 1: Spam Classifier
- SMS Spam dataset (UCI)
- TF-IDF + Logistic Regression / Naive Bayes
- FastAPI endpoint
- Streamlit UI

### Mini-loyiha 2: Stock Price Direction
- yfinance bilan stock data
- Texnik indikatorlar (RSI, MACD) feature engineering
- Up/Down classification
- Backtesting

### Mini-loyiha 3: Recommendation System (Collaborative Filtering)
- MovieLens dataset
- Surprise library
- User-based va item-based
- API: `/recommend/{user_id}`

### Mini-loyiha 4: Time Series Forecasting
- Prophet yoki ARIMA
- Daily sales bashorat
- 30 kunlik prediction

## 🧪 Quiz

### ML Fundamentals
1. Supervised va Unsupervised farqi?
2. Bias-Variance tradeoff'ni misol bilan tushuntiring.
3. Overfitting'ni qanday aniqlasiz?
4. Cross-validation nima uchun kerak?
5. Train/Val/Test bo'lishda nima uchun 3 ta?

### Algorithms
1. Logistic Regression nomidagi "regression" so'zi nima uchun? (Hint: log-odds)
2. KNN'da `k` parametri nimaga ta'sir qiladi?
3. Random Forest va Gradient Boosting farqi (parallel vs sequential)?
4. XGBoost va LightGBM asosiy farqi?
5. CatBoost'ning categorical handling'i nima sababdan yaxshiroq?

### Metrics
1. Imbalanced classification'da accuracy nima uchun yomon metric?
2. ROC-AUC va PR-AUC qachon farq qiladi?
3. F1 va F-beta orasidagi farq?
4. Regression'da MAE va MSE qachon birini ishlatasiz?
5. R² manfiy bo'lishi mumkinmi? Nima uchun?

### Production
1. `joblib` va `pickle` farqi?
2. ML modelni Docker'ga qanday joylaysiz?
3. Model drift nima va qanday aniqlanadi? (preview, Oy 6)
4. ONNX nima uchun foydali?
5. A/B testing'da statistical significance nima?

## ✅ Oy 2 oxiri checklist

- [ ] Klassik ML algoritmlarining ko'pini ishlatib ko'rdim
- [ ] Scikit-learn Pipeline va ColumnTransformer ni egalladim
- [ ] XGBoost/LightGBM bilan ishladim (kamida 1 ta competition)
- [ ] Optuna bilan hyperparameter tuning qildim
- [ ] SHAP yoki Feature Importance bilan modelni interpret qildim
- [ ] FastAPI bilan ML model production'ga chiqarish
- [ ] Birinchi Kaggle submission qildim (top 30%)
- [ ] GitHub'ga capstone loyiha
- [ ] LinkedIn'ga post (loyiha + sertifikat)

Tabriklayman! 🎉 [Oy 3 — Deep Learning](../month-03-deep-learning/README.md) ga o'tamiz.
