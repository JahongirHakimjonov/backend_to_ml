# Matematika asoslari

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- ML kodida uchraydigan vektor, matritsa, gradient kabi tushunchalarni tushunasiz
- Algoritmlar nima uchun shunday ishlashini matematik nuqtai nazardan ko'ra olasiz
- Loss function, gradient descent kabi terminlar sizga "qora quti" bo'lmaydi

> **Eslatma:** ML uchun matematika — bu universitet darajasidagi to'liq kurs emas. Sizga `intuition` (sezgi) va asosiy operatsiyalarning ma'nosi yetadi. Chuqur teoremalarni o'rganishingiz shart emas.

## 📖 Nimani o'rganish kerak

### 1. Linear Algebra (chiziqli algebra)
- **Scalar, Vector, Matrix, Tensor** — ML'da ma'lumotlar shu shaklda
- **Vektor operatsiyalari** — qo'shish, ko'paytirish, dot product (skalyar ko'paytma)
- **Matritsa operatsiyalari** — transpose, ko'paytma, inverse, determinant
- **Identity matrix, Diagonal matrix** — maxsus matritsalar
- **Eigenvalues va Eigenvectors** — PCA va SVD uchun

### 2. Calculus (matematik analiz)
- **Function (funksiya)** — input → output
- **Derivative (hosila)** — funksiya qanday tezlikda o'zgaradi
- **Partial derivative (qisman hosila)** — bir necha o'zgaruvchili funksiyada
- **Gradient** — barcha qisman hosilalardan iborat vektor
- **Chain rule (zanjir qoidasi)** — neural network'ning asosi (backpropagation)
- **Optimization (optimizatsiya)** — minimum/maximum qidirish

### 3. Statistics va Probability
- **Mean, Median, Mode** — markaziy tendensiya o'lchovlari
- **Variance, Standard Deviation** — tarqoqlik
- **Normal distribution (Gaussian)** — ML'dagi eng muhim taqsimot
- **Probability distributions** — Bernoulli, Binomial, Poisson, Uniform
- **Bayes Theorem** — shartli ehtimollik
- **Correlation** vs **Causation** — bog'liqlik vs sabab
- **Hypothesis testing** — A/B testlar uchun

## 📦 Kutubxonalar

```bash
pip install numpy scipy sympy matplotlib
```

- **NumPy** — vektor/matritsa hisob-kitoblari
- **SciPy** — ilg'or matematik funksiyalar, statistika
- **SymPy** — simvolik matematika (formulalar bilan ishlash)

## 🧠 Muhim mavzular

### Vector va Matrix ML'da
Har qanday ma'lumot ML uchun **tensor** shaklida bo'ladi:

- **Skalyar** (0-d tensor) — bitta son: `5`
- **Vektor** (1-d tensor) — sonlar ro'yxati: `[1, 2, 3]` (masalan, bir o'quvchining 3 ta fan bahosi)
- **Matrix** (2-d tensor) — jadval: `[[1,2,3], [4,5,6]]` (masalan, 2 ta o'quvchi × 3 fan)
- **Tensor** (3+ d) — masalan, rasm: `[height, width, channels]`

### Gradient nima va nima uchun kerak?

Tasavvur qiling, siz tog'da turibsiz va eng pastki nuqtaga tushishingiz kerak. **Gradient** sizga aytadi: "qaysi tomon eng tik balanddir" — siz uning **teskari** yo'nalishida qadam tashlaysiz. Bu **Gradient Descent** algoritmining mohiyati.

ML'da:
- Tog' = **loss function** (xatolik darajasi)
- Tushish = **training** (o'rgatish)
- Maqsad = **loss'ni minimallashtirish**

### Normal distribution nima uchun muhim?

Real dunyodagi ko'p o'lchamlar (odamlar bo'yi, mahsulot narxi, IQ) **normal taqsimot**ga ega. Bu **Central Limit Theorem** (markaziy chegara teoremasi)dan kelib chiqadi. ML algoritmlari ham ko'pincha shu taqsimotga moslashtirilgan.

## 💻 Kod misollari

### NumPy bilan vektor va matritsa

```python
import numpy as np

# Vektor
v = np.array([1, 2, 3])

# Matrix (matritsa)
A = np.array([[1, 2], [3, 4]])

# Dot product (skalyar ko'paytma)
u = np.array([4, 5, 6])
result = np.dot(v, u)  # 1*4 + 2*5 + 3*6 = 32

# Matritsa ko'paytmasi
B = np.array([[5, 6], [7, 8]])
C = A @ B  # yoki np.matmul(A, B)

# Transpose
A_T = A.T
```

### Gradient hisoblash (oddiy misol)

```python
import numpy as np

# f(x) = x^2 funksiyasining hosilasi: f'(x) = 2x
def f(x):
    return x ** 2

def gradient_f(x):
    return 2 * x

# Gradient descent — minimumni topish
x = 10.0  # boshlang'ich nuqta
learning_rate = 0.1

for i in range(20):
    grad = gradient_f(x)
    x = x - learning_rate * grad  # teskari yo'nalishda qadam
    print(f"step {i}: x = {x:.4f}, f(x) = {f(x):.4f}")

# Natija: x → 0 ga yaqinlashadi (f(x) = x^2 ning minimumi)
```

### Statistik o'lchovlar

```python
import numpy as np

data = np.array([2, 4, 4, 4, 5, 5, 7, 9])

print(f"Mean:    {np.mean(data)}")      # 5.0
print(f"Median:  {np.median(data)}")    # 4.5
print(f"Std:     {np.std(data):.2f}")   # 2.00
print(f"Var:     {np.var(data):.2f}")   # 4.00

# Normal taqsimotdan tasodifiy son
sample = np.random.normal(loc=0, scale=1, size=1000)
print(f"Sample mean: {sample.mean():.3f}")  # ~0 ga yaqin
print(f"Sample std:  {sample.std():.3f}")   # ~1 ga yaqin
```

## 🔌 Backend integratsiyasi

Backend dev sifatida sizga matematika quyidagi joylarda kerak bo'ladi:

1. **Analytics endpoints** — Django'da `/api/stats/` route — `mean`, `median`, `percentile` hisoblash uchun NumPy ishlatishingiz mumkin (Python'ning ichidagi `statistics` modulidan tez)
2. **A/B testing backend** — ikki versiya farqi statistik jihatdan ahamiyatlimi tekshirish (scipy.stats.ttest_ind)
3. **Anomaly detection** — z-score yoki IQR usulida outlier'larni topish
4. **Rate limiting va load forecasting** — Poisson distribution bilan request load'ni bashorat qilish

```python
# FastAPI'da statistik endpoint misoli
from fastapi import FastAPI
import numpy as np
from scipy import stats

app = FastAPI()

@app.post("/api/stats/")
def calculate_stats(values: list[float]):
    arr = np.array(values)
    return {
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "std": float(arr.std()),
        "p95": float(np.percentile(arr, 95)),
        "outliers_zscore": [
            float(v) for v in arr if abs((v - arr.mean()) / arr.std()) > 3
        ],
    }
```

## 📚 Resurslar

### Bepul
- **3Blue1Brown — "Essence of Linear Algebra"** (YouTube playlist) — vizual tushuntirish, **MUST WATCH** ([link](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab))
- **3Blue1Brown — "Essence of Calculus"** (YouTube playlist) — calculus uchun
- **Khan Academy — Linear Algebra** ([link](https://www.khanacademy.org/math/linear-algebra))
- **StatQuest with Josh Starmer** (YouTube) — statistika tushunchalarini soddalashtirish
- **"Mathematics for Machine Learning"** — Deisenroth, Faisal, Ong (bepul PDF: [mml-book.com](https://mml-book.com/))

### Pullik (ixtiyoriy)
- **Coursera — Mathematics for Machine Learning Specialization** (Imperial College London)

## 🏋️ Mashqlar

### 🟢 Easy
1. NumPy bilan 5 ta tasodifiy son yarating, ularning `mean`, `median`, `std` ni toping.
2. Ikki vektor `[1, 2, 3]` va `[4, 5, 6]` ning dot product'ini qo'lda hisoblang, keyin NumPy bilan tekshiring.
3. `3x3` identity matrix yarating.

### 🟡 Medium
1. `f(x) = (x-3)^2 + 5` funksiyasining minimumini gradient descent bilan toping (learning rate'ni o'zgartirib ko'ring: 0.01, 0.1, 1.0).
2. 1000 ta tasodifiy normal sonlardan dataset yarating va histogram chizing (matplotlib bilan).
3. `scipy.stats` ishlatib, ikki guruh natijalari uchun t-test o'tkazing va p-value'ni interpret qiling.

### 🔴 Hard
1. FastAPI endpoint yozing: foydalanuvchi `[float]` ro'yxat yuboradi, javob qilib `mean`, `std`, `outliers (z-score > 3)`, `normality test (Shapiro-Wilk)` natijalarini qaytaring. Pydantic model'lar bilan to'liq type-safe qiling.

## 🚀 Capstone (oxirgi mashq)

`notebooks/month-01/00_math_warmup.ipynb` faylida quyidagilarni amalga oshiring:
1. NumPy bilan 100×100 random matrix yarating
2. Uning eigenvalues va eigenvectors'ini toping (`np.linalg.eig`)
3. Matritsani SVD bilan dekompozitsiya qiling (`np.linalg.svd`)
4. Singular values'larni vizualizatsiya qiling

## ✅ Tekshirish ro'yxati

- [ ] Vektor va matritsa farqini tushunaman
- [ ] Dot product nima ekanini, qachon ishlatilishini bilaman
- [ ] Gradient nima — bir gapda tushuntira olaman
- [ ] Gradient descent algoritmini kodda yozdim
- [ ] Mean, median, std orasidagi farqni bilaman
- [ ] Normal distribution nimaligini, nima uchun muhimligini tushunaman
- [ ] Bayes theorem'ning bir misolini ayta olaman
- [ ] NumPy'da matritsa amallarini bajarishni bilaman

Tayyor bo'lsangiz, [NumPy](./02-numpy.md) bobiga o'ting.
