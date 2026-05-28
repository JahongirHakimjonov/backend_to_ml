# Text Preprocessing

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Real, "iflos" matn ma'lumotlarini tozalashni bilasiz
- Regex bilan murakkab pattern'larni topa olasiz
- HuggingFace tokenizer'lar bilan ishlay olasiz
- Production tekstual pipeline yoza olasiz

## 📖 Nimani o'rganish kerak

- **Text cleaning** — HTML, URL, emoji, punctuation
- **Unicode normalization** — NFC, NFD, NFKC
- **Encoding issues** — UTF-8, Windows-1251, latin1
- **Regex** — pattern matching, capture groups
- **Subword tokenization** — BPE, WordPiece, SentencePiece
- **HuggingFace `tokenizers`** library
- **Truncation va padding strategiyalari**
- **Multi-language handling**

## 📦 Kutubxonalar

```bash
pip install nltk spacy transformers tokenizers ftfy unidecode emoji
pip install beautifulsoup4 lxml                  # HTML parsing
```

## 🧠 Muhim mavzular

### Text cleaning pipeline

Real matn shu kabi ko'rinishda keladi:
```
"<p>Salom!!! 😊 Mening email: ali@gmail.com,&nbsp;telefon: +99890-123-45-67. Marketing manager 🚀</p>"
```

Bizning vazifa — uni ML uchun "toza" qilish:
```
"salom mening email telefon marketing manager"
```

### Subword Tokenization — nima va nima uchun?

Klassik word-level tokenization muammosi:
- Vocabulary juda katta (millionlab so'z)
- "running", "runs", "runner" — alohida ushlanadi
- Unknown words (OOV) — `[UNK]` ga aylanadi

**Subword tokenization yechimi:**

| Algorithm | Where used |
|-----------|------------|
| **BPE (Byte-Pair Encoding)** | GPT, RoBERTa, Llama |
| **WordPiece** | BERT, DistilBERT |
| **SentencePiece (BPE/Unigram)** | T5, Llama, ALBERT, multilingual models |

Misol (BPE):
```
"unfortunately" → ["un", "for", "tun", "ate", "ly"]
```

Yangi so'z ham bo'laklarga ajraladi, OOV muammosi yo'q.

## 💻 Kod misollari

### Asosiy text cleaning

```python
import re
from bs4 import BeautifulSoup
import emoji
import unicodedata

def clean_text(text: str) -> str:
    # 1. HTML olib tashlash
    text = BeautifulSoup(text, "lxml").get_text()
    
    # 2. URL'lar
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
    # 3. Email'lar
    text = re.sub(r"\S+@\S+", "", text)
    
    # 4. Telefon raqamlari (oddiy)
    text = re.sub(r"\+?\d[\d\-\s\(\)]{7,}\d", "", text)
    
    # 5. Emoji'larni text'ga aylantirish yoki olib tashlash
    text = emoji.demojize(text, delimiters=("", ""))    # 😊 → smiling_face
    # yoki: text = emoji.replace_emoji(text, "")
    
    # 6. Unicode normalize
    text = unicodedata.normalize("NFKC", text)
    
    # 7. Special chars — faqat alphanumeric + space
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    
    # 8. Ko'p bo'sh joylar
    text = re.sub(r"\s+", " ", text).strip()
    
    # 9. Lowercase
    text = text.lower()
    
    return text

# Test
dirty = "<p>Salom!!! 😊 Mening email: ali@gmail.com.</p>"
print(clean_text(dirty))
# "salom mening email"
```

### Encoding fix (ftfy)

```python
from ftfy import fix_text

broken = "â€œHelloâ€\x9d"  # noto'g'ri encoded
print(fix_text(broken))
# "Hello"
```

### Regex patternlari (foydali)

```python
import re

# Hashtag'lar (#ai #machinelearning)
hashtags = re.findall(r"#(\w+)", text)

# Mention'lar (@username)
mentions = re.findall(r"@(\w+)", text)

# Sanalar (2024-05-28, 28/05/2024)
dates = re.findall(r"\b\d{4}[-/]\d{2}[-/]\d{2}\b|\b\d{2}[-/]\d{2}[-/]\d{4}\b", text)

# Telefon raqamlari (UZ)
phones = re.findall(r"\+998[\s\-]?\d{2}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", text)

# IP addresses
ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text)

# URL'lar
urls = re.findall(r"https?://[^\s<>\"'{}|\\^`\[\]]+", text)
```

### HuggingFace Tokenizer

```python
from transformers import AutoTokenizer

# BERT
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

text = "Salom dunyo! Bu mashina o'rganish."
tokens = tokenizer.tokenize(text)
# ['sal', '##om', 'duny', '##o', '!', 'bu', 'mash', '##ina', "'", 'ran', '##ish', '.']

# Token IDs
ids = tokenizer.encode(text, add_special_tokens=True)
# [101, ..., 102]  ([CLS] va [SEP] qo'shildi)

# Decode (orqaga)
decoded = tokenizer.decode(ids)

# Batch processing (padding + truncation)
batch = ["Salom!", "Bu uzunroq matn. Bir necha gap bor."]
encoded = tokenizer(
    batch,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt",
)
# {'input_ids': tensor(...), 'attention_mask': tensor(...), 'token_type_ids': tensor(...)}
```

### Custom BPE tokenizer (HuggingFace tokenizers)

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# 1. Train custom tokenizer
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

trainer = BpeTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
)

files = ["data/uzbek_corpus.txt"]
tokenizer.train(files, trainer)

# 2. Save / load
tokenizer.save("uzbek_bpe.json")
tokenizer = Tokenizer.from_file("uzbek_bpe.json")

# 3. Encode
encoded = tokenizer.encode("Salom dunyo")
print(encoded.tokens)
print(encoded.ids)
```

