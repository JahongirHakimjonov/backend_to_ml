# Computer Vision ga kirish

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Computer Vision masalalarining 5 ta asosiy turini bilasiz
- Har masala uchun mos pretrained model'larni tanlay olasiz
- Rasm/video bilan ishlash uchun zarur tushunchalarni bilasiz
- Domain'ga mos CV pipeline qurishni rejalashtira olasiz

## Nimani o'rganish kerak

- **CV masala turlari** — classification, detection, segmentation, OCR, pose, generation
- **Image fundamentals** — pixel, channels, color spaces (RGB, BGR, HSV, Grayscale)
- **Image formats** — JPEG, PNG, WebP, TIFF
- **CV bo'yicha pretrained ekosistema** — torchvision, timm, MMDetection, Detectron2, Ultralytics
- **Edge cases** — rotation, occlusion, lighting, scale

## CV masalalarining 5 ta asosiy turi

### 1. Image Classification
- Bitta rasm → bitta label (yoki bir nechta label, multi-label)
- Model: ResNet, EfficientNet, ViT, ConvNeXt
- Misol: spam image, kasallik turi, mahsulot kategoriyasi

### 2. Object Detection
- Bitta rasm → bir nechta bounding box + label + confidence
- Model: YOLO, Faster R-CNN, DETR
- Misol: avtomobillarni hisoblash, xavfsizlik tahdidlari

### 3. Semantic / Instance / Panoptic Segmentation
- Pixel darajasida classification
- Model: U-Net, Mask R-CNN, SAM (Segment Anything Model)
- Misol: medical imaging, satellite analysis

### 4. OCR (Optical Character Recognition)
- Rasm → matn
- Model: Tesseract, EasyOCR, PaddleOCR, TrOCR
- Misol: ID kartlar, hujjatlar, receipts

### 5. Pose / Keypoint Estimation
- Inson tanasi yoki obyekt nuqtalarini topish
- Model: MediaPipe, OpenPose, MMPose
- Misol: sport analytics, AR filtrlar

### 6. Generative (bonus)
- Rasm yaratish/o'zgartirish
- Model: Stable Diffusion, DALL-E, ControlNet
- Misol: marketing assets, design tools

## Image fundamentals

### Pixel va Channels

```
RGB rasm (3 channel):
shape = (height, width, 3)
har pixel: [R, G, B] qiymatlari, har biri [0..255] (uint8) yoki [0..1] (float)

Grayscale (1 channel):
shape = (height, width)
har pixel: [0..255] (yorqinlik darajasi)

OpenCV o'qiganda BGR (not RGB)!
PIL/torchvision RGB ishlatadi
```

### Color spaces

| Space | Channels | Qachon |
|-------|----------|--------|
| **RGB** | Red, Green, Blue | Default display |
| **BGR** | Blue, Green, Red | OpenCV default |
| **Grayscale** | Yorqinlik | Edge detection, classification (kichik) |
| **HSV** | Hue, Saturation, Value | Color-based filtering |
| **YCrCb** | Luminance, Chroma | Video compression |
| **LAB** | Lightness, A, B | Color-aware processing |

### Image formats — qachon qaysi?

| Format | Lossy? | Transparency | Use case |
|--------|--------|--------------|----------|
| **JPEG** | Yes | No | Photos, web (kichik) |
| **PNG** | No | Yes | Logos, screenshots |
| **WebP** | Both | Yes | Web (modern, kichik) |
| **TIFF** | No (yoki Yes) | Yes | Print, scientific |
| **HEIC** | Yes | Yes | iPhone |
| **NPY** | No | N/A | ML pipeline (raw arrays) |

## Asosiy kutubxonalar

```bash
pip install opencv-python pillow numpy matplotlib
pip install torch torchvision timm
pip install ultralytics                  # YOLO
pip install easyocr paddleocr            # OCR
pip install mediapipe                    # Pose, hand tracking
pip install albumentations               # Augmentation
```

## Kod misollari

### Image yuklash va inspectsiya

```python
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# OpenCV (BGR)
img_cv = cv2.imread("photo.jpg")
print(img_cv.shape)         # (H, W, 3)
print(img_cv.dtype)         # uint8
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# PIL (RGB)
img_pil = Image.open("photo.jpg")
print(img_pil.size)         # (W, H) — diqqat: tartib boshqacha!

# matplotlib (RGB kutadi)
plt.imshow(img_rgb)
plt.axis("off")
plt.show()
```

### Rasm bilan asosiy operatsiyalar

```python
# Resize
resized = cv2.resize(img_cv, (224, 224))

# Crop
cropped = img_cv[100:400, 200:500]  # [y1:y2, x1:x2]

# Rotation
h, w = img_cv.shape[:2]
M = cv2.getRotationMatrix2D((w/2, h/2), angle=45, scale=1.0)
rotated = cv2.warpAffine(img_cv, M, (w, h))

# Flip
flipped = cv2.flip(img_cv, 1)  # 1=horizontal, 0=vertical, -1=both

# Color conversion
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
```

