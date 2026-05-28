# PyTorch asoslari

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- PyTorch'ning tensor, autograd, nn.Module, DataLoader API'larini bilasiz
- O'z modelingizni `nn.Module` orqali yarata olasiz
- To'liq training loop yoza olasiz (CPU yoki GPU'da)
- Modelni saqlash, yuklash va inference qilishni bilasiz
- Production'ga olib chiqish (`torch.jit`, ONNX) bilan tanishasiz

## 📖 Nimani o'rganish kerak

- **Tensor** — NumPy ndarray + GPU support + autograd
- **Autograd** — avtomatik differentsiya
- **nn.Module** — model qurish
- **nn.Linear, nn.Conv2d, nn.RNN** — qatlamlar
- **Loss functions** — `nn.MSELoss`, `nn.CrossEntropyLoss`, va h.k.
- **Optimizers** — `optim.SGD`, `optim.Adam`
- **Dataset va DataLoader** — batch loading
- **Device management** — CPU/GPU/MPS
- **Saqlash/yuklash** — `state_dict`
- **TorchScript** — production export

## 📦 Kutubxonalar

```bash
# CPU
pip install torch torchvision torchaudio

# CUDA 12.1 (NVIDIA GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Mac M1/M2/M3 — default install MPS bilan ishlaydi
```

Tekshirish:
```python
import torch
print(torch.__version__)
print(torch.cuda.is_available())     # NVIDIA GPU
print(torch.backends.mps.is_available())  # Mac
```

## 🧠 Muhim mavzular

### Tensor — PyTorch'ning yuragi

```python
import torch

# Yaratish
a = torch.tensor([1, 2, 3])              # int64
b = torch.tensor([1.0, 2.0, 3.0])        # float32
c = torch.zeros(3, 4)                    # 3x4 nollar
d = torch.randn(2, 3)                    # normal random
e = torch.arange(10)                     # [0..9]

# NumPy'dan
import numpy as np
arr = np.array([1, 2, 3])
t = torch.from_numpy(arr)                # share memory!
arr_back = t.numpy()                     # share memory!

# Atributlar
print(a.shape, a.dtype, a.device)        # torch.Size([3]) torch.int64 cpu
```

### Device management

```python
# Eng yaxshi device avtomatik
device = "cuda" if torch.cuda.is_available() else (
    "mps" if torch.backends.mps.is_available() else "cpu"
)

# Tensor'ni device'ga ko'chirish
x = torch.randn(1000, 1000).to(device)
model = MyModel().to(device)

# Diqqat: ikkala tensor bir device'da bo'lishi kerak
# y = x @ y  # ❌ agar y CPU'da bo'lsa
# y = x @ y.to(device)  # ✅
```

### Autograd — magic

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1     # y = x² + 3x + 1
y.backward()                # dy/dx = 2x + 3
print(x.grad)               # tensor(7.0)  ← x=2 da 2*2+3=7

# Asosiy mexanizm — computational graph quriladi va backward chaqirilganda
# har x uchun gradient hisoblanadi
```

### nn.Module pattern

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.3)
        self.activation = nn.ReLU()
    
    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.dropout(x)
        x = self.activation(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

model = MyModel(input_dim=784, hidden_dim=256, output_dim=10)
print(model)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

### Dataset va DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class CSVDataset(Dataset):
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        self.X = torch.tensor(df.drop("target", axis=1).values, dtype=torch.float32)
        self.y = torch.tensor(df["target"].values, dtype=torch.long)
    
    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_dataset = CSVDataset("train.csv")
train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,       # parallel data loading
    pin_memory=True,     # GPU uchun tez
)
```

## 💻 Kod misollari

### To'liq training loop

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"

# Model
model = MyModel(784, 256, 10).to(device)

# Loss va optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

# Training loop
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, total_correct, total = 0, 0, 0
    
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * X.size(0)
        total_correct += (logits.argmax(dim=1) == y).sum().item()
        total += X.size(0)
    
    return total_loss / total, total_correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, total_correct, total = 0, 0, 0
    
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        logits = model(X)
        loss = criterion(logits, y)
        
        total_loss += loss.item() * X.size(0)
        total_correct += (logits.argmax(dim=1) == y).sum().item()
        total += X.size(0)
    
    return total_loss / total, total_correct / total

# Trening
EPOCHS = 20
for epoch in range(EPOCHS):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    val_loss, val_acc = evaluate(model, val_loader, criterion, device)
    
    print(f"Epoch {epoch+1}/{EPOCHS}  "
          f"Train: loss={train_loss:.4f}, acc={train_acc:.4f}  "
          f"Val: loss={val_loss:.4f}, acc={val_acc:.4f}")
```

### Modelni saqlash va yuklash

```python
# Faqat weights (RECOMMENDED)
torch.save(model.state_dict(), "model.pt")

# Yuklash
model = MyModel(784, 256, 10)
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()

# To'liq checkpoint (resuming training uchun)
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "loss": loss,
}, "checkpoint.pt")

checkpoint = torch.load("checkpoint.pt")
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
```

### TorchScript — production export

```python
# Tracing (input examples kerak)
example_input = torch.randn(1, 784).to(device)
traced_model = torch.jit.trace(model, example_input)
traced_model.save("model_traced.pt")

