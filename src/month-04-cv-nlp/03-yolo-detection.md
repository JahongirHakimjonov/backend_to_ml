# YOLO va Object Detection

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Object Detection masalasini Image Classification'dan farqlay olasiz
- YOLO ekosistemasini (v5, v8, v11) bilasiz
- Pretrained YOLO bilan inference qilasiz
- O'z datasetingiz uchun YOLO fine-tune qila olasiz
- Production'da object detection servisini deploy qilasiz
- Segmentation va OCR bilan ham tanish bo'lasiz

## Nimani o'rganish kerak

- **Detection**vs Classification vs Segmentation
- **Bounding box** — coordinates, IoU (Intersection over Union)
- **Anchor boxes, anchor-free detection**
- **NMS (Non-Maximum Suppression)**
- **YOLO arxitekturasi**evolyutsiyasi (v1 → v11)
- **mAP (mean Average Precision)** — detection metric
- **Annotation formats** — YOLO, COCO, Pascal VOC
- **Ultralytics ekosistemasi** — YOLOv8/v11 (PyTorch)
- **Segmentation** — instance (Mask R-CNN), semantic (DeepLab), SAM
- **OCR** — Tesseract, EasyOCR, PaddleOCR, TrOCR

## Kutubxonalar

```bash
pip install ultralytics                    # YOLO
pip install supervision                    # Detection helpers
pip install easyocr                        # OCR (multi-language)
pip install paddleocr paddlepaddle         # PaddleOCR (best for many languages)
pip install segment-anything-py            # SAM (Meta)
```

## Muhim mavzular

### Detection metric — mAP

- **IoU (Intersection over Union):**predicted va ground truth box'larining qoplanish darajasi
- **IoU > 0.5**odatda "true positive"
- **AP (Average Precision)**= bitta class uchun precision-recall curve area
- **mAP**= barcha class'lar bo'yicha o'rtacha
- **mAP@0.5:0.95**= IoU threshold'larini 0.5..0.95 oraliqda o'rtacha (COCO standard)

### YOLO evolyutsiyasi

| Version | Yil | Asosiy yangiliklar |
|---------|-----|-------------------|
| YOLOv1 | 2016 | Birinchi real-time detector |
| YOLOv3 | 2018 | Multi-scale detection |
| YOLOv4 | 2020 | Architectural improvements |
| YOLOv5 | 2020 | PyTorch, Ultralytics |
| YOLOv7 | 2022 | Re-parametrization |
| **YOLOv8** | 2023 | Detection+Segmentation+Pose+Classification |
| **YOLOv11** | 2024 | Faster + better accuracy |

**Maslahat:**YOLOv8 yoki YOLOv11 — production uchun eng yaxshi tanlov (Ultralytics).

### Annotation format'lari

**YOLO format**(eng oddiy):
```
# image1.txt — har qator: class_id x_center y_center width height (normallashtirilgan 0..1)
0 0.5 0.5 0.3 0.4
2 0.7 0.3 0.1 0.2
```

**COCO format**(JSON):
```json
{
  "images": [{"id": 1, "file_name": "image1.jpg", "width": 800, "height": 600}],
  "annotations": [
    {"image_id": 1, "category_id": 0, "bbox": [100, 200, 50, 80], "area": 4000}
  ],
  "categories": [{"id": 0, "name": "person"}]
}
```

## Kod misollari

### YOLOv8 — inference

```python
from ultralytics import YOLO

# Pretrained model (COCO dataset — 80 class)
model = YOLO("yolov8n.pt")  # n=nano, s=small, m=medium, l=large, x=xlarge

# Inference
results = model("path/to/image.jpg")

for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        cls = int(box.cls[0].item())
        cls_name = model.names[cls]
        print(f"{cls_name}: ({x1:.0f}, {y1:.0f})-({x2:.0f}, {y2:.0f}), conf={conf:.2f}")

# Vizualizatsiya
result.show()
result.save("output.jpg")
```

### Batch / video / webcam

