# NumPy

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- NumPy `ndarray` ni Python `list`'dan farqini tushunasiz va qachon ishlatishni bilasiz
- Vectorized operations bilan loop'siz tezkor kod yozishni o'rganasiz
- Broadcasting'dan foydalanib turli o'lchamdagi array'lar bilan ishlay olasiz
- ML kodida 90% paydo bo'ladigan NumPy patternlarini bilasiz

## 📖 Nimani o'rganish kerak

- `ndarray` yaratish: `np.array`, `np.zeros`, `np.ones`, `np.arange`, `np.linspace`, `np.random`
- Array atributlari: `shape`, `dtype`, `ndim`, `size`
- Indexing va slicing (1-D, 2-D, boolean, fancy)
- Reshape, transpose, concatenate, stack, split
- Arithmetic operations va broadcasting
- Universal functions (ufuncs): `np.sin`, `np.exp`, `np.log`, va h.k.
- Aggregations: `sum`, `mean`, `max`, `min`, `argmax`, `axis` parametri
- Linear algebra (`np.linalg`)
- Random sampling (`np.random`)

## 📦 Kutubxonalar

```bash
pip install numpy
```

NumPy versiyasi 1.26+ yoki 2.x tavsiya etiladi.

## 🧠 Muhim mavzular

### Nima uchun NumPy Python list'dan tezroq?

```python
# Python list — har element alohida PyObject (sekin)
py_list = [1, 2, 3, 1_000_000]
# NumPy — bir blok C massiv (tez)
np_arr = np.array([1, 2, 3, 1_000_000], dtype=np.int64)
```

NumPy:
- C tilida yozilgan, **SIMD** instruktsiyalardan foydalanadi
- Bitta `dtype` (masalan, hammasi `int64`) — `cache-friendly`
- **Vectorized**: `arr * 2` — bitta operatsiya, butun array'ga

Bench: `1M ta elementni 2 ga ko'paytirish` — list ~50ms, NumPy ~1ms (50x tez).

### Broadcasting

NumPy'ning eng kuchli xususiyati. Turli o'lchamdagi array'lar bilan ishlash:

```python
# (3, 3) matritsaga (3,) vektor qo'shish
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # shape (3, 3)
b = np.array([10, 20, 30])                        # shape (3,)
result = A + b
# [[11, 22, 33], [14, 25, 36], [17, 28, 39]]
```

NumPy avtomatik `b` ni har bir qatorga "broadcast" qiladi.

**Qoida:** O'lchamlar oxiridan boshlab solishtiriladi. Ular yo teng, yo birortasi `1` bo'lishi kerak.

### Axis tushunchasi

2-D array uchun:
- `axis=0` — qator (vertikal, "down the rows")
- `axis=1` — ustun (gorizontal, "across the columns")

```python
A = np.array([[1, 2], [3, 4], [5, 6]])  # shape (3, 2)
A.sum(axis=0)  # [9, 12]  — har ustun summasi
A.sum(axis=1)  # [3, 7, 11]  — har qator summasi
```

## 💻 Kod misollari

### Array yaratish va asosiy operatsiyalar

```python
import numpy as np

# Yaratish usullari
a = np.array([1, 2, 3, 4])
zeros = np.zeros((3, 4))            # 3×4 nollar
ones = np.ones((2, 2))               # 2×2 birlar
rng = np.arange(0, 10, 2)            # [0, 2, 4, 6, 8]
lin = np.linspace(0, 1, 5)           # 5 ta teng tarqalgan son [0, 0.25, 0.5, 0.75, 1]
random_arr = np.random.rand(3, 3)    # 3×3 random [0, 1)

# Atributlar
print(a.shape, a.dtype, a.ndim, a.size)  # (4,) int64 1 4
```

### Indexing va boolean filtering

```python
arr = np.array([10, 20, 30, 40, 50, 60])

# Slicing
print(arr[1:4])      # [20, 30, 40]
print(arr[::-1])     # teskari

# Boolean indexing — ML'da juda ko'p ishlatiladi
mask = arr > 30
print(arr[mask])     # [40, 50, 60]

# Bir vaqtda filter va o'zgartirish
arr[arr < 30] = 0
print(arr)           # [0, 0, 30, 40, 50, 60]

# 2-D indexing
M = np.arange(12).reshape(3, 4)
print(M[1, 2])       # 6
print(M[:, 1])       # 2-ustun
print(M[1:, :2])     # 1-qatordan, 0 va 1-ustunlar
```

### Vectorized operations (loop'siz)

```python
# Loop bilan (SEKIN — bunday qilmang)
arr = np.arange(1_000_000)
result = []
for x in arr:
    result.append(x ** 2 + 3 * x - 5)

# Vectorized (TEZ — har doim shunday)
arr = np.arange(1_000_000)
result = arr ** 2 + 3 * arr - 5

# Conditional vectorization
prices = np.array([100, 50, 200, 75, 300])
discounted = np.where(prices > 100, prices * 0.9, prices)
# [100, 50, 180, 75, 270]
```