# Scripting (full Python control flow)
scripted_model = torch.jit.script(model)
scripted_model.save("model_scripted.pt")

# Yuklash (Python kerakmas!)
loaded = torch.jit.load("model_traced.pt")
output = loaded(torch.randn(1, 784))
```

### ONNX export

```python
torch.onnx.export(
    model,
    example_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    opset_version=17,
)

# ONNX Runtime'da yuklash
import onnxruntime as ort
sess = ort.InferenceSession("model.onnx")
output = sess.run(None, {"input": input_array})[0]
```

## 🔌 Backend integratsiyasi

### FastAPI'da PyTorch model

```python
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.device = "cuda" if torch.cuda.is_available() else "cpu"
    app.state.model = MyModel(784, 256, 10).to(app.state.device)
    app.state.model.load_state_dict(torch.load("model.pt", map_location=app.state.device))
    app.state.model.eval()
    yield

app = FastAPI(lifespan=lifespan)

class Input(BaseModel):
    features: list[float]  # 784 elements

@app.post("/predict")
@torch.no_grad()
def predict(data: Input):
    X = torch.tensor([data.features], dtype=torch.float32).to(app.state.device)
    logits = app.state.model(X)
    probs = torch.softmax(logits, dim=1)
    pred_class = probs.argmax(dim=1).item()
    confidence = probs[0, pred_class].item()
    return {"class": pred_class, "confidence": confidence}
```

### Batch prediction (samarali)

```python
@app.post("/predict/batch")
@torch.no_grad()
def predict_batch(items: list[Input]):
    X = torch.tensor([item.features for item in items], dtype=torch.float32).to(device)
    logits = app.state.model(X)
    probs = torch.softmax(logits, dim=1)
    return [
        {"class": int(p.argmax().item()), "confidence": float(p.max().item())}
        for p in probs
    ]
```

### Production tips

1. **`model.eval()`** — Dropout va BatchNorm production'da boshqacha ishlaydi
2. **`torch.no_grad()`** — gradient tracking o'chiriladi (tez + memory)
3. **`torch.inference_mode()`** — `no_grad` + bonus optimizatsiya
4. **Batching** — bitta request'ga 64 ta input — GPU yaxshiroq foydalanadi
5. **TorchServe** — production'da batching, versioning, A/B test (Oy 6)
6. **Async serving** — `asyncio` + `to_thread` (CPU bound) yoki Triton/BentoML

## 📚 Resurslar

- **PyTorch tutorials** — [pytorch.org/tutorials](https://pytorch.org/tutorials/)
- **"Deep Learning with PyTorch"** — Eli Stevens (free PDF: [pytorch.org/deep-learning-with-pytorch](https://pytorch.org/deep-learning-with-pytorch))
- **PyTorch Lightning** — wrapper kichikroq boilerplate uchun
- **Karpathy — "Let's build GPT"** (YouTube) — PyTorch chuqur
- **Hugging Face Course** — PyTorch transformer'lar uchun

## 🏋️ Mashqlar

### 🟢 Easy
1. `torch.randn(3, 4)` tensor yarating, transpose, sum, mean qiling.
2. `requires_grad=True` bilan `f(x) = x³` ning x=3 dagi gradient'ini toping.
3. `nn.Linear(10, 1)` yarating, forward pass, parametrlar sonini chiqaring.

### 🟡 Medium
1. **MNIST MLP**: 2-layer MLP bilan MNIST'da 95%+ accuracy oling.
2. **Custom dataset**: o'zingiz CSV bilan `Dataset` class yarating.
3. **GPU check**: model'ni CPU va GPU'da treninga solib, vaqt farqini o'lchang.

### 🔴 Hard
1. **FastAPI + PyTorch service**: MNIST classifier, image upload, prediction qaytaradi. Docker bilan.
2. **TorchScript benchmark**: oddiy model va TorchScript versiyasini latency bo'yicha solishtiring (`timeit`).
3. **Multi-GPU**: `nn.DataParallel` yoki `DistributedDataParallel` bilan 2+ GPU'da train (Colab Pro yoki Kaggle bilan).

## 🚀 Capstone

`notebooks/month-03/02_pytorch_mnist.ipynb`:
- MNIST datasetni `torchvision.datasets` orqali yuklang
- 3-layer MLP yozing
- Train + Validation loop
- Test set'da 97%+ accuracy
- Confusion matrix
- Eng yomon misollarni vizualizatsiya qiling
- Modelni TorchScript'ga export qiling
- FastAPI endpoint yarating

## ✅ Tekshirish ro'yxati

- [ ] Tensor yaratish, operatsiyalar, device ko'chirish
- [ ] Autograd asoslari (requires_grad, backward, grad)
- [ ] `nn.Module` subclassing
- [ ] DataLoader bilan batch loading
- [ ] Training loop yozish (train + eval mode, zero_grad, optimizer.step)
- [ ] Modelni saqlash va yuklash (state_dict)
- [ ] TorchScript yoki ONNX export
- [ ] FastAPI'da PyTorch serving

[TensorFlow va Keras](./03-tensorflow-keras.md) ga o'tamiz.