```python
# Batch images
results = model(["img1.jpg", "img2.jpg", "img3.jpg"])

# Video file
results = model("video.mp4", save=True, project="runs", name="detection")

# Webcam (real-time)
results = model(source=0, show=True)

# URL
results = model("https://ultralytics.com/images/bus.jpg")
```

### Custom dataset uchun training

#### 1. Dataset tayyorlash (YOLO format)

```
my_dataset/
├── data.yaml
├── images/
│   ├── train/
│   │   ├── img001.jpg
│   │   └── ...
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    │   ├── img001.txt
    │   └── ...
    ├── val/
    └── test/
```

`data.yaml`:
```yaml
path: ./my_dataset
train: images/train
val: images/val
test: images/test

nc: 3  # number of classes
names: ['cat', 'dog', 'bird']
```

#### 2. Training

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # transfer learning'dan boshlash

results = model.train(
    data="my_dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,  # GPU index, "cpu" yoki "mps"
    patience=20,  # early stopping
    project="runs/train",
    name="my_experiment",
)

# Best model
best_model = YOLO("runs/train/my_experiment/weights/best.pt")
```

#### 3. Validation

```python
metrics = best_model.val(data="my_dataset/data.yaml")
print(metrics.box.map)       # mAP@0.5:0.95
print(metrics.box.map50)     # mAP@0.5
print(metrics.box.map75)     # mAP@0.75
```

### YOLO Segmentation

```python
# Segmentation modeli (suffix `-seg`)
model = YOLO("yolov8n-seg.pt")
results = model("image.jpg")

for r in results:
    masks = r.masks  # segmentation masks
    if masks is not None:
        for mask in masks:
            mask_array = mask.data[0].cpu().numpy()  # (H, W) binary
```

### SAM — Segment Anything Model (Meta)

```python
from segment_anything import sam_model_registry, SamPredictor
import cv2

# Pretrained SAM
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
predictor = SamPredictor(sam)

# Image
image = cv2.imread("image.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image_rgb)

# Point yoki box prompt
masks, scores, _ = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),  # 1=foreground, 0=background
    multimask_output=True,
)
# masks shape: (3, H, W) — 3 ta variant
```

### OCR — Tesseract

```python
import pytesseract
import cv2

