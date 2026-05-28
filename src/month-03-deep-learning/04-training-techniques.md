# Training texnikalari

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Neural network'larni samarali train qilish texnikalarini bilasiz
- Overfitting bilan kurashish vositalarini (Dropout, BatchNorm, regularization) ishlatasiz
- Learning rate scheduling, gradient clipping, mixed precision'ni qo'llay olasiz
- Transfer learning bilan kichik datasetda ham yaxshi natija olasiz

## Nimani o'rganish kerak

- **Regularization**: L1/L2 (weight decay), Dropout, BatchNorm, LayerNorm
- **Initialization**: Xavier (Glorot), He, Kaiming
- **Optimizers**chuqurroq: SGD+momentum, Adam, AdamW, LAMB
- **Learning rate scheduling**: StepLR, CosineAnnealingLR, OneCycleLR, ReduceLROnPlateau
- **Gradient clipping** — gradient explosion'dan himoya
- **Mixed precision training**(FP16/BF16) — tezroq + kam memory
- **Data augmentation** — sun'iy ravishda dataset kengaytirish
- **Transfer learning** — pretrained model'larni qayta ishlatish
- **Early stopping va checkpointing**
- **Weights & Biases / TensorBoard** — experiment tracking

## Kutubxonalar

```bash
pip install torch torchvision wandb tensorboard
```

## Muhim mavzular

### Regularization texnikalari

#### Dropout
Trening paytida tasodifiy neuron'larni "o'chirib" qo'yish — overfitting'ning oldini olish.

```python
import torch.nn as nn

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.dropout = nn.Dropout(p=0.5)  # 50% neuron o'chiriladi
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return x

# Eval mode'da dropout avtomatik o'chadi (`.eval()` chaqirilganda)
```

#### Batch Normalization
Har batch'da activation'larni normallashtirish — tezroq konvergentsiya + regulyarizatsiya effekti.

```python
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.bn1 = nn.BatchNorm1d(256)  # 1D BN (MLP uchun)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = torch.relu(x)
        return x

# CNN uchun: nn.BatchNorm2d
# Transformer uchun: nn.LayerNorm (LayerNorm ko'proq mos)
```

#### Weight Decay (L2)
Optimizer'da `weight_decay` parametri.

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

### Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import (
    StepLR, CosineAnnealingLR, OneCycleLR, ReduceLROnPlateau,
)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Variant 1: Step decay (har N epoch'da gamma marta kamayadi)
scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

# Variant 2: Cosine annealing (silliq tushish)
scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS)

# Variant 3: OneCycleLR (warmup + decay) — Karpathy's favorite
scheduler = OneCycleLR(optimizer, max_lr=1e-2, total_steps=EPOCHS * len(train_loader))

# Variant 4: ReduceLROnPlateau (val loss yaxshilanmasa)
scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=3)

# Trening loop'da
for epoch in range(EPOCHS):
    train_one_epoch(...)
    scheduler.step()         # epoch oxirida (yoki ReduceLROnPlateau uchun: scheduler.step(val_loss))
```

### Gradient Clipping

Gradient'lar juda katta bo'lganda training "portlamaydi":

```python
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

Ayniqsa **RNN/LSTM**va **Transformer**training'da kerak.

### Mixed Precision Training

GPU memory'ni 2x ga tushiradi, tezligi 2-3x ga oshiradi.

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for X, y in loader:
    X, y = X.cuda(), y.cuda()
    
    with autocast(dtype=torch.float16):
        logits = model(X)
        loss = criterion(logits, y)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()
```

### Data Augmentation (Image uchun)

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Test uchun augmentation YO'Q
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
```

### Transfer Learning

```python
import torchvision.models as models

# Pretrained ResNet-18
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Variant 1: Faqat oxirgi qatlamni qayta o'rgatish (feature extraction)
for param in model.parameters():
    param.requires_grad = False  # barchasini freeze

model.fc = nn.Linear(model.fc.in_features, num_classes)  # yangi classifier
# Faqat model.fc.parameters() train bo'ladi

# Variant 2: Fine-tuning (barchasini train, kichik LR bilan)
optimizer = torch.optim.AdamW([
    {"params": model.layer1.parameters(), "lr": 1e-5},  # eski layer'lar — past LR
    {"params": model.layer4.parameters(), "lr": 1e-4},
    {"params": model.fc.parameters(), "lr": 1e-3},      # yangi layer — yuqori LR
])
```

## Kod misollari

### To'liq training pipeline (production-ready)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.cuda.amp import autocast, GradScaler

def train_model(
    model, train_loader, val_loader,
    epochs=20, lr=1e-3, weight_decay=1e-4,
    grad_clip=1.0, use_amp=True,
    save_path="best.pt",
):
    device = next(model.parameters()).device
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs)
    scaler = GradScaler() if use_amp else None
    
    best_val_acc = 0
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        for X, y in train_loader:
            X, y = X.to(device), y.to(device)
            optimizer.zero_grad()
            
            if use_amp:
                with autocast():
                    logits = model(X)
                    loss = criterion(logits, y)
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
                scaler.step(optimizer)
                scaler.update()
            else:
                logits = model(X)
                loss = criterion(logits, y)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
                optimizer.step()
            
            train_loss += loss.item()
        
        scheduler.step()
        
        # Validate
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for X, y in val_loader:
                X, y = X.to(device), y.to(device)
                logits = model(X)
                val_correct += (logits.argmax(dim=1) == y).sum().item()
                val_total += y.size(0)
        
        val_acc = val_correct / val_total
        print(f"Epoch {epoch+1}/{epochs}  "
              f"train_loss={train_loss/len(train_loader):.4f}  "
              f"val_acc={val_acc:.4f}  "
              f"lr={optimizer.param_groups[0]['lr']:.6f}")
        
        # Save best
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), save_path)
    
    return best_val_acc
