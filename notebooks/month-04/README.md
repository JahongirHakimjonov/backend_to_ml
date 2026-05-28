# Month 04 — CV + NLP Notebooks

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `01_cv_intro.ipynb` | CV overview | [CV intro](../../src/month-04-cv-nlp/01-computer-vision.md) |
| `02_opencv_pipeline.ipynb` | OpenCV | [OpenCV](../../src/month-04-cv-nlp/02-opencv.md) |
| `03_yolo_detection.ipynb` | YOLO custom | [YOLO](../../src/month-04-cv-nlp/03-yolo-detection.md) |
| `04_nlp_basics.ipynb` | NLP fundamentals | [NLP basics](../../src/month-04-cv-nlp/04-nlp-basics.md) |
| `05_text_preprocessing.ipynb` | Text cleaning | [Text Preprocessing](../../src/month-04-cv-nlp/05-text-preprocessing.md) |
| `06_transformers.ipynb` | HuggingFace | [Transformers](../../src/month-04-cv-nlp/06-transformers-intro.md) |

## 🛠 Dependencies

```bash
# uv bilan
uv sync --group month-04

# spaCy modellari (sync'dan keyin)
uv run python -m spacy download en_core_web_sm
uv run python -m spacy download xx_ent_wiki_sm

uv run jupyter lab
```

Tarkibida (CV + NLP): opencv, pillow, timm, ultralytics, supervision, mediapipe, easyocr, paddleocr, nltk, spacy, transformers, sentence-transformers va h.k.

## 📚 Datasets

- **CV:** COCO sample, custom (telefon rasmlar), Roboflow Universe
- **NLP:** IMDB, AG News, custom (Telegram channels)

[Asosiy bob](../../src/month-04-cv-nlp/README.md).
