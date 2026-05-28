# Oy 4 — Mashqlar to'plami

## 🟢 Easy

### Computer Vision
1. OpenCV bilan rasm yuklang, RGB/HSV/Grayscale ga aylantiring.
2. Canny edge detection + contour topish.
3. YOLOv8n pretrained model bilan rasm uchun inference.
4. Pretrained EfficientNet bilan rasm uchun top-5 classification.
5. Tesseract bilan oddiy matnli rasm uchun OCR.

### NLP
1. NLTK bilan tokenization, stop words olib tashlash, lemmatization.
2. spaCy bilan NER va POS tagging.
3. TF-IDF + Logistic Regression baseline (Spam SMS dataset).
4. HuggingFace `pipeline("sentiment-analysis")` 10 ta gap uchun.
5. Sentence Transformers bilan 5 ta gap orasidagi cosine similarity matrix.

## 🟡 Medium

### CV — Real loyihalar
1. **Document Scanner**: telefon rasmidan hujjatni "tekislash" (contour + perspective).
2. **Custom YOLO training**: 100-200 ta rasmni Roboflow'da label qiling, YOLOv8 fine-tune (Colab GPU).
3. **OCR pipeline**: pasport rasmidan ism, familiya, raqamlarni ajratib olish.
4. **Image similarity search**: 1000 ta rasmni pretrained CNN bilan embed qiling, query rasmga eng yaqin 10 tasini toping.
5. **Real-time webcam YOLO**: webcam → bounding box + label.

### NLP — Real loyihalar
1. **News classifier**: BBC News dataset (5 kategoriya), TF-IDF + LR vs BERT solishtirish.
2. **O'zbek matn dataset**: Telegram'dan 5000+ post yig'ing, classifier yarating.
3. **Multilingual sentiment**: 3 til (en/ru/uz) uchun bitta model.
4. **Custom BPE tokenizer**: o'zbek korpus uchun BPE o'rgating.
5. **Zero-shot classifier**: 10 ta yangiliklarni "labels" bermay 5 ta kategoriyaga ajrating.

## 🔴 Hard (Production)

### 1. CV — Object Counter Service

**Talab:**
- FastAPI + YOLOv8 custom trained model
- Endpoint: rasm/video upload → count by class
- Celery + Redis (async processing)
- WebSocket real-time updates
- Docker + docker-compose
- Streamlit yoki React frontend

**Misol use case:**parking lotda mashinalar soni, do'konda odamlar oqimi

### 2. OCR — ID Card Reader

**Talab:**
- ID kart turini detect qilish (YOLO)
- Perspective correction (OpenCV)
- Field-by-field OCR (PaddleOCR)
- Validation + parsing (regex)
- PostgreSQL'da saqlash
- REST API + admin panel

### 3. NLP — Multilingual Customer Support Classifier

**Talab:**
- 3 tilda (en/ru/uz) keladigan support ticket'larni 10 kategoriyaga ajratish
- mBERT yoki XLM-R fine-tune
- FastAPI + caching
- Prediction monitoring (concept drift detection)
- Telegram bot integration

### 4. CV+NLP — Visual Question Answering

**Talab:**
- BLIP yoki similar VLM (Vision-Language Model)
- Rasm + savol → javob
- Streamlit demo
- Mobile app integration

## Mini-loyihalar

### Mini-loyiha 1: O'zbek Plate Number Recognition
- O'zbek raqam belgilari datasetini yig'ish (telefondan 100+ rasm)
- YOLO bilan plate detection
- OCR bilan raqamni o'qish
- FastAPI servisi

### Mini-loyiha 2: Receipt Scanner
- Magazin chekining rasmini OCR
- Mahsulotlar va narxlarni ajratish
- Total summa va kategoriya bo'yicha guruhlash
- Telegram bot

### Mini-loyiha 3: Sport Highlights Generator
- Futbol o'yini video
- Object detection (player, ball)
- Event detection (goal, foul)
- Avtomatik highlights montage (FFmpeg)

### Mini-loyiha 4: Smart Document Search
- 100+ PDF hujjatni indexlash
- Sentence embeddings + FAISS
- Natural language search
- Streamlit UI

## Quiz

### CV
1. Object detection va classification farqi?
2. IoU va mAP nima?
3. YOLO va Faster R-CNN tezligi va aniqligi farqi?
4. Anchor box nima va anchor-free detector qanday ishlaydi?
5. NMS (Non-Maximum Suppression) qachon ishlatiladi?
6. Tesseract va modern OCR (EasyOCR/PaddleOCR) farqi?
7. SAM (Segment Anything) ning special tomoni?

### NLP
1. Stemming va Lemmatization farqi?
2. TF-IDF formulasi va intuitsiyasi?
3. Word2Vec'ning Skip-gram va CBOW farqi?
4. BPE va WordPiece tokenization farqi?
5. BERT, GPT, T5 farqi (arxitektura)?
6. Attention mechanism Q, K, V nima?
7. Zero-shot classification qanday ishlaydi?

### Production
1. Pretrained model'ni qanday qilib production'ga olib chiqasiz?
2. GPU inference uchun batching nima uchun foydali?
3. Model versioning strategiyalari?
4. CV servis uchun Docker image hajmini qanday kamaytirasiz?
5. NLP servis uchun caching strategiyalari?

## ✅ Oy 4 oxiri checklist

- [ ] OpenCV bilan klassik image processing
- [ ] YOLOv8 inference va fine-tuning (Colab/Kaggle)
- [ ] OCR (kamida bitta kutubxona: Tesseract/EasyOCR/PaddleOCR)
- [ ] NLP klassik: TF-IDF + LR baseline
- [ ] spaCy bilan NER, POS
- [ ] HuggingFace Transformers (pipeline + Auto*)
- [ ] Sentence embeddings (RAG'ga tayyor)
- [ ] FastAPI'da CV yoki NLP servis
- [ ] Capstone loyiha GitHub'da
- [ ] LinkedIn'ga post

Tabriklayman! [Oy 5 — LLM, RAG va AI Agentlar](../month-05-llm-rag/README.md) ga tayyormiz — endi siz LLM era'ga kirasiz!