img = cv2.imread("text.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Default English
text = pytesseract.image_to_string(gray)

# Multi-language (o'zbek lotin uchun "uzb")
text = pytesseract.image_to_string(gray, lang="uzb+eng+rus")

# Konfiguratsiya
custom_config = r"--oem 3 --psm 6"
text = pytesseract.image_to_string(gray, config=custom_config)

# Bounding box'lar bilan
data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
```

### OCR — EasyOCR (zamonaviy)

```python
import easyocr

# Bir nechta til (uzbek qo'shilmagan, lekin lotin yozuv ishlayishi mumkin)
reader = easyocr.Reader(['en', 'ru'])

result = reader.readtext("text.jpg")
for (bbox, text, prob) in result:
    print(f"Text: {text}, Confidence: {prob:.2f}")
```

### OCR — PaddleOCR (eng yaxshi multi-language)

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ru")  # uzbek yozuvlar uchun "ru" yoki "en"

result = ocr.ocr("text.jpg")
for line in result[0]:
    bbox, (text, conf) = line
    print(text, conf)
```

## Backend integratsiyasi

### Detection API (FastAPI + YOLO)

```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, Response
from contextlib import asynccontextmanager
from ultralytics import YOLO
import cv2
import numpy as np

@asynccontextmanager
async def lifespan(app):
    app.state.model = YOLO("yolov8n.pt")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/detect")
async def detect(file: UploadFile, conf_threshold: float = 0.25):
    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    results = app.state.model(img, conf=conf_threshold)
    detections = []
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append({
                "class": app.state.model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
            })
    
    return {"detections": detections, "count": len(detections)}


@app.post("/detect-image")
async def detect_image(file: UploadFile):
    """Annotated rasm qaytaradi."""
    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    results = app.state.model(img)
    annotated = results[0].plot()
    
    _, buf = cv2.imencode(".jpg", annotated)
    return Response(content=buf.tobytes(), media_type="image/jpeg")
```

### Async video processing (Celery)

```python
from celery import Celery

celery_app = Celery("detection", broker="redis://localhost:6379")

@celery_app.task(bind=True)
def detect_video(self, video_path: str):
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(video_path)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    all_detections = []
    
    for frame_idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame, verbose=False)
        frame_detections = []
        for box in results[0].boxes:
            frame_detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist(),
            })
        all_detections.append({"frame": frame_idx, "detections": frame_detections})
        
        # Progress
        if frame_idx % 30 == 0:
            self.update_state(state="PROGRESS", 
                              meta={"current": frame_idx, "total": total_frames})
    
    cap.release()
    return all_detections
```

### OCR + Detection combo (ID card scanner)

```python
@app.post("/scan-id-card")
async def scan_id_card(file: UploadFile):
    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    # 1. Detect ID card via custom YOLO model
    detections = id_card_detector(img)
    
    # 2. Crop ID card
    x1, y1, x2, y2 = detections[0]["bbox"]
    id_crop = img[y1:y2, x1:x2]
    
    # 3. Preprocess
    gray = cv2.cvtColor(id_crop, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.adaptiveThreshold(gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # 4. OCR
    text = pytesseract.image_to_string(enhanced, lang="uzb+eng")
    
    # 5. Parse fields (regex yoki ML)
    fields = parse_id_text(text)
    
    return fields
```

## Resurslar

- **Ultralytics docs** — [docs.ultralytics.com](https://docs.ultralytics.com/)
- **Roboflow Universe** — datasets + pretrained models
- **Supervision library** — [supervision.roboflow.com](https://supervision.roboflow.com/) (detection helpers)
- **Detectron2** — Facebook research detection framework
- **MMDetection** — OpenMMLab toolbox
- **PaddleOCR docs** — best multi-language OCR
- **Segment Anything (SAM)** — Meta research

## 🏋️ Mashqlar

### 🟢 Easy
1. YOLOv8n pretrained bilan rasm va video'da inference.
2. Confidence threshold'ni o'zgartirib (`0.1`, `0.3`, `0.7`) natijalarni ko'ring.
3. Tesseract bilan oddiy matnli rasmni o'qing.

### 🟡 Medium
1. **Custom YOLO**: Roboflow yoki Label Studio bilan 100 ta rasmni label qiling (1-2 class), YOLO fine-tune (Colab GPU bilan).
2. **OCR comparison**: bir xil rasmda Tesseract, EasyOCR, PaddleOCR natijalarini solishtiring.
3. **People counter**: video'da odamlar sonini real-time hisoblang.

### 🔴 Hard
1. **Production CV pipeline**: FastAPI + YOLO + Celery + Redis + Docker. WebSocket bilan real-time video stream processing.
2. **Custom OCR pipeline**: hujjat sahifasi → text region detection (YOLO) → OCR (PaddleOCR) → JSON structured output.
3. **SAM + YOLO combo**: YOLO bounding box → SAM bilan segmentation mask → object-by-object analysis.

## Capstone

`notebooks/month-04/03_yolo_detection.ipynb`:
- **Loyiha:**O'z dataset (telefondan 50-100 rasm) — masalan, mahalliy belgilar (yo'l belgilar, do'kon vivesakalari, mevalar)
- Roboflow'da annotation
- YOLOv8 fine-tune (Colab GPU)
- mAP 80%+
- FastAPI servisni Docker'da deploy

## ✅ Tekshirish ro'yxati

- [ ] Detection va Classification farqini bilaman
- [ ] IoU va mAP metric'larini tushunaman
- [ ] YOLO inference qila olaman (image, video, webcam)
- [ ] Custom dataset uchun YOLO fine-tune qilishni bilaman
- [ ] Segmentation (YOLO-seg, SAM) bilan tanishman
- [ ] OCR (3 ta kutubxonadan birortasi)
- [ ] FastAPI'da detection servis yaratishni bilaman
- [ ] Async video processing (Celery)

[NLP asoslari](./04-nlp-basics.md) ga o'tamiz.
