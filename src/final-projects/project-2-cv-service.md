# Loyiha 2: Computer Vision Service

## 🎯 Maqsad

YOLO yoki shunga o'xshash CV model'ni production'da serve qiluvchi to'liq backend servis. Async processing, S3 storage, Docker GPU support — modern CV stack.

## Tavsiya etilgan use case'lar

| Use case | Dataset / API | Difficulty |
|----------|---------------|------------|
| **License Plate Recognition** | O'zbek raqamlar (telefondan to'plang) | ⭐⭐⭐⭐ |
| **Food Detection** | UECFoodPix yoki Open Images | ⭐⭐⭐ |
| **Product Catalog (E-commerce)** | Mahsulot rasmlari | ⭐⭐⭐ |
| **Document Scanner + OCR** | Hujjat rasmlar | ⭐⭐⭐⭐ |
| **Crop Disease Detection** | PlantVillage dataset | ⭐⭐⭐ |
| **Sport Highlights** | Futbol/basketball video | ⭐⭐⭐⭐⭐ |
| **Construction Safety** | Worker safety datasets | ⭐⭐⭐⭐ |

**Tavsiya:****License Plate Recognition**(o'zbek kontekst — original loyiha) yoki **Crop Disease Detection**(PlantVillage tayyor dataset).

## Architecture

```
┌─────────────┐
│  Client     │
│  (Web/App)  │
└──────┬──────┘
       │ Upload image/video
       ▼
┌──────────────────────┐
│   FastAPI Backend    │
│  - Auth              │
│  - Validation        │
│  - Routing           │
└────┬───────────┬─────┘
     │           │
     ▼           ▼
┌─────────┐  ┌──────────────┐
│  S3 /   │  │  Celery      │
│  MinIO  │  │  Workers     │
│ (files) │  │              │
└─────────┘  └──────┬───────┘
                    │
                    ▼
            ┌──────────────┐
            │  YOLO Model  │
            │  (GPU/CPU)   │
            └──────┬───────┘
                   │
                   ▼
            ┌──────────────┐
            │  Postgres    │
            │  Results     │
            └──────────────┘
```

## Tech Stack

### Required
- **Backend:**FastAPI
- **ML:**YOLOv8 / YOLOv11 (Ultralytics) yoki HuggingFace
- **Async:**Celery + Redis
- **Storage:**S3 yoki MinIO
- **Database:**PostgreSQL
- **Container:**Docker (GPU support)

### Nice to have
- **Frontend:**Streamlit yoki React
- **Real-time:**WebSocket
- **OCR:**PaddleOCR
- **Tracking:**Custom (Lightweight DeepSORT)
- **Monitoring:**Prometheus

## Features

### MVP (1-hafta)
- [ ] FastAPI image upload endpoint
- [ ] YOLO pretrained inference
- [ ] Bounding box JSON response
- [ ] Annotated image qaytarish
- [ ] Docker (CPU)
- [ ] Basic README

### V2 (2-hafta)
- [ ] Custom YOLO training (Roboflow yoki Label Studio)
- [ ] S3/MinIO storage (uploaded images, results)
- [ ] Celery async processing
- [ ] Video upload + frame-by-frame
- [ ] Result history (Postgres)
- [ ] Tests
- [ ] CI/CD

### V3 (3-hafta)
- [ ] OCR integration (license plate raqamlarini o'qish)
- [ ] WebSocket real-time webcam
- [ ] GPU Docker image
- [ ] Streamlit demo
- [ ] Cloud deployment (RunPod / GPU)
- [ ] Blog post

## API spec

### `POST /detect/image`
```bash
curl -X POST -F "file=@photo.jpg" http://api/detect/image
```
```json
{
    "detection_id": "uuid",
    "detections": [
        {
            "class": "car",
            "confidence": 0.94,
            "bbox": [120, 200, 450, 380],
            "license_plate": "01A123BC"  // OCR result
        }
    ],
    "image_url": "https://s3.../annotated_uuid.jpg",
    "processing_time_ms": 245
}
```

### `POST /detect/video` (async)
```json
{
    "task_id": "celery_task_uuid",
    "status": "queued",
    "estimated_time_seconds": 120
}
```

### `GET /detect/video/{task_id}`
```json
{
    "task_id": "uuid",
    "status": "processing",  // queued | processing | completed | failed
    "progress_percent": 45,
    "result_url": null  // completed bo'lganda
}
```

### `WebSocket /detect/stream`
- Browser webcam frame → server
- Server YOLO inference
- Bounding boxes JSON qaytaradi (real-time)

### `POST /annotations` (custom training uchun)
```json
{
    "image_id": "uuid",
    "annotations": [
        {"class": "license_plate", "bbox": [...]},
    ]
}
```

## Project structure

```
cv-service/
├── README.md
├── docker-compose.yml
├── Dockerfile.cpu
├── Dockerfile.gpu
├── .github/workflows/
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── detect.py
│   │   │   ├── annotations.py
│   │   │   └── ws.py
│   │   └── schemas.py
│   ├── core/
│   │   └── config.py
│   ├── storage/
│   │   └── s3.py                   # MinIO/S3 client
│   ├── ml/
│   │   ├── yolo.py                 # Model wrapper
│   │   ├── ocr.py
│   │   └── tracking.py             # DeepSORT
│   ├── tasks/                      # Celery
│   │   ├── celery_app.py
│   │   └── video_processing.py
│   └── data/
│       └── models.py               # Postgres ORM
├── tests/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_yolo_training.ipynb     # Roboflow/Colab
│   └── 03_model_evaluation.ipynb
├── data/
│   └── raw/                        # Custom dataset
├── models/
│   └── yolov8_custom.pt
├── frontend/
│   └── streamlit_app.py
└── pyproject.toml
```

## Implementatsiya plani (3 hafta)

### Hafta 1 — MVP
- Day 1-2: Dataset collection (telefondan rasm yoki Kaggle)
- Day 3: Roboflow'da annotation (50-200 rasm)
- Day 4: YOLOv8 training (Colab GPU)
- Day 5: FastAPI endpoint + inference
- Day 6: Docker (CPU image)
- Day 7: GitHub + README

### Hafta 2 — Async processing
- Day 8: MinIO local setup (Docker)
- Day 9-10: Celery + Redis
- Day 11: Video processing pipeline
- Day 12: Postgres history
- Day 13: Tests
- Day 14: CI/CD

### Hafta 3 — Production + Demo
- Day 15: OCR integration (PaddleOCR)
- Day 16: WebSocket real-time
- Day 17: GPU Dockerfile
- Day 18: Streamlit demo
- Day 19: Cloud deployment
- Day 20: Demo video
- Day 21: Blog post

## Success metrics

- **Detection accuracy (mAP):**> 0.85 on custom dataset
- **Latency (single image):**< 200ms (CPU), < 50ms (GPU)
- **Video processing:**30 fps (CPU), 100+ fps (GPU)
- **Concurrent users:**> 100 (via Celery)
- **OCR accuracy:**> 90% on plates

## Resurslar

- **Ultralytics YOLO docs** — [docs.ultralytics.com](https://docs.ultralytics.com/)
- **Roboflow Universe** — datasets va training
- **PaddleOCR docs** — multi-language OCR
- **MinIO docs** — S3-compatible local
- **FastAPI WebSocket tutorial**

## Bonus features

- **Multi-model serving** — YOLO + OCR + Tracking pipeline
- **Custom training UI** — upload images → annotate → train (no-code)
- **Edge deployment** — TensorRT yoki ONNX runtime
- **Mobile app** — React Native + image upload
- **Real-time tracking** — multi-object tracking
- **Cost optimization** — GPU spot instances

## ✅ Submission checklist

- [ ] GitHub repo
- [ ] Custom dataset (100+ images, annotated)
- [ ] YOLO custom model fine-tuned
- [ ] FastAPI API working
- [ ] Async video processing
- [ ] OCR integration (agar applicable)
- [ ] Streamlit demo
- [ ] Demo video (web + CLI)
- [ ] Blog post
- [ ] LinkedIn post

Tugatdingiz? [Loyiha 3: RAG Chatbot](./project-3-rag-chatbot.md) ga o'ting.
