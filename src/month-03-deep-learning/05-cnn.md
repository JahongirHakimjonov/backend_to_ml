# CNN — Convolutional Networks

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Convolution operatsiyasi va uning intuition'ini tushunasiz
- Pooling, padding, stride'ni bilasiz
- Klassik CNN arxitekturalarini (LeNet, AlexNet, VGG, ResNet, EfficientNet) bilasiz
- O'z CNN'ingizni yarata olasiz va image classification qila olasiz
- Pretrained CNN'larni transfer learning bilan qo'llay olasiz

## Nimani o'rganish kerak

- **Convolution operatsiyasi** — kernel, stride, padding
- **Pooling** — Max, Average, Global Average
- **Feature maps** — convolutional output'lar
- **Receptive field**
- **CNN arxitekturalari**: LeNet, AlexNet, VGG, ResNet, Inception, MobileNet, EfficientNet
- **Skip connections (ResNet)** — chuqurroq tarmoqlarni o'rgatish
- **Inception modules** — multi-scale features
- **Depthwise separable convolutions**(MobileNet) — kichik modellar
- **Data augmentation** — image augmentation
- **timm** — pretrained models hub

## Kutubxonalar

```bash
pip install torch torchvision timm pillow albumentations
```

- **torchvision** — pretrained models, transforms
- **timm** — PyTorch Image Models (1000+ model arxitekturalar)
- **albumentations** — kuchli image augmentation

## Muhim mavzular

### Convolution intuition

```
Image (5x5):           Kernel (3x3):          Output (3x3):
1 1 1 0 0              1 0 1                  4 3 4
0 1 1 1 0              0 1 0                  2 4 3
0 0 1 1 1     conv      1 0 1     =          2 3 4
0 0 1 1 0              
0 1 1 0 0              (sum of element-wise products in 3x3 window)
```

**Nima uchun CNN?**
1. **Translation invariance** — obekt qaerda bo'lishidan qat'i nazar topadi
2. **Parameter sharing** — bitta kernel butun rasm bo'ylab
3. **Spatial hierarchy** — quyi qatlamlar: edges, yuqori qatlamlar: complex shapes

### Pooling

```
Max Pooling (2x2, stride=2):

Input (4x4):              Output (2x2):
1 3 2 4                   3 4
5 6 1 2     ───>          6 8
7 8 4 3                   
1 2 5 6                   8 6
```

Maqsad: dimensionality kamaytirish + translation invariance + overfitting'ni kamaytirish.

### Padding va Stride

- **Padding** — chetlarga `0` qo'shish (spatial dimensions saqlanadi)
- **Stride** — kernel necha pixel ko'chadi (1 = har pixel, 2 = har 2-pixel)

Formula:
```
output_size = (input_size + 2*padding - kernel_size) / stride + 1
```

### Klassik arxitekturalar

| Yil | Arxitektura | Asosiy g'oya | Parametrlar |
|-----|-------------|--------------|-------------|
| 1998 | **LeNet-5** | Birinchi muvaffaqiyatli CNN | 60K |
| 2012 | **AlexNet** | ReLU, Dropout, GPU | 60M |
| 2014 | **VGG-16** | Faqat 3x3 kernel, chuqurroq | 138M |
| 2014 | **GoogLeNet/Inception** | Multi-scale features | 7M |
| 2015 | **ResNet** | Skip connections, 152 layers | 25M+ |
| 2017 | **MobileNet** | Mobile-optimized | 4M |
| 2019 | **EfficientNet** | NAS optimized scaling | 5M-66M |
| 2020 | **ConvNeXt** | Modernized ResNet | 28M-198M |

### Skip Connections (ResNet) — chuqurroq tarmoqlar uchun ochilish

```
Oddiy:           ResNet:
x ──> [Conv] ──> y      x ──> [Conv] ──> z
                              │           ↑
                              └── ─ ─ ─ ─ +
                                  y = z + x
```

Skip connection vanishing gradient muammosini hal qiladi va 100+ qatlamli tarmoqlarni o'rgatish imkonini beradi.

## Kod misollari

### Oddiy CNN — CIFAR-10 uchun

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 32x32 -> 16x16
            
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 16x16 -> 8x8
            
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 8x8 -> 4x4
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),  # 4x4 -> 1x1
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN(num_classes=10)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")  # ~95K
```

### Image transforms va DataLoader

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Train transforms (augmentation bilan)
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

# Test transforms (NO augmentation)
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

train_dataset = datasets.CIFAR10("data/", train=True, download=True, transform=train_transform)
test_dataset = datasets.CIFAR10("data/", train=False, download=True, transform=test_transform)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, num_workers=4)
test_loader = DataLoader(test_dataset, batch_size=256, shuffle=False, num_workers=4)
```

### Pretrained ResNet — Transfer Learning

```python
import torchvision.models as models

# Pretrained ResNet-50
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Yangi classifier (masalan, 5 ta gul turi uchun)
num_classes = 5
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Freeze backbone, faqat fc trainable
for name, param in model.named_parameters():
    if "fc" not in name:
        param.requires_grad = False
```

### `timm` bilan modern arxitekturalar

