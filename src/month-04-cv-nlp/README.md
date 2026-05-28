# Oy 4 — Computer Vision + NLP

## 🎯 Bu oydagi maqsad

Oy oxirida siz quyidagilarni qila olasiz:
- OpenCV bilan klassik image processing
- YOLO va boshqa pretrained model'lar bilan object detection
- OCR (Tesseract, EasyOCR, PaddleOCR) bilan matn ajratish
- spaCy va NLTK bilan text preprocessing
- HuggingFace Transformers bilan BERT-style modellarni qo'llash

## 📅 Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | OpenCV + Image Processing | 10-12 soat |
| **Hafta 2** | YOLO, Detection, Segmentation, OCR | 10-12 soat |
| **Hafta 3** | NLP asoslari + Text Preprocessing | 10-12 soat |
| **Hafta 4** | Transformers + HuggingFace | 10-12 soat |

## 📖 Boblar tartibi

1. [Computer Vision ga kirish](./01-computer-vision.md)
2. [OpenCV bilan ishlash](./02-opencv.md)
3. [YOLO va Object Detection](./03-yolo-detection.md)
4. [NLP asoslari](./04-nlp-basics.md)
5. [Text Preprocessing](./05-text-preprocessing.md)
6. [Transformers ga kirish](./06-transformers-intro.md)
7. [Mashqlar](./exercises.md)

## 🎓 Oy oxirida nima qila olasiz?

- Rasm/video upload'ni qabul qilib YOLO bilan object detection qaytaradigan FastAPI servis
- OCR servisi — passport, ID kartlardan ma'lumot ajratish
- HuggingFace pretrained model bilan sentiment analyzer va NER
- Oy 5 (LLM/RAG) ga to'liq tayyor bo'lish

## 💡 Backend Dev uchun maslahat

Bu oyda asosan **pretrained model'lar**dan foydalanish:
- ResNet/EfficientNet (Oy 3) — image classification uchun
- YOLO — object detection
- Segment Anything (SAM) — segmentation
- BERT/RoBERTa — text understanding
- Whisper — speech-to-text
- Stable Diffusion — image generation

Sizning vazifangiz — bu modellarni **production'ga olib chiqish**, mahalliy tilingiz (o'zbek) uchun fine-tune qilish, FastAPI/Django ekosistemasi bilan birlashtirish.

## 🚀 Boshlash

[Computer Vision ga kirish](./01-computer-vision.md) bilan boshlang.
