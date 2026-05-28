# NLP asoslari

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- NLP (Natural Language Processing) ning asosiy masala turlarini bilasiz
- spaCy va NLTK bilan klassik NLP pipeline qura olasiz
- TF-IDF, Word2Vec, GloVe vektor representation'larini bilasiz
- HuggingFace (Oy 5'da chuqurroq) ekosistemasiga tayyor bo'lasiz

## Nimani o'rganish kerak

- **NLP masala turlari** — classification, NER, POS, parsing, generation, translation
- **Tokenization** — word, subword (BPE, WordPiece, SentencePiece), char-level
- **Stemming va Lemmatization**
- **Stop words**
- **Bag of Words (BoW)**va **TF-IDF**
- **n-grams**
- **Word embeddings** — Word2Vec, GloVe, FastText
- **POS tagging, dependency parsing**
- **Named Entity Recognition (NER)**
- **Language detection**
- **O'zbek tili uchun NLP**

## Kutubxonalar

```bash
pip install nltk spacy textblob
python -m spacy download en_core_web_sm    # English
python -m spacy download ru_core_news_sm   # Russian (uzbek uchun yaqinroq)
python -m spacy download xx_ent_wiki_sm    # Multilingual

pip install gensim                          # Word2Vec, topic modeling
pip install langdetect polyglot            # Language detection

pip install scikit-learn                   # TF-IDF
```

## NLP masala turlari

| Task | Misol | Approach |
|------|-------|----------|
| **Text Classification** | Sentiment, spam, news category | TF-IDF + LR, BERT |
| **Named Entity Recognition (NER)** | "Toshkent" → LOC | spaCy, BERT-NER |
| **Part-of-Speech (POS) Tagging** | "yugurish" → VERB | spaCy |
| **Dependency Parsing** | Subject-verb-object | spaCy |
| **Text Generation** | Auto-complete | GPT, T5 |
| **Translation** | EN → UZ | MarianMT, GPT-4 |
| **Summarization** | Long → short text | BART, T5, GPT |
| **Question Answering** | Q + Context → Answer | BERT, RoBERTa |
| **Topic Modeling** | Articles → topics | LDA, BERTopic |
| **Speech to Text** | Audio → text | Whisper |
| **Text Similarity** | Sentence pairs | Sentence-BERT |

## Kod misollari

### NLTK — klassik NLP

```python
import nltk
nltk.download(['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger'])

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "Natural Language Processing is amazing! It allows computers to understand human language."

# Sentence tokenization
sents = sent_tokenize(text)
# ['Natural Language Processing is amazing!', 'It allows computers to understand human language.']

# Word tokenization
words = word_tokenize(text)
# ['Natural', 'Language', 'Processing', 'is', ...]

# Stop words removal
stop_words = set(stopwords.words('english'))
filtered = [w for w in words if w.lower() not in stop_words and w.isalpha()]

# Stemming
stemmer = PorterStemmer()
stems = [stemmer.stem(w) for w in filtered]
# 'amazing' → 'amaz', 'computers' → 'comput'

# Lemmatization (POS-aware, yaxshiroq)
lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(w.lower()) for w in filtered]
# 'computers' → 'computer'
```

### spaCy — modern NLP pipeline

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion in 2024.")

# Tokenization + POS + NER + DEP
for token in doc:
    print(f"{token.text:15s} {token.pos_:10s} {token.dep_:10s} {token.lemma_}")

# Named Entity Recognition
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
# Output:
# Apple                ORG
# U.K.                 GPE
# $1 billion           MONEY
# 2024                 DATE

# Noun chunks
for chunk in doc.noun_chunks:
    print(chunk.text)
```

### TF-IDF — Bag of Words

```python
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    "Natural language processing is fun",
    "Machine learning powers natural language processing",
    "Deep learning has revolutionized NLP",
    "Backend development requires understanding APIs",
]

vectorizer = TfidfVectorizer(
    max_features=100,
    ngram_range=(1, 2),       # unigrams + bigrams
    stop_words="english",
    min_df=1,
    max_df=0.95,
)

X = vectorizer.fit_transform(corpus)
print(X.shape)                                # (4, 100)
print(vectorizer.get_feature_names_out()[:10])
```

### Text classification — Naive Bayes baseline

```python
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000)),
])

pipeline.fit(train_texts, train_labels)
accuracy = pipeline.score(test_texts, test_labels)

# Yangi text uchun
prediction = pipeline.predict(["This product is excellent!"])
```

### Word2Vec — embeddings

```python
from gensim.models import Word2Vec

sentences = [
    ["natural", "language", "processing"],
    ["machine", "learning", "models"],
    ["deep", "learning", "neural", "networks"],
    # ...
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4,
    epochs=10,
)

# Bitta so'z vektori
vec = model.wv["natural"]                     # shape (100,)

# Eng o'xshash so'zlar
similar = model.wv.most_similar("natural", topn=5)

# So'zlar orasidagi cosine similarity
sim = model.wv.similarity("language", "processing")
```

### Pretrained embeddings (GloVe)

```python
import gensim.downloader

# 100MB GloVe (Wikipedia 6B tokens)
model = gensim.downloader.load("glove-wiki-gigaword-100")

print(model["king"].shape)                    # (100,)
print(model.most_similar("king", topn=5))
print(model.most_similar(positive=["king", "woman"], negative=["man"]))
# → "queen" yaqin natija
```

### Language detection

```python
from langdetect import detect, detect_langs

