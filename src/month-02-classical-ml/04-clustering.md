# Clustering

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Unsupervised learning va clustering nima ekanini tushunasiz
- K-Means, DBSCAN, Hierarchical algoritmlarining farqini bilasiz
- Optimal cluster sonini topish usullarini bilasiz
- Customer segmentation kabi real biznes loyihalarda qo'llay olasiz

## Nimani o'rganish kerak

- **K-Means** — eng oddiy va keng tarqalgan
- **K-Means++** — yaxshi initialization
- **MiniBatchKMeans** — katta datasetlar uchun
- **DBSCAN** — density-based, ixtiyoriy shakl
- **Hierarchical Clustering** — agglomerative, dendrogram
- **Gaussian Mixture Models (GMM)** — soft clustering
- **Mean Shift, OPTICS** — alternativlar
- **Cluster soni tanlash** — Elbow method, Silhouette score
- **Vizualizatsiya** — PCA, t-SNE, UMAP bilan 2D'ga

## Kutubxonalar

```bash
pip install scikit-learn umap-learn yellowbrick
```

- **scikit-learn** — asosiy algoritmlar
- **umap-learn** — dimensionality reduction (t-SNE'dan tezroq va aniqroq)
- **yellowbrick** — ML vizualizatsiyalari (Elbow, Silhouette)

## Muhim mavzular

### Clustering qachon kerak?

- **Customer segmentation** — mijozlarni guruhlash (marketing uchun)
- **Anomaly detection** — qaysi nuqta hech bir guruhga to'g'ri kelmaydi
- **Document grouping** — o'xshash matnlarni topish
- **Image compression** — ranglarni clusterlash
- **Feature engineering** — cluster ID'ni yangi feature qilish

### K-Means algoritmi

```
1. K ta tasodifiy markaz (centroid) tanlash
2. Har nuqtani eng yaqin centroidga assign qilish
3. Centroidlarni o'rta arifmetik bilan yangilash
4. Konvergentsiyaga qadar 2-3 qadamlarini takrorlash
```

**Cheklovlar:**
- K ni oldindan bilish kerak
- Faqat sferik cluster'lar
- Outlier'larga sezgir
- Feature scaling muhim

### DBSCAN — alternativ

K-Means'dan farqli:
- K kerak emas (avtomatik)
- Ixtiyoriy shaklli cluster'lar
- Outlier'larni avtomatik aniqlaydi (noise label `-1`)
- 2 ta parametr: `eps` (radius) va `min_samples`

```
DBSCAN'da nuqta turlari:
- Core: eps radiusida >= min_samples ta nuqta
- Border: core'ga yaqin lekin o'zi core emas
- Noise: hech bir cluster'ga to'g'ri kelmaydi (outlier)
```

### Optimal K topish

**1. Elbow method:**
```
Har K uchun inertia (within-cluster sum of squares) hisoblash
→ "burchak" joyini topish (egilish bo'yicha)
```

**2. Silhouette score:**
```
Score = (b - a) / max(a, b)
a = average distance to own cluster
b = average distance to nearest other cluster

Range: [-1, 1]
1 = ajoyib clustering
0 = overlapping clusters
< 0 = noto'g'ri assignment
```

## Kod misollari

### K-Means clustering

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Sun'iy data
X, _ = make_blobs(n_samples=500, centers=4, n_features=2, random_state=42)

# Scale (MUHIM — distance-based algoritmlar uchun)
X_scaled = StandardScaler().fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# Silhouette
score = silhouette_score(X_scaled, labels)
print(f"Silhouette Score: {score:.3f}")  # 0.8+ — yaxshi

# Vizualizatsiya
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=30)
ax.scatter(*kmeans.cluster_centers_.T, c="red", s=200, marker="X", label="Centroids")
ax.legend()
plt.show()
```

### Elbow method

```python
from yellowbrick.cluster import KElbowVisualizer

model = KMeans(n_init=10, random_state=42)
visualizer = KElbowVisualizer(model, k=(2, 11), metric="distortion")
visualizer.fit(X_scaled)
visualizer.show()
# Avtomatik "elbow point" ni aniqlaydi
```

### Silhouette analysis

```python
from sklearn.metrics import silhouette_score

scores = {}
for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels)

best_k = max(scores, key=scores.get)
print(f"Best k: {best_k} (silhouette = {scores[best_k]:.3f})")
```

### DBSCAN

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.3, min_samples=10)
labels = dbscan.fit_predict(X_scaled)

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)
print(f"Clusters: {n_clusters}, Noise points: {n_noise}")
```

### Hierarchical Clustering + Dendrogram

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt

linkage_matrix = linkage(X_scaled, method="ward")

fig, ax = plt.subplots(figsize=(12, 5))
dendrogram(linkage_matrix, truncate_mode="lastp", p=20, leaf_font_size=10, ax=ax)
ax.set_title("Hierarchical Clustering Dendrogram")
plt.show()

