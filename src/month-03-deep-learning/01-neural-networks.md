# Neural Networks asoslari

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Neural network nima ekanini, qanday qurilganini tushunasiz
- Perceptron, MLP, activation functions, loss functions ni bilasiz
- Forward pass va Backpropagation algoritmlarini tushunasiz
- Gradient Descent va uning variantlarini bilasiz
- Pure NumPy bilan oddiy NN yoza olasiz

## Nimani o'rganish kerak

- **Perceptron** — eng oddiy "neuron"
- **Multi-Layer Perceptron (MLP)** — chuqurroq
- **Activation functions** — ReLU, Sigmoid, Tanh, Softmax
- **Loss functions** — MSE, CrossEntropy, Binary CrossEntropy
- **Forward pass** — input → output yo'li
- **Backpropagation** — gradient'larni hisoblash
- **Gradient Descent**variantlari — SGD, Momentum, Adam, RMSprop
- **Universal Approximation Theorem** — nima uchun NN ishlaydi

## Kutubxonalar

```bash
pip install numpy matplotlib torch torchvision
```

## Muhim mavzular

### Perceptron — eng oddiy neuron

```
input  ─x₁──┐
input  ─x₂──┤── (weighted sum) ── activation ── output
input  ─x₃──┘
            ↑
           bias

z = w₁x₁ + w₂x₂ + w₃x₃ + b
a = activation(z)
```

### Activation functions — nima uchun kerak?

Agar `activation` bo'lmasa, butun NN — bitta katta `linear regression`. Activation = **nonlinearity**qo'shadi.

| Function | Formula | Range | Qachon |
|----------|---------|-------|--------|
| **Sigmoid** | `1/(1+e^-x)` | (0, 1) | Binary classification output |
| **Tanh** | `(e^x - e^-x)/(e^x + e^-x)` | (-1, 1) | Hidden layers (eski) |
| **ReLU** | `max(0, x)` | [0, ∞) | Hidden layers (default) |
| **Leaky ReLU** | `max(0.01x, x)` | (-∞, ∞) | ReLU dying neuron muammosi |
| **Softmax** | `e^xᵢ / Σe^xⱼ` | (0, 1), sum=1 | Multi-class output |
| **GELU** | `x * Φ(x)` | ~ReLU | Transformers'da |

### MLP arxitekturasi

```
Input Layer       Hidden Layer 1     Hidden Layer 2    Output Layer
    [x₁]                [h₁₁]               [h₂₁]
    [x₂]    ──W₁,b₁──>  [h₁₂]   ──W₂,b₂──> [h₂₂]   ──W₃,b₃──> [y]
    [x₃]                [h₁₃]               [h₂₃]
    [x₄]                [h₁₄]

input shape: (n,)
W₁ shape: (hidden_1, n)
W₂ shape: (hidden_2, hidden_1)
W₃ shape: (1, hidden_2)
```

### Loss functions

| Task | Loss | Formula |
|------|------|---------|
| Regression | **MSE** | `mean((y - ŷ)²)` |
| Regression | **MAE** | `mean(|y - ŷ|)` |
| Binary Class. | **BCE** | `-mean(y·log(ŷ) + (1-y)·log(1-ŷ))` |
| Multi-class | **CCE** | `-mean(Σ yᵢ·log(ŷᵢ))` |

### Backpropagation — gradient'larni "orqaga" tarqatish

```
Forward:  input → ... → output → loss
                                  │
Backward: ∂loss/∂w ← ... ← ∂loss/∂a ← ─┘

Chain rule:
∂L/∂w = ∂L/∂a × ∂a/∂z × ∂z/∂w
```

PyTorch/TensorFlow'da bu **avtomatik**(autograd). Lekin intuition'ni bilish muhim.

### Optimizer'lar

| Optimizer | Description | Default LR |
|-----------|-------------|------------|
| **SGD** | Vanilla gradient descent | 0.01 |
| **SGD + Momentum** | Inertsiya qo'shilgan | 0.01, momentum=0.9 |
| **Adam** | Adaptive, default choice | 0.001 |
| **AdamW** | Adam + better weight decay | 0.001 |
| **RMSprop** | Adaptive learning rate | 0.001 |

**Maslahat:**`Adam` yoki `AdamW` bilan boshlang. Tuning vaqti kelganda boshqalarni sinab ko'ring.

## Kod misollari

### Pure NumPy bilan MLP (intuition uchun)

