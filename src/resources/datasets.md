# Datasets

## 🌍 Asosiy manbalar

### Kaggle
- **kaggle.com/datasets** — minglab dataset
- **kaggle.com/competitions** — competitions (real problems)
- Klassik ML uchun #1 manba
- Notebook'lar bilan birga

### Hugging Face Datasets
- **huggingface.co/datasets** — NLP/CV/Audio
- 100,000+ dataset
- Python API bilan oson yuklash

### UCI ML Repository
- **archive.ics.uci.edu/ml** — klassik datasets
- Akademik standart

### Google Dataset Search
- **datasetsearch.research.google.com**
- Universal search engine

### Papers With Code
- **paperswithcode.com/datasets** — paper'larda ishlatilgan

### data.gov / data.gov.uz
- **data.gov.uz** — O'zbekiston open data
- Lokal kontekst uchun

## 📊 Klassik ML / Tabular

### Boshlovchilar uchun
- **Iris** — 3 class classification (150 sample)
- **Titanic** — binary classification
- **California Housing** — regression
- **MNIST** — image classification (handwritten digits)
- **Wine Quality** — regression/classification
- **Adult Income** — classification

### Real-world tabular
- **Telco Customer Churn** (Kaggle) — churn prediction
- **House Prices** (Kaggle Ames Housing) — regression
- **Credit Card Fraud Detection** — imbalanced classification
- **NYC Taxi Trips** — time series + geo
- **Olist E-commerce** (Kaggle) — multi-table
- **LendingClub Loans** — credit risk
- **Movie Lens** — recommendations

## 🖼 Computer Vision

### Image classification
- **CIFAR-10, CIFAR-100** — 32x32 color images
- **ImageNet** — 1000 classes (akademik)
- **Fashion-MNIST** — kiyim turlari
- **Tiny ImageNet** — kichikroq versiya
- **Caltech 101/256** — har xil obyektlar
- **Stanford Cars** — avtomobillar
- **Oxford Flowers** — 102 gul turi
- **Food-101** — ovqat rasmlari

### Object detection
- **COCO** — eng katta detection dataset
- **Pascal VOC** — klassik
- **Open Images** (Google) — 9M images
- **KITTI** — autonomous driving
- **WIDER FACE** — face detection
- **LVIS** — long-tail detection

### Segmentation
- **Cityscapes** — urban scene
- **ADE20K** — scene parsing
- **PASCAL VOC Segmentation**
- **Mapillary Vistas** — street view

### Medical imaging
- **MURA** — bone X-rays
- **CheXpert** — chest X-rays
- **ISIC** — skin lesions
- **Kaggle Medical Image Datasets**

### Specialized
- **PlantVillage** — plant diseases
- **DeepFashion** — fashion images
- **CelebA** — face attributes
- **LFW** — face recognition

## 📝 NLP

### Text classification
- **IMDB Reviews** — sentiment
- **Yelp Reviews** — sentiment
- **AG News** — topic classification
- **SST-2** — sentiment
- **20 Newsgroups** — topic

### NER
- **CoNLL-2003** — English NER
- **OntoNotes 5.0** — multi-genre

### Question Answering
- **SQuAD 2.0** — extractive QA
- **Natural Questions** — Google
- **TriviaQA**

### Translation
- **WMT** — annual translation
- **OPUS** — parallel corpora

### Summarization
- **CNN/Daily Mail** — news summarization
- **XSum** — extreme summarization
- **Reddit TIFU** — informal

### Multi-task / Modern
- **GLUE / SuperGLUE** — NLU benchmark
- **MMLU** — knowledge benchmark
- **HellaSwag** — common sense

### Multilingual
- **OSCAR** — multilingual web
- **mC4** — Common Crawl
- **CC-100** — 100+ tillar
- **FLORES** — translation benchmark

## 🇺🇿 O'zbek tilidagi datasetlar

### Resmiy
- **data.gov.uz** — open data
- **stat.uz** — statistika
- **lex.uz** — qonun hujjatlari

### Web scraping mumkin
- **uz.wikipedia.org** — Wikipedia dump
- **daryo.uz, kun.uz, gazeta.uz** — yangiliklar (legal/personal use)
- **Telegram channellar** — public channels (with respect)