print(detect("Salom! Mening ismim Ali."))     # uz (yoki uz hidoyat, ko'p hollarda)
print(detect_langs("Hello, how are you?"))    # [en:0.99]
```

## O'zbek tili uchun NLP

### Hozirgi vaziyat
- Resurs **kam**: nlp uchun pretrained o'zbek modellari ozchilik
- Yaxshi tomonlari: **multilingual modellar**(mBERT, XLM-R, mT5) o'zbek tilini qisman qo'llab-quvvatlaydi
- **Latin va Kirill**ikkalasini ham hisobga olish kerak

### Foydali resurslar
- **HuggingFace'da o'zbek modellari**(qidirish: `uzbek`)
- **OpenAI/Anthropic** — GPT-4 va Claude o'zbek tilini yaxshi tushinadi (Oy 5)
- **Whisper** — o'zbek nutqni transkripsiya qila oladi
- **Common Voice — Uzbek dataset**(Mozilla)

### O'zbek matn bilan ishlash

```python
import spacy

# Multilingual model (o'zbek qisman)
nlp = spacy.load("xx_ent_wiki_sm")

text = "Toshkent shahri 2024 yilda yangi loyihalar boshladi."
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)

# Better: HuggingFace XLM-R based (Oy 5)
```

### Lotin ↔ Kirill konvertor (sodda)

```python
LATIN_TO_CYRILLIC = {
    "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я", "o'": "ў", "g'": "ғ",
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ",
    "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о",
    "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в",
    "x": "х", "y": "й", "z": "з", "'": "ъ",
}

def latin_to_cyrillic(text: str) -> str:
    result = text.lower()
    # 2-character first
    for lat, cyr in sorted(LATIN_TO_CYRILLIC.items(), key=lambda x: -len(x[0])):
        result = result.replace(lat, cyr)
    return result
```

## Backend integratsiyasi

### Text classification API

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
pipeline = joblib.load("text_classifier.joblib")  # TfidfVectorizer + Classifier

class TextInput(BaseModel):
    text: str
    language: str = "en"

@app.post("/classify")
def classify_text(data: TextInput):
    prediction = pipeline.predict([data.text])[0]
    proba = pipeline.predict_proba([data.text])[0]
    
    return {
        "predicted_class": str(prediction),
        "confidence": float(proba.max()),
        "all_probabilities": dict(zip(pipeline.classes_, proba.tolist())),
    }
```

### Sentiment + NER endpoint

```python
import spacy

nlp_en = spacy.load("en_core_web_sm")

@app.post("/analyze")
def analyze_text(data: TextInput):
    doc = nlp_en(data.text)
    
    entities = [
        {"text": ent.text, "type": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
    ]
    
    pos_counts = {}
    for token in doc:
        pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
    
    return {
        "entities": entities,
        "pos_distribution": pos_counts,
        "tokens": len(doc),
        "sentences": len(list(doc.sents)),
    }
```

### Text similarity service

```python
import gensim.downloader as api
import numpy as np

model = api.load("glove-wiki-gigaword-100")

def text_to_vector(text: str) -> np.ndarray:
    words = text.lower().split()
    vectors = [model[w] for w in words if w in model]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@app.post("/similarity")
def similarity(text1: str, text2: str):
    v1 = text_to_vector(text1)
    v2 = text_to_vector(text2)
    return {"similarity": float(cosine_similarity(v1, v2))}
```

## Resurslar

- **NLTK Book** — [nltk.org/book](https://www.nltk.org/book/)
- **spaCy docs** — [spacy.io](https://spacy.io/)
- **"Speech and Language Processing"** — Jurafsky & Martin (free PDF — bibliya)
- **HuggingFace NLP Course** — bepul, Oy 5 uchun tayyorgarlik
- **Stanford NLP videos** — Chris Manning
- **gensim docs** — Word2Vec, topic modeling

## 🏋️ Mashqlar

### 🟢 Easy
1. Bir matnni tokenize qiling, stop words olib tashlang, lemmatize qiling.
2. spaCy bilan POS tagging va NER.
3. TF-IDF bilan 5 ta hujjat orasida o'xshashlikni hisoblang.

### 🟡 Medium
1. **News classification**: 4-5 ta kategoriya (BBC dataset), TF-IDF + Logistic Regression, 90%+ accuracy.
2. **Spam classifier**: SMS Spam dataset, Naive Bayes vs LogReg solishtirish.
3. **NER pipeline**: matnda nomlangan obyektlarni topib, tip bo'yicha guruhlash.

### 🔴 Hard
1. **Uzbek text classifier**: o'zingiz Telegram channellardan dataset to'plang (2-3 kategoriya), TF-IDF + LR baseline.
2. **NER service**: FastAPI + spaCy + caching (Redis) — yuqori RPS uchun optimize.
3. **Topic modeling**: 1000+ ta hujjatlarni LDA yoki BERTopic bilan topic'larga ajrating, vizualizatsiya qiling.

## Capstone

`notebooks/month-04/04_nlp_basics.ipynb`:
- **Loyiha:**O'zbek tilidagi yangiliklar (Daryo.uz, Kun.uz) yoki Telegram channellardan dataset
- TF-IDF + Logistic Regression bilan baseline classifier
- spaCy multilingual bilan NER
- Word2Vec o'rgatib similar so'zlarni topish
- FastAPI servisi

## ✅ Tekshirish ro'yxati

- [ ] Tokenization, stemming, lemmatization farqini bilaman
- [ ] BoW va TF-IDF ni ishlatishni bilaman
- [ ] spaCy bilan NER, POS, parsing
- [ ] Word2Vec va GloVe embedding'larini ishlataman
- [ ] Text classification baseline (TF-IDF + LR)
- [ ] O'zbek tili uchun NLP cheklovlarini bilaman
- [ ] FastAPI'da NLP endpoint yarata olaman

[Text Preprocessing](./05-text-preprocessing.md) ga o'tamiz.