# Cut tree pri threshold
labels = fcluster(linkage_matrix, t=4, criterion="maxclust")
```

### Customer Segmentation — Real misol (RFM)

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Sun'iy customer data
df = pd.DataFrame({
    "customer_id": range(1000),
    "recency_days": np.random.exponential(30, 1000),
    "frequency": np.random.poisson(5, 1000),
    "monetary": np.random.exponential(500, 1000),
})

# RFM scaling
X = df[["recency_days", "frequency", "monetary"]].copy()
X["recency_days"] = -X["recency_days"]  # less is better → invert
X_scaled = StandardScaler().fit_transform(X)

# Clustering
km = KMeans(n_clusters=4, n_init=10, random_state=42)
df["segment"] = km.fit_predict(X_scaled)

# Segment xulosalari
segment_summary = df.groupby("segment")[["recency_days", "frequency", "monetary"]].mean()
print(segment_summary)
# Biznes nomlash:
# Champions:    low recency, high freq, high monetary
# At Risk:      high recency, low freq, low monetary
# va h.k.
```

## Backend integratsiyasi

### Customer Segmentation API

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model_bundle = joblib.load("models/customer_segments.joblib")
# {"kmeans": kmeans, "scaler": scaler, "segment_names": [...]}

class CustomerRFM(BaseModel):
    recency_days: int
    frequency: int
    monetary: float

class SegmentResponse(BaseModel):
    segment_id: int
    segment_name: str
    marketing_action: str

SEGMENT_ACTIONS = {
    0: "Champions — VIP offer",
    1: "At Risk — win-back campaign",
    2: "New — onboarding email",
    3: "Loyal — referral program",
}

@app.post("/segment", response_model=SegmentResponse)
def get_segment(customer: CustomerRFM):
    X = np.array([[-customer.recency_days, customer.frequency, customer.monetary]])
    X_scaled = model_bundle["scaler"].transform(X)
    seg_id = int(model_bundle["kmeans"].predict(X_scaled)[0])
    return SegmentResponse(
        segment_id=seg_id,
        segment_name=model_bundle["segment_names"][seg_id],
        marketing_action=SEGMENT_ACTIONS[seg_id],
    )
```

### Anomaly Detection (DBSCAN)

```python
@app.post("/check-anomaly")
def detect_anomaly(transaction: TransactionData):
    X = np.array([[transaction.amount, transaction.time_of_day, ...]])
    X_scaled = scaler.transform(X)
    
    # DBSCAN re-fit on recent data + new point
    cluster = dbscan.fit_predict(np.vstack([recent_data, X_scaled]))[-1]
    
    is_anomaly = cluster == -1
    return {"is_anomaly": is_anomaly, "cluster": int(cluster)}
```

## Resurslar

- **Scikit-learn Clustering** — [scikit-learn.org/stable/modules/clustering.html](https://scikit-learn.org/stable/modules/clustering.html)
- **StatQuest — K-Means, Hierarchical Clustering**(YouTube)
- **"K-Means visualization"** — [naftaliharris.com/blog/visualizing-k-means-clustering/](https://www.naftaliharris.com/blog/visualizing-k-means-clustering/)
- **UMAP docs** — t-SNE alternativ
- **"Customer Segmentation in Python"** — Towards Data Science

## 🏋️ Mashqlar

### 🟢 Easy
1. `make_blobs` bilan 3 ta cluster yarating, K-Means bilan classifylang va vizualizatsiya qiling.
2. Elbow method bilan optimal K ni toping (K=2..10).
3. DBSCAN'da `eps` ni o'zgartirib (`0.1, 0.3, 0.5, 1.0`) natijani ko'ring.

### 🟡 Medium
1. **Wholesale Customer**dataset (UCI) yuklang, K-Means bilan customer segmentlarini toping va har segmentni biznes nuqtai nazaridan interpret qiling.
2. **t-SNE / UMAP**bilan yuqori o'lchamli datani 2D'da vizualizatsiya qiling.
3. **Silhouette analysis**: turli `k` qiymatlar uchun silhouette plot chizing.

### 🔴 Hard
1. **Segmentation API**: production-ready FastAPI servisi — customer RFM data kelganda real-time segment qaytaradi, modeli har hafta retrain bo'ladi (Airflow yoki cron).
2. **Image color quantization**: rasm fayl yuklab, K-Means bilan 16 ta dominant ranglar bilan qayta yarating (image compression).

## Capstone

`notebooks/month-02/03_clustering.ipynb`:
- **Mall Customer Segmentation**Kaggle dataset
- EDA → feature selection (Age, Income, Spending Score)
- K-Means, DBSCAN, Hierarchical solishtirish
- Optimal K topish
- Har clusterni biznes tilida nomlash (Premium, Budget, Young Spenders, etc.)
- Marketing tavsiyalari yozish

## ✅ Tekshirish ro'yxati

- [ ] Supervised vs Unsupervised farqini bilaman
- [ ] K-Means algoritmi qanday ishlashini tushunaman
- [ ] Optimal K ni Elbow va Silhouette bilan topishni bilaman
- [ ] K-Means va DBSCAN qachon qaysi birini ishlatishni bilaman
- [ ] Feature scaling clustering uchun nima uchun muhimligini bilaman
- [ ] Customer segmentation kabi real biznes loyihaga clustering'ni qo'llay olaman

[Feature Engineering](./05-feature-engineering.md) ga o'tamiz.