```python
import numpy as np

class SimpleMLP:
    def __init__(self, input_size, hidden_size, output_size):
        # Xavier initialization
        self.W1 = np.random.randn(hidden_size, input_size) * np.sqrt(2 / input_size)
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(output_size, hidden_size) * np.sqrt(2 / hidden_size)
        self.b2 = np.zeros(output_size)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def softmax(self, x):
        # Numerical stability
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / exp_x.sum(axis=1, keepdims=True)
    
    def forward(self, X):
        # X shape: (batch, input_size)
        self.z1 = X @ self.W1.T + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.a1 @ self.W2.T + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    def backward(self, X, y_true, learning_rate=0.01):
        # y_true: one-hot encoded
        batch_size = X.shape[0]
        
        # Output layer gradient
        dz2 = (self.a2 - y_true) / batch_size
        dW2 = dz2.T @ self.a1
        db2 = dz2.sum(axis=0)
        
        # Hidden layer gradient
        da1 = dz2 @ self.W2
        dz1 = da1 * self.relu_derivative(self.z1)
        dW1 = dz1.T @ X
        db1 = dz1.sum(axis=0)
        
        # Update weights
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
    
    def train(self, X, y, epochs=100, batch_size=32, learning_rate=0.01):
        for epoch in range(epochs):
            # Mini-batch
            indices = np.random.permutation(len(X))
            for start in range(0, len(X), batch_size):
                batch_idx = indices[start:start + batch_size]
                X_batch = X[batch_idx]
                y_batch = y[batch_idx]
                
                self.forward(X_batch)
                self.backward(X_batch, y_batch, learning_rate)
            
            # Track loss
            y_pred = self.forward(X)
            loss = -np.mean(np.sum(y * np.log(y_pred + 1e-9), axis=1))
            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Loss = {loss:.4f}")

# Misol — Iris (3-class)
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)
y_onehot = np.eye(3)[y]

model = SimpleMLP(input_size=4, hidden_size=16, output_size=3)
model.train(X, y_onehot, epochs=200, batch_size=16, learning_rate=0.05)
```

### PyTorch'da bir xil narsa — ANSALCO sodda

```python
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x  # logits (softmax loss ichida)

model = SimpleMLP(4, 16, 3)
optimizer = optim.Adam(model.parameters(), lr=0.05)
loss_fn = nn.CrossEntropyLoss()

X_t = torch.tensor(X, dtype=torch.float32)
y_t = torch.tensor(y, dtype=torch.long)

for epoch in range(200):
    optimizer.zero_grad()
    logits = model(X_t)
    loss = loss_fn(logits, y_t)
    loss.backward()           # backprop avtomatik
    optimizer.step()
    
    if epoch % 20 == 0:
        accuracy = (logits.argmax(dim=1) == y_t).float().mean()
        print(f"Epoch {epoch}: Loss={loss.item():.4f}, Acc={accuracy.item():.4f}")
```

**Diqqat:**Bir xil natija — `pure NumPy` 60 qator, `PyTorch` 20 qator. **Productivity = framework**.

## Backend integratsiyasi

Hozircha (asoslar) — bu bob nazariy. Production deployment haqida [PyTorch bobi](./02-pytorch-basics.md) va Oy 6 MLOps'da batafsil.

Lekin **mental model**: NN — bu **matematik function**. Backend dev sifatida siz har doim:
- `input` → `output` (REST API ham xuddi shunday)
- Stateless (weights — bu function parametri)
- Versioning kerak (model_v1.pt, model_v2.pt)
- Monitoring (latency, prediction distribution)

## Resurslar

- **3Blue1Brown — Neural Networks playlist**([YouTube](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)) — vizual, **MUST WATCH**
- **Andrew Ng — Deep Learning Specialization (Course 1)** — nazariy asoslar
- **"Neural Networks and Deep Learning"** — Michael Nielsen (bepul: [neuralnetworksanddeeplearning.com](http://neuralnetworksanddeeplearning.com/))
- **Andrej Karpathy — "Neural Networks: Zero to Hero"**(YouTube) — kuchli amaliy course
- **fast.ai — Practical Deep Learning**(bepul kurs)

## 🏋️ Mashqlar

### 🟢 Easy
1. Sigmoid, ReLU, Tanh funksiyalarini Matplotlib bilan chizing.
2. `2x + 1` linear function uchun MSE loss'ni minimize qiluvchi `w` va `b` ni gradient descent bilan toping.
3. PyTorch'da `nn.Linear(10, 1)` yarating va random tensor uchun forward pass ishlatib ko'ring.

### 🟡 Medium
1. **NumPy MLP**: yuqoridagi kodni Iris dataset'da 90%+ accuracy gacha sozlang.
2. **XOR problem**: 2 layer MLP bilan XOR problem'ni hal qiling.
3. **PyTorch vs Numpy speed**: 1M parametrli model uchun training time'ni solishtiring.

### 🔴 Hard
1. **From-scratch backprop** — 3 hidden layer'li MLP, dropout, batchnorm — hammasini pure NumPy'da.
2. **Visualize**: PyTorch model'ning loss landscape'ini chizing (2 ta weight bo'yicha 3D plot).

## Capstone

`notebooks/month-03/01_neural_network_scratch.ipynb`:
- Numpy bilan 2-layer MLP yozing
- MNIST'ning kichik sample (1000 sample, 10 class) ga train qiling
- Bir xil narsani PyTorch'da yozing
- Accuracy va training time'ni solishtiring

## ✅ Tekshirish ro'yxati

- [ ] Perceptron va MLP farqini bilaman
- [ ] ReLU, Sigmoid, Softmax qachon ishlatishni bilaman
- [ ] Forward pass va Backprop intuition'ni tushunaman
- [ ] Gradient Descent, SGD, Adam farqini bilaman
- [ ] CrossEntropy va MSE qachon ishlatishni bilaman
- [ ] PyTorch'da oddiy `nn.Module` yozaman
- [ ] Pure NumPy bilan oddiy MLP qurishni bilaman

[PyTorch asoslari](./02-pytorch-basics.md) ga o'tamiz.