```

### Weights & Biases integratsiyasi

```python
import wandb

wandb.init(project="my-ml-project", config={
    "lr": 1e-3,
    "batch_size": 64,
    "epochs": 20,
    "architecture": "ResNet-18",
})

# Training loop ichida
wandb.log({
    "train_loss": train_loss,
    "val_acc": val_acc,
    "lr": optimizer.param_groups[0]["lr"],
}, step=epoch)

wandb.finish()
```

### TensorBoard integratsiyasi

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/experiment_1")

for epoch in range(epochs):
    # ... training ...
    writer.add_scalar("Loss/train", train_loss, epoch)
    writer.add_scalar("Accuracy/val", val_acc, epoch)
    writer.add_histogram("fc.weights", model.fc.weight, epoch)

writer.close()

# $ tensorboard --logdir=runs
```

### Transfer Learning to'liq misol

```python
import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 1. Pretrained ResNet
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Freeze backbone
for param in model.parameters():
    param.requires_grad = False

# Yangi classifier (kasllar uchun 10 ta class)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, 10),
)

# 2. Faqat fc parametrlari uchun optimizer
optimizer = torch.optim.AdamW(model.fc.parameters(), lr=1e-3)

# 3. Train (faqat fc)
train_model(model, train_loader, val_loader, epochs=5, lr=1e-3)

# 4. Unfreeze va fine-tune (kichik LR)
for param in model.parameters():
    param.requires_grad = True

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
train_model(model, train_loader, val_loader, epochs=10, lr=1e-5)
```

## Backend integratsiyasi

### Training service (background job)

```python
from celery import Celery
import torch

celery_app = Celery("training", broker="redis://localhost:6379")

@celery_app.task(bind=True)
def train_model_task(self, dataset_path, hyperparams):
    # Progress tracking
    def on_epoch_end(epoch, val_acc):
        self.update_state(
            state="PROGRESS",
            meta={"epoch": epoch, "val_acc": val_acc},
        )
    
    model = create_model()
    train_loader, val_loader = create_loaders(dataset_path, hyperparams["batch_size"])
    
    best_acc = train_model(model, train_loader, val_loader, **hyperparams, 
                            on_epoch_end=on_epoch_end)
    
    # Save to S3 or local
    model_path = f"models/run_{self.request.id}.pt"
    torch.save(model.state_dict(), model_path)
    
    return {"best_acc": best_acc, "model_path": model_path}

# FastAPI endpoint
@app.post("/train")
def start_training(dataset_path: str, epochs: int = 20):
    task = train_model_task.delay(dataset_path, {"epochs": epochs, "batch_size": 64, "lr": 1e-3})
    return {"task_id": task.id}

@app.get("/train/{task_id}")
def get_training_status(task_id: str):
    task = train_model_task.AsyncResult(task_id)
    return {
        "state": task.state,
        "info": task.info if task.info else {},
    }
```

## Resurslar

- **PyTorch tutorials — Training techniques**([link](https://pytorch.org/tutorials/))
- **"Bag of Tricks for Image Classification with CNNs"** — paper (training improvements)
- **Andrej Karpathy — "A Recipe for Training Neural Networks"**(blog)
- **Weights & Biases — Best Practices**courses
- **OneCycleLR — Leslie Smith paper**

## 🏋️ Mashqlar

### 🟢 Easy
1. MLP'da Dropout qo'shing, train accuracy va val accuracy farqini ko'ring.
2. Adam va SGD'ni bir xil modelda solishtiring.
3. ReduceLROnPlateau qo'shing, plateau'ni vizual ko'ring.

### 🟡 Medium
1. **Mixed precision**: bir xil training'ni FP32 va AMP bilan ishlating, vaqt va memory farqi.
2. **Augmentation**: oddiy CNN'da augmentation bilan va usiz solishtiring (CIFAR-10).
3. **Transfer learning**: 100 ta rasmli kichik dataset'da pretrained ResNet bilan 90%+ accuracy oling.

### 🔴 Hard
1. **Custom LR scheduler**: warmup + cosine annealing kombinatsiyali scheduler yozing.
2. **Hyperparameter sweep**: Optuna yoki wandb sweeps bilan 50 ta trial, eng yaxshi konfiguratsiyani toping.
3. **Production training service**: Celery + FastAPI + S3 + W&B — to'liq pipeline.

## Capstone

`notebooks/month-03/04_training_techniques.ipynb`:
- CIFAR-10 datasetda 2 ta variantni solishtiring:
 - Baseline: oddiy CNN, Adam, no augmentation
 - Improved: BatchNorm + Dropout + augmentation + OneCycleLR + AMP
- Wandb yoki TensorBoard'da loglar
- Test accuracy: baseline ~70%, improved 85%+

## ✅ Tekshirish ro'yxati

- [ ] Dropout, BatchNorm qachon ishlatishni bilaman
- [ ] Adam vs AdamW farqini bilaman (weight decay)
- [ ] Learning rate scheduling turlarini bilaman
- [ ] Gradient clipping qachon kerakligini bilaman
- [ ] Mixed precision training (AMP)ni qo'llay olaman
- [ ] Data augmentation (vision) ni ishlataman
- [ ] Transfer learning bilan kichik dataset'da yaxshi natija olaman
- [ ] W&B yoki TensorBoard bilan experiment tracking qilaman

[CNN — Convolutional Networks](./05-cnn.md) ga o'tamiz.