### CV pipeline tanlash — decision tree

```
Sizning masalangiz?
│
├── "Bu rasm nima?"
│   → Image Classification (ResNet/EfficientNet/ViT)
│
├── "Rasmda qaerda nima bor?"
│   → Object Detection (YOLO, Faster R-CNN)
│
├── "Har pixel qaysi obyektga tegishli?"
│   → Segmentation (U-Net, SAM)
│
├── "Bu rasmda qanday matn yozilgan?"
│   → OCR (Tesseract, EasyOCR, PaddleOCR)
│
├── "Insondan keypoint'larni topish"
│   → Pose Estimation (MediaPipe, OpenPose)
│
└── "Rasm yaratish/o'zgartirish"
    → Generative (Stable Diffusion)
```

## Backend integratsiyasi — umumiy patternlar

### 1. Image upload endpoint

```python
from fastapi import FastAPI, UploadFile
from PIL import Image
import io

app = FastAPI()

@app.post("/process-image")
async def process_image(file: UploadFile):
    # Validation
    if not file.content_type.startswith("image/"):
        return {"error": "Not an image"}
    
    # Read
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Validate size
    if img.size[0] > 4000 or img.size[1] > 4000:
        return {"error": "Image too large"}
    
    # Process (CV pipeline)
    # ...
    
    return {"status": "ok", "size": img.size}
```

### 2. URL'dan rasm yuklash

```python
import httpx
from PIL import Image
import io

@app.post("/process-url")
async def process_url(url: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
    
    img = Image.open(io.BytesIO(response.content)).convert("RGB")
    # ...
```

### 3. Stream/Video processing

```python
import cv2

def process_video(video_path: str, output_path: str):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply model
        processed = some_model_inference(frame)
        out.write(processed)
    
    cap.release()
    out.release()
```

### 4. Async processing (Celery)

```python
@celery_app.task
def process_image_async(image_path: str):
    img = cv2.imread(image_path)
    
    # Heavy processing
    result = run_yolo(img)
    
    # Save result
    output_path = image_path.replace(".jpg", "_processed.jpg")
    cv2.imwrite(output_path, result)
    
    return {"output": output_path}

@app.post("/process-async")
async def process_async(file: UploadFile):
    # Save uploaded file
    path = f"/tmp/{uuid.uuid4()}.jpg"
    with open(path, "wb") as f:
        f.write(await file.read())
    
    # Queue task
    task = process_image_async.delay(path)
    return {"task_id": task.id}
```

## Resurslar

- **PyImageSearch** — [pyimagesearch.com](https://pyimagesearch.com/) — eng yaxshi CV blog
- **OpenCV docs** — [docs.opencv.org](https://docs.opencv.org/)
- **CS231n**(Stanford) — CV nazariyasi
- **Roboflow** — datasets va training (no-code)
- **MMDetection / Detectron2** — production-grade detection frameworks
- **HuggingFace Vision** — pretrained vision models

## 🏋️ Mashqlar

### 🟢 Easy
1. Rasm yuklang (OpenCV va PIL), shape va format'ni chiqaring.
2. RGB → Grayscale, RGB → HSV ga aylantiring va vizualizatsiya qiling.
3. Rasmni 224x224 ga resize qilib saqlang.

### 🟡 Medium
1. **Image gallery API**: FastAPI'da rasm upload, thumbnail (200x200) yaratish, EXIF metadata olish.
2. **Color analysis**: rasmdan dominant ranglarni K-Means bilan toping (Oy 2'dan).
3. **Pretrained classifier**: torchvision modeli bilan rasm uchun top-5 prediction.

### 🔴 Hard
1. **CV Pipeline Service**: FastAPI + Celery + Redis. Endpoint'lar:
 - Upload image
 - Resize / convert format
 - Apply pretrained model (classification/detection)
 - Webhook callback bilan async
2. **Real-time webcam**: FastAPI WebSocket + browser webcam → server'da YOLO → bounding box JSON qaytarish.

## Capstone

`notebooks/month-04/01_cv_intro.ipynb`:
- Custom dataset (200+ rasm) yuklang yoki Kaggle'dan oling
- 5 ta turli CV masalani bitta dataset uchun ishlatib chiqing:
 - Classification (pretrained)
 - Detection (YOLO)
 - Segmentation (SAM)
 - OCR (matn bor rasmlarda)
 - Pose (insonlar bor rasmlarda)

## ✅ Tekshirish ro'yxati

- [ ] CV ning 5+ ta asosiy masalalarini bilaman
- [ ] Image formats va color spaces farqini bilaman
- [ ] OpenCV va PIL ning farqini bilaman
- [ ] Pretrained model qachon va qaysi birini tanlashni bilaman
- [ ] Async image processing pipeline yaratishni rejalashtira olaman

[OpenCV bilan ishlash](./02-opencv.md) ga o'tamiz.
