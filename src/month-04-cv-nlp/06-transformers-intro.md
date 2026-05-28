# Transformers ga kirish

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Transformer arxitekturasini va attention mechanism'ini tushunasiz
- HuggingFace Transformers ekosistemasini bilasiz
- Pretrained model'larni (BERT, RoBERTa, T5) qo'llay olasiz
- Sentiment, NER, Summarization, QA pipeline'larini ishga tushira olasiz
- Oy 5 (LLM/RAG) ga to'liq tayyor bo'lasiz

## 📖 Nimani o'rganish kerak

- **Attention mechanism** — Q, K, V
- **Self-attention** va **Multi-head attention**
- **Transformer arxitekturasi** — Encoder, Decoder
- **BERT** — Encoder-only (NLU)
- **GPT** — Decoder-only (Generation)
- **T5, BART** — Encoder-Decoder (Seq2Seq)
- **HuggingFace Hub** — pretrained models
- **HuggingFace `pipeline` API**
- **`AutoModel`, `AutoTokenizer`**
- **Sentence Transformers** — embeddings

## 📦 Kutubxonalar

```bash
pip install transformers torch sentence-transformers datasets
pip install accelerate                       # Multi-GPU, mixed precision
```

## 🧠 Muhim mavzular

### Attention mechanism — intuition

```
Query (Q): "Nima qidiryapman?"
Key (K):   "Bu yerda nima bor?"
Value (V): "Mana bu"

attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) · V
```

Sodda analogiya: **Google qidiruv**
- Q = sizning so'rovingiz
- K = web sahifalardagi mavzular
- V = sahifalarning haqiqiy mazmuni
- Attention score = sahifaning sizning so'rovingiz bilan mosligi

### Self-attention

Bitta sequence ichida har bir token qolganlar bilan munosabati hisoblanadi:

```
Sentence: "The cat sat on the mat"
                ↑
        "cat" tokeni uchun:
        - "The" bilan attention = 0.1
        - "sat" bilan attention = 0.3 (verb!)
        - "mat" bilan attention = 0.4 (object!)
        - va h.k.
```

### Transformer arxitekturasi

```
Encoder (BERT, T5 encoder):
  Input → Embedding → [Multi-Head Self-Attention + FFN] x N → Output

Decoder (GPT, T5 decoder):
  Input → Embedding → [Masked Self-Attention + Cross-Attention + FFN] x N → Output

Encoder-Decoder (T5, BART):
  Source → Encoder → Decoder (uses encoder output) → Target
```

### Model turlari va vazifalari

| Model turi | Misol | Vazifa |
|-----------|-------|--------|
| **Encoder-only** | BERT, RoBERTa, XLM-R | NLU: classification, NER, QA |
| **Decoder-only** | GPT, Llama, Claude | Generation, chat |
| **Encoder-Decoder** | T5, BART, mT5 | Translation, summarization |

## 💻 Kod misollari

### HuggingFace `pipeline` — eng oson yo'l

```python
from transformers import pipeline

# 1. Sentiment analysis
sentiment = pipeline("sentiment-analysis")
result = sentiment("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.999}]

# Multilingual
sentiment_multi = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
)
result = sentiment_multi("Bu mahsulot juda yaxshi!")
# 5 stars rating

# 2. NER
ner = pipeline("ner", grouped_entities=True)
result = ner("Apple is looking at buying U.K. startup for $1 billion")
# [{'entity_group': 'ORG', 'word': 'Apple', ...},
#  {'entity_group': 'LOC', 'word': 'U.K.', ...},
#  {'entity_group': 'MONEY', 'word': '$1 billion', ...}]

# 3. Question Answering
qa = pipeline("question-answering")
context = "Hugging Face is a company based in New York and Paris."
result = qa(question="Where is Hugging Face based?", context=context)
# {'answer': 'New York and Paris', 'score': 0.95, ...}

# 4. Summarization
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
result = summarizer(long_text, max_length=100, min_length=30)

# 5. Translation
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
result = translator("Hello, how are you?")
# [{'translation_text': 'Привет, как дела?'}]

# 6. Text generation
generator = pipeline("text-generation", model="gpt2")
result = generator("In a galaxy far far away,", max_length=50, num_return_sequences=2)

# 7. Zero-shot classification (juda kuchli!)
zsc = pipeline("zero-shot-classification")
result = zsc(
    "I have a problem with my iPhone screen",
    candidate_labels=["technology", "sports", "politics", "weather"],
)
# scores: technology=0.95, ...
```

### AutoModel + AutoTokenizer — pastroq darajada

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

texts = ["I love this!", "This is terrible.", "Average product."]

inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)

labels = ["NEGATIVE", "POSITIVE"]
for text, prob in zip(texts, probs):
    pred = labels[prob.argmax().item()]
    score = prob.max().item()
    print(f"{text} → {pred} ({score:.3f})")
```

### Sentence Embeddings (RAG uchun muhim!)

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Pretrained sentence encoder
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, tez
# yoki: "all-mpnet-base-v2" — 768-dim, aniqroq
# Multilingual: "paraphrase-multilingual-MiniLM-L12-v2"

sentences = [
    "Mashina o'rganish juda qiziq",
    "Machine learning is very interesting",
    "Men futbolni yaxshi ko'raman",
    "I love football",
]

embeddings = model.encode(sentences)  # shape (4, 384)

# Cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(embeddings)
# sim[0][1] high — har ikkalasi "ML" haqida
# sim[2][3] high — har ikkalasi "futbol" haqida
```

### Fine-tuning BERT classifier (text classification)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# 1. Data
df = pd.read_csv("reviews.csv")  # text, label
dataset = Dataset.from_pandas(df).train_test_split(test_size=0.2)