### HuggingFace
- HuggingFace'da `language:uz` qidiring
- **OSCAR-uz** — uzbek web corpus
- **mC4-uz** — Common Crawl

### Audio (speech)
- **Common Voice — Uzbek** — Mozilla project
- **Voxlingua107** — language identification

## 🎵 Audio / Speech

### Speech recognition
- **LibriSpeech** — English audiobooks
- **Common Voice** (Mozilla) — multilingual
- **VoxPopuli** — European Parliament
- **TED-LIUM** — TED talks

### Music
- **GTZAN** — genre classification
- **FMA (Free Music Archive)**
- **MagnaTagATune** — auto-tagging

### Environmental
- **UrbanSound8K** — city sounds
- **ESC-50** — environmental sounds

## 📹 Video

- **Kinetics-400/700** — action recognition
- **UCF101** — action recognition
- **YouTube-8M** — large scale
- **Something-Something** — temporal reasoning

## 💻 Time Series

### Finance
- **Yahoo Finance** (yfinance library) — stocks
- **Quandl** — financial data
- **Kaggle Stock Market**

### Healthcare
- **MIT-BIH** — ECG signals
- **MIMIC** — clinical (access kerak)

### IoT / Sensors
- **UCI HAR** — human activity
- **WESAD** — stress detection

### Weather / Environment
- **NOAA** — climate
- **NASA Earth Data**

## 🌐 Multimodal

- **MS COCO Captions** — image + text
- **Flickr30k** — image + text
- **Visual Question Answering (VQA)**
- **AudioSet** — video + audio
- **HowTo100M** — instruction videos

## 🤖 LLM / RAG

### Documentation
- **Wikipedia dump** — keng knowledge base
- **arxiv** — research papers
- **GitHub repos** — code docs
- **StackExchange dumps** — Q&A

### Conversation
- **Anthropic HH-RLHF** — preferences
- **ShareGPT** — real ChatGPT logs
- **OpenAssistant** — public conversations

### Instruction
- **Alpaca** — Stanford (52K)
- **Dolly** — Databricks (15K)
- **Tulu** — AllenAI

## 🎯 Qaysi dataset qachon?

### Yangi mavzuni o'rganishda
- **Boshlovchi:** Iris, Titanic, MNIST
- **Klassik ML:** Telco Churn, House Prices
- **DL boshlash:** CIFAR-10, IMDB
- **CV:** Pretrained datasets + custom

### Portfolio loyiha uchun
- **Original** — o'zingiz to'plang (telefon, web scraping)
- **Real-world** — Kaggle competitions
- **Lokal** — O'zbekiston open data

### Production simulation
- **Streaming** — Kafka simulated data
- **Live** — public APIs (Twitter, Reddit)
- **Synthetic** — `make_classification`, faker library

## 🛠 Tools

### Dataset library'lar
```python
# scikit-learn datasets
from sklearn.datasets import load_iris, fetch_california_housing

# HuggingFace datasets
from datasets import load_dataset
ds = load_dataset("squad")

# torchvision
from torchvision import datasets
mnist = datasets.MNIST(root="./", train=True, download=True)

# Kaggle API
!pip install kaggle
!kaggle competitions download -c titanic
```

### Annotation tools
- **Label Studio** — open source
- **CVAT** — CV annotation
- **Roboflow** — CV + datasets management
- **Prodigy** — NLP annotation
- **Doccano** — text annotation (open source)

## ⚖️ Legal va ethik

### Tekshirib qo'ying
- **License** — MIT, Apache, CC-BY, CC-BY-SA, va h.k.
- **Commercial use** — bepulmi yoki yo'qmi
- **Attribution** — manbani ko'rsatish kerakmi
- **PII** — shaxsiy ma'lumotlar bormi

### Best practices
- **Bias check** — dataset balanced/representative emi?
- **Privacy** — anonimization
- **Documentation** — datasheet, model card
- **Consent** — yig'ilgan ma'lumotlar uchun

[Cheatsheets](./cheatsheets.md) ga o'tish.