## 🔌 Backend integratsiyasi

Backend'da NumPy quyidagi joylarda qulay:

### 1. Tezkor JSON aggregatsiya
```python
from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.post("/metrics/")
def process_metrics(values: list[float]):
    arr = np.array(values, dtype=np.float64)
    # Pure Python da 1M element uchun ~500ms, NumPy da ~5ms
    return {
        "sum": float(arr.sum()),
        "mean": float(arr.mean()),
        "p50": float(np.percentile(arr, 50)),
        "p95": float(np.percentile(arr, 95)),
        "p99": float(np.percentile(arr, 99)),
    }
```

### 2. Image processing endpoint
```python
import numpy as np
from PIL import Image
from io import BytesIO

@app.post("/image/grayscale/")
async def to_grayscale(file: UploadFile):
    img = Image.open(file.file)
    arr = np.array(img)
    # RGB ni grayscale ga: luminance formulasi
    gray = (0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]).astype(np.uint8)
    out = Image.fromarray(gray)
    buf = BytesIO()
    out.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")
```

### 3. Embedding similarity (RAG uchun)
```python
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Batch search — 1000 ta embeddingni query bilan solishtirish
def find_similar(query: np.ndarray, embeddings: np.ndarray, top_k: int = 5):
    # embeddings shape: (1000, 384), query shape: (384,)
    sims = embeddings @ query / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query))
    top_indices = np.argsort(sims)[::-1][:top_k]
    return top_indices, sims[top_indices]
```

## 📚 Resurslar

- **Official NumPy quickstart** — [numpy.org/doc/stable/user/quickstart.html](https://numpy.org/doc/stable/user/quickstart.html)
- **"From Python to NumPy"** — Nicolas Rougier (bepul, advanced patterns)
- **NumPy Illustrated: The Visual Guide** — Lev Maximov (Medium)
- **"100 NumPy exercises"** — GitHub repo (mashqlar to'plami): [github.com/rougier/numpy-100](https://github.com/rougier/numpy-100)

## 🏋️ Mashqlar

### 🟢 Easy
1. `np.arange(0, 100, 5)` ga teng array yarating va ulardan toq sonlarni filter qiling.
2. `3×3` random matrix yarating, eng katta elementni va uning indeksini toping (`np.argmax`).
3. Ikki array `[1, 2, 3, 4]` va `[5, 6, 7, 8]` ni vertikal va gorizontal birlashtiring (`np.vstack`, `np.hstack`).

### 🟡 Medium
1. `10000` ta tasodifiy son yarating va Pure Python `for` loop + NumPy vectorized variantida `x^2 + 2x + 1` hisoblang. `timeit` bilan ikkalasini solishtiring.
2. `(50, 50)` random matrix yarating va `chess` panjarasini imitatsiya qiling (`np.indices` + broadcasting).
3. Normalize qilish: random matrix uchun har ustunni `0..1` oralig'iga keltiring (min-max normalization).

### 🔴 Hard
1. **Cosine similarity API**: FastAPI endpoint yarating. Foydalanuvchi `query: list[float]` va `database: list[list[float]]` yuboradi. Top-K eng o'xshash vektorlarni qaytaring. Hammasi NumPy vectorized bo'lsin (loop ishlatmang).
2. **Sliding window**: 1-D array uchun `window_size=k` bo'lgan rolling mean'ni `np.lib.stride_tricks` yordamida memory-efficient hisoblang.

## 🚀 Capstone

`notebooks/month-01/01_numpy_basics.ipynb` faylida:
- 1000 ta foydalanuvchining 30 kunlik faollik matritsasini simulyatsiya qiling: `shape (1000, 30)`
- Har foydalanuvchining haftalik o'rtacha faolligini hisoblang (`shape (1000, 4)`)
- Eng faol 10 foydalanuvchini toping
- Faollik matritsasini heatmap shaklida vizualizatsiya qiling (Matplotlib bilan)

## ✅ Tekshirish ro'yxati

- [ ] `ndarray` va Python `list` farqini tushunaman
- [ ] `shape`, `dtype`, `axis` tushunchalari aniq
- [ ] Boolean indexing'dan foydalanaman, `for` loop yozmayman
- [ ] Broadcasting qoidasini bilaman, kichik misollarda qo'llay olaman
- [ ] `np.linalg` orqali matritsa amallari (dot product, inverse, eigvals) ni bilaman
- [ ] Vectorized kodimning Python loop'dan necha barobar tez ekanini o'lchaganman

[Pandas](./03-pandas.md) ga o'tish vaqti keldi.