### Truncation va padding strategiyalari

```python
texts = [
    "Short text",
    "Medium length text with some more words",
    "Very long text " * 100,
]

# Truncation: max_length'gacha qisqartirish
encoded = tokenizer(
    texts,
    truncation=True,        # max_length'dan oshganini kesish
    max_length=128,
    padding="max_length",   # 128'gacha [PAD] bilan to'ldirish
    return_tensors="pt",
)

# Boshqa padding strategiyalari:
# padding="longest" — eng uzun matnga moslash (memory tejaydi)
# padding=False — padding yo'q (single sample uchun)

# Dynamic padding (batch ichida eng uzun):
encoded = tokenizer(texts, padding=True, truncation=True, max_length=512)
```

### Sliding window — uzun matnlar uchun

```python
def chunk_text(text: str, tokenizer, max_length: int = 512, stride: int = 50):
    """Uzun matnni overlapping chunks'ga ajratish."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    
    for i in range(0, len(tokens), max_length - stride):
        chunk_tokens = tokens[i:i + max_length]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

# Misol: 10000 token matn → 20 ta 512-token chunk
long_text = "..." * 5000
chunks = chunk_text(long_text, tokenizer, max_length=512, stride=50)
```

### Multi-language handling

```python
from langdetect import detect

def preprocess_multilingual(text: str) -> dict:
    lang = detect(text)
    
    if lang == "en":
        cleaned = clean_text_english(text)
    elif lang == "uz":
        cleaned = clean_text_uzbek(text)
    elif lang == "ru":
        cleaned = clean_text_russian(text)
    else:
        cleaned = clean_text(text)
    
    return {"language": lang, "cleaned_text": cleaned}
```

## 🔌 Backend integratsiyasi

### Text preprocessing service

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str
    operations: list[str] = ["clean", "tokenize"]

class TextOutput(BaseModel):
    original: str
    cleaned: str
    tokens: list[str]
    language: str
    stats: dict

@app.post("/preprocess", response_model=TextOutput)
def preprocess(data: TextInput):
    original = data.text
    cleaned = clean_text(original) if "clean" in data.operations else original
    tokens = tokenizer.tokenize(cleaned) if "tokenize" in data.operations else []
    
    return TextOutput(
        original=original,
        cleaned=cleaned,
        tokens=tokens,
        language=detect(original) if original.strip() else "unknown",
        stats={
            "original_length": len(original),
            "cleaned_length": len(cleaned),
            "token_count": len(tokens),
        },
    )
```

### Bulk processing (Celery)

```python
@celery_app.task
def preprocess_dataset(csv_path: str, text_column: str):
    df = pd.read_csv(csv_path)
    df["cleaned"] = df[text_column].apply(clean_text)
    
    output_path = csv_path.replace(".csv", "_cleaned.csv")
    df.to_csv(output_path, index=False)
    
    return {"output": output_path, "n_rows": len(df)}
```

## 📚 Resurslar

- **HuggingFace Tokenizers docs** — [huggingface.co/docs/tokenizers](https://huggingface.co/docs/tokenizers/)
- **"Natural Language Processing with Transformers"** — Lewis Tunstall (O'Reilly)
- **Regex101** — [regex101.com](https://regex101.com/) (interactive regex tester)
- **Unicode normalization** — Unicode.org docs
- **ftfy library** — [github.com/rspeer/python-ftfy](https://github.com/rspeer/python-ftfy)

## 🏋️ Mashqlar

### 🟢 Easy
1. Yuqoridagi `clean_text` funksiyasini "dirty" o'zbek matnda sinab ko'ring.
2. Regex bilan matnda telefon raqamlarini toping.
3. BERT tokenizer bilan o'zbek matn — qancha token chiqadi?

### 🟡 Medium
1. **Custom BPE**: 100MB o'zbek matnda BPE tokenizer o'rgating, default `bert-multilingual` bilan vocabulary'ni solishtiring.
2. **Sliding window**: 50,000 so'zli kitobni 512-token chunks'ga ajrating.
3. **Multi-language preprocessor**: tilga qarab turli preprocessing pipeline qo'llaydigan class.

### 🔴 Hard
1. **Production text pipeline**: Kafka stream'dan kelayotgan matnni real-time clean/tokenize/embed qiladigan FastAPI servisi.
2. **Custom tokenizer service**: REST API'da custom tokenizer training va inference.
3. **NER + Anonymization**: matndagi PII (personal info) ni topib `[NAME]`, `[EMAIL]`, `[PHONE]` placeholders'ga almashtirish (GDPR uchun).

## 🚀 Capstone

`notebooks/month-04/05_text_preprocessing.ipynb`:
- O'zbek Telegram channel postlaridan 10,000 ta xabar yig'ing
- To'liq cleaning pipeline qurish
- Custom BPE tokenizer
- Pretrained BERT tokenizer bilan solishtirish (vocab coverage, OOV rate)

## ✅ Tekshirish ro'yxati

- [ ] HTML, URL, email, telefon olib tashlashni bilaman
- [ ] Unicode normalization (NFKC) nima
- [ ] Regex bilan ishlay olaman
- [ ] BPE/WordPiece subword tokenization'ni tushunaman
- [ ] HuggingFace tokenizer bilan ishlash
- [ ] Truncation va padding strategiyalari
- [ ] Custom BPE tokenizer o'rgata olaman
- [ ] Multi-language preprocessing pipeline

[Transformers ga kirish](./06-transformers-intro.md) ga o'tamiz.