# 2. Tokenize
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized = dataset.map(tokenize, batched=True)

# 3. Model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=df["label"].nunique(),
)

# 4. Training
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    load_best_model_at_end=True,
    fp16=True,  # mixed precision
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    tokenizer=tokenizer,
)

trainer.train()

# 5. Save
trainer.save_model("./final_model")
```

### Multilingual model (o'zbek uchun)

```python
from transformers import pipeline

# XLM-R — 100+ tillarni qo'llab-quvvatlaydi
ner_multi = pipeline(
    "ner",
    model="xlm-roberta-large-finetuned-conll03-english",
    aggregation_strategy="simple",
)

# O'zbek matnda ham qisman ishlaydi
text = "Toshkent shahri Markaziy Osiyodagi eng katta shahar"
result = ner_multi(text)
```

## 🔌 Backend integratsiyasi

### BERT sentiment API

```python
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.sentiment = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=0 if torch.cuda.is_available() else -1,
    )
    yield

app = FastAPI(lifespan=lifespan)

class TextInput(BaseModel):
    text: str

@app.post("/sentiment")
def analyze(data: TextInput):
    result = app.state.sentiment(data.text)[0]
    return {"label": result["label"], "score": result["score"]}
```

### Embedding service (RAG uchun asos)

```python
from sentence_transformers import SentenceTransformer

@asynccontextmanager
async def lifespan(app):
    app.state.encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    yield

app = FastAPI(lifespan=lifespan)

class TextsInput(BaseModel):
    texts: list[str]

@app.post("/embeddings")
def get_embeddings(data: TextsInput):
    embeddings = app.state.encoder.encode(data.texts).tolist()
    return {"embeddings": embeddings, "dim": len(embeddings[0])}
```

### Batching va caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=10000)
def cached_embedding(text: str) -> tuple:
    return tuple(encoder.encode(text).tolist())

@app.post("/embed-batch")
async def embed_batch(texts: list[str]):
    # Cache check
    embeddings = []
    uncached = []
    uncached_indices = []
    
    for i, text in enumerate(texts):
        h = hashlib.md5(text.encode()).hexdigest()
        cached = await redis.get(f"emb:{h}")
        if cached:
            embeddings.append(json.loads(cached))
        else:
            embeddings.append(None)
            uncached.append(text)
            uncached_indices.append(i)
    
    # Batch encode uncached
    if uncached:
        new_embeddings = encoder.encode(uncached, batch_size=32).tolist()
        for idx, emb, text in zip(uncached_indices, new_embeddings, uncached):
            embeddings[idx] = emb
            h = hashlib.md5(text.encode()).hexdigest()
            await redis.setex(f"emb:{h}", 86400, json.dumps(emb))
    
    return {"embeddings": embeddings}
```

## 📚 Resurslar

- **HuggingFace Course** — [huggingface.co/learn](https://huggingface.co/learn) — **MUST**
- **"Natural Language Processing with Transformers"** — Lewis Tunstall (O'Reilly)
- **"The Illustrated Transformer"** — Jay Alammar ([blog](http://jalammar.github.io/illustrated-transformer/))
- **Andrej Karpathy — "Let's build GPT"** (YouTube) — transformer'ni noldan
- **"Attention is All You Need"** — original paper (2017)
- **Sentence Transformers docs** — [sbert.net](https://www.sbert.net/)

## 🏋️ Mashqlar

### 🟢 Easy
1. `pipeline("sentiment-analysis")` bilan 10 ta gap classify qiling.
2. NER bilan matndan barcha nomlangan obyektlarni ajrating.
3. Sentence Transformers bilan 2 gap orasidagi similarity.

### 🟡 Medium
1. **Zero-shot classification**: o'zbek matnlarni 5 ta kategoriyaga ajrating.
2. **Fine-tune DistilBERT**: o'zingiz dataset (sentiment, topic) bilan.
3. **Multilingual embeddings**: o'zbek va inglizcha matnlar orasida cross-lingual similarity.

### 🔴 Hard
1. **Production NLP service**: HuggingFace model + FastAPI + Redis cache + Docker. Batch endpoint, healthcheck, Prometheus metrics.
2. **Embeddings index**: 10,000 ta hujjat embeddings'ini saqlab, semantic search API yaratish (Oy 5 RAG uchun asos).
3. **Custom NER**: o'zbek manzillar uchun NER (Toshkent, Yunusobod tumani, va h.k.) fine-tuning.

## 🚀 Capstone

`notebooks/month-04/06_transformers.ipynb`:
- **Loyiha:** O'zbek Telegram kanal post'lari uchun multilingual sentiment classifier
- Yo'l: `pipeline` → fine-tune mBERT → evaluation → FastAPI deployment
- Hospital appointment booking — natural language input → structured fields (NER + parsing)

## ✅ Tekshirish ro'yxati

- [ ] Attention mechanism intuition
- [ ] Encoder-only, Decoder-only, Encoder-Decoder farqi
- [ ] BERT va GPT farqini bilaman
- [ ] HuggingFace `pipeline` API bilan ishlay olaman
- [ ] `AutoModel` va `AutoTokenizer` bilan ham
- [ ] Sentence embeddings va RAG'ning asoslari
- [ ] Fine-tuning Trainer API
- [ ] Production'da Transformer model serving

🎉 **Oy 4 tugadi!** [Mashqlar](./exercises.md) ni ko'rib chiqing va [Oy 5 — LLM, RAG va AI Agentlar](../month-05-llm-rag/README.md) ga o'ting — endi haqiqiy AI mahsulotlar yaratasiz.