```python
import timm

# Mavjud modellarni ko'rish
print(timm.list_models("efficientnet*"))

# EfficientNet-B3 pretrained
model = timm.create_model(
    "efficientnet_b3",
    pretrained=True,
    num_classes=10,  # avtomatik yangi classifier
)

# ConvNeXt
model = timm.create_model("convnext_base.fb_in22k_ft_in1k", pretrained=True, num_classes=10)
```

### Albumentations — kuchli augmentation

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

train_aug = A.Compose([
    A.Resize(256, 256),
    A.RandomCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.HueSaturationValue(p=0.3),
    A.OneOf([
        A.GaussianBlur(p=0.5),
        A.MotionBlur(p=0.5),
    ], p=0.2),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __getitem__(self, idx):
        image = cv2.imread(self.image_paths[idx])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image=image)["image"]
        
        return image, label
    
    def __len__(self):
        return len(self.labels)
```

### Grad-CAM — modelni interpretatsiya qilish

```python
import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Hook bilan feature maps va gradient'larni olish
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def __call__(self, x, class_idx):
        logits = self.model(x)
        self.model.zero_grad()
        logits[0, class_idx].backward()
        
        weights = self.gradients.mean(dim=[2, 3], keepdim=True)
        cam = (weights * self.activations).sum(dim=1).squeeze()
        cam = torch.relu(cam)
        cam = cam / cam.max()
        return cam.numpy()

model = models.resnet18(pretrained=True).eval()
gradcam = GradCAM(model, model.layer4[-1])
# heatmap = gradcam(input_image, predicted_class)
```

## Backend integratsiyasi

### Image classification API

```python
from fastapi import FastAPI, UploadFile
from PIL import Image
import torch
import io

app = FastAPI()

model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=1000).eval()
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ImageNet class labels
import json
imagenet_labels = json.load(open("imagenet_labels.json"))

@app.post("/classify")
@torch.no_grad()
async def classify_image(file: UploadFile):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    X = transform(image).unsqueeze(0)
    
    logits = model(X)
    probs = torch.softmax(logits, dim=1)
    
    # Top 5
    top5_probs, top5_indices = probs.topk(5, dim=1)
    
    return {
        "predictions": [
            {"class": imagenet_labels[idx.item()], "probability": prob.item()}
            for idx, prob in zip(top5_indices[0], top5_probs[0])
        ]
    }
```

### Optimization for production

```python
# 1. TorchScript — Python kerakmas
model_scripted = torch.jit.script(model)
model_scripted.save("model.pt")

# 2. Quantization — 4x kichik, 2-3x tez
import torch.quantization
model_quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# 3. ONNX export
torch.onnx.export(model, dummy_input, "model.onnx", opset_version=17)

# 4. Triton Inference Server (Oy 6'da batafsil)
```

## Resurslar

- **CS231n: CNN for Visual Recognition**(Stanford, bepul) — bibliya
- **PyTorch Vision tutorials** — [pytorch.org/tutorials](https://pytorch.org/tutorials/)
- **timm GitHub** — [github.com/huggingface/pytorch-image-models](https://github.com/huggingface/pytorch-image-models)
- **fast.ai Course** — practical CV
- **"Deep Learning for Computer Vision"** — Adrian Rosebrock

## 🏋️ Mashqlar

### 🟢 Easy
1. SimpleCNN'ni CIFAR-10'da 5 epoch train qiling, accuracy chiqaring.
2. `nn.Conv2d` parametrlari (in_channels, out_channels, kernel_size, padding, stride) ni o'zgartirib output shape'ni hisoblang.
3. Pretrained ResNet-18 ni yuklang, ImageNet rasmda inference qiling.

### 🟡 Medium
1. **CIFAR-10**: SimpleCNN'ni augmentation va BatchNorm bilan train qilib, 85%+ accuracy oling.
2. **Transfer Learning**: 100 ta rasmli kichik dataset (masalan, Kaggle'dan biror gul tasnifi) — pretrained ResNet bilan 90%+ accuracy.
3. **Grad-CAM**: ResNet'ning qaror qabul qilish jarayonini vizualizatsiya qiling.

### 🔴 Hard
1. **Image classification API**: FastAPI + upload + EfficientNet — Docker'da. Batching support, async processing.
2. **Custom architecture**: ResNet-18'ni o'zingiz noldan implement qiling (skip connections bilan).
3. **Model optimization**: PyTorch model'ni ONNX'ga + quantization — original vs optimized model latency.

## Capstone

`notebooks/month-03/05_cnn_image_classification.ipynb`:
- **Kaggle — Intel Image Classification**(6 turdagi landshaftlar) yoki o'xshash dataset
- EDA + augmentation
- 2 ta model: (1) custom CNN noldan, (2) EfficientNet-B0 fine-tune
- Test accuracy: custom ~80%, EfficientNet 93%+
- Grad-CAM visualization
- FastAPI endpoint Docker'da

## ✅ Tekshirish ro'yxati

- [ ] Convolution operatsiyasini tushunaman
- [ ] Padding, stride, output_size formulasini bilaman
- [ ] Max va Average pooling farqi
- [ ] ResNet'ning skip connection g'oyasini bilaman
- [ ] `torchvision.models` va `timm` bilan pretrained model yuklayman
- [ ] Transfer learning'da freeze/unfreeze strategiyalarini bilaman
- [ ] Albumentations bilan image augmentation
- [ ] Image classification API qurganman

[RNN, LSTM, GRU](./06-rnn-lstm.md) ga o'tamiz.
