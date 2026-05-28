# LLM fundamentals

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- LLM nima ekanini, qanday ishlashini tushunasiz
- Model turlari (proprietary vs open source) farqini bilasiz
- Token, context window, temperature kabi terminlarni to'g'ri ishlatasiz
- Modellarning kuchli/zaif tomonlarini bilasiz va to'g'ri tanlay olasiz

## Nimani o'rganish kerak

- **LLM arxitekturasi** — Transformer decoder
- **Training stages** — pretraining, SFT, RLHF
- **Token va tokenization** — qanday hisoblash, narxlash
- **Context window** — 4K → 1M+ evolyutsiyasi
- **Temperature, top_p, top_k** — sampling parametrlari
- **Hallucination** — nima va qanday kamaytirish
- **Modeling family** — GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama (Meta), Mistral, Qwen, DeepSeek

## Muhim mavzular

### LLM qanday ishlaydi (sodda)

```
Input:  "Bugun havo juda"
              ↓
        LLM (50B parametr)
              ↓
Output: probability distribution next token
        "yaxshi" 0.45
        "sovuq" 0.20
        "issiq" 0.15
        ...
              ↓
        Sampling (temperature)
              ↓
        "yaxshi"

Keyin "Bugun havo juda yaxshi" → keyingi token, va h.k.
```

LLM — bu **next-token predictor**. U bitta navbatdagi tokenni bashorat qiladi.

### Token nima?

```
"Salom dunyo!" → ["Sal", "om", " duny", "o", "!"]
                  5 ta token (taxminan, model'ga qarab)

GPT-4 narxlash:
- Input: $2.50 / 1M tokens
- Output: $10 / 1M tokens

Bizning chatbot $0.001 / xabar (taxminan, GPT-4o-mini bilan)
```

**Tilga qarab token narxi:**
- Inglizcha — eng arzon (1 word ≈ 1.3 token)
- O'zbek/Rus — qimmatroq (1 word ≈ 2-3 token)
- Xitoycha — har character bir necha token

### Context Window

Model bir vaqtda qancha tokenni "ko'ra oladi":

| Model | Context window |
|-------|----------------|
| GPT-3.5 | 16K |
| GPT-4 | 128K |
| GPT-4o | 128K |
| Claude 4.6 Sonnet | 200K (1M beta) |
| Claude 4.7 Opus | 200K (1M extended) |
| Gemini 2.5 Pro | 1M-2M |
| Llama 3.1 | 128K |

**Context window'ga kiradi:**
- System prompt
- Tarixiy xabarlar
- User input
- LLM response (output)

Hammasi birga **input + output context window'dan kichik bo'lishi kerak**.

### Training stages

```
1. Pretraining (asosiy)
   - Trillions of tokens (internet, kitoblar)
   - Next-token prediction
   - Result: "base model" — completion qila oladi

2. SFT (Supervised Fine-Tuning)
   - Sifatli (prompt, response) juftliklari
   - Instruction following
   - Result: "instruct model"

3. RLHF (Reinforcement Learning from Human Feedback)
   - Human preferences asosida
   - Yaxshiroq, foydaliroq, xavfsizroq
   - Result: "chat model" (production-ready)
```

### Temperature va sampling

```python
# temperature=0.0 — deterministik (bir xil prompt → bir xil javob)
# temperature=1.0 — default, balanced
# temperature=2.0 — chaotic, creative

# top_p (nucleus sampling)
# top_p=1.0 — barchasidan tanlash
# top_p=0.9 — top 90% cumulative probability'dan tanlash

# top_k
# top_k=50 — faqat top 50 tokendan tanlash
```

**Qachon qaysi?**

| Task | Temperature | Top_p |
|------|-------------|-------|
| Faktual savol | 0.0-0.3 | 0.95 |
| Kod yozish | 0.0-0.2 | 0.95 |
| Translation | 0.3 | 0.9 |
| Creative writing | 0.7-1.0 | 0.9 |
| Brainstorming | 1.0-1.5 | 0.9 |

### Hallucination

LLM **ishonchli ko'rinishda**noto'g'ri javob bera oladi:
- "Toshkent metrosida 24 ta stansiya bor" (haqiqatda 30+)
- "Python'da `dict.merge()` methodi bor" (yo'q, `dict | dict` yoki `.update()`)

**Sabablari:**
1. Training data eski yoki noto'g'ri
2. Internal knowledge cheklangan
3. Model "bilmasligini" tan olmaydi

**Yechimlar:**
1. **RAG** — real ma'lumotlardan kontekst berish
2. **Tool use** — calculator, search, DB query
3. **Prompt engineering** — "Bilmasangiz 'Bilmayman' deng"
4. **Citation** — javob qaerdan olinganini ko'rsatish

### Proprietary vs Open Source

| | Proprietary (GPT, Claude) | Open Source (Llama, Mistral) |
|---|--------------------------|----------------------------|
| **Sifat** | Eng yuqori | Yaxshi (Llama 3.1 ≈ GPT-3.5) |
| **Narx** | Per-token | Hosting cost (yoki bepul lokal) |
| **Privacy** | Cloud — ma'lumot tashqariga | Lokal — privacy 100% |
| **Customization** | Cheklangan (fine-tuning API) | To'liq (LoRA, full FT) |
| **Latency** | Tezroq | Hardware'ga bog'liq |
| **Offline** | Yo'q | Ha |
| **Compliance** | GDPR, SOC2 ta'minlangan | O'zingiz |

### Model family'lar (2024-2026)

#### OpenAI
- **GPT-4o** — multimodal (image, audio, text)
- **GPT-4o-mini** — eng arzon flagship
- **o1, o3** — reasoning models (matematika, kod)

#### Anthropic
- **Claude Opus 4.7** — eng kuchli, 1M context (extended)
- **Claude Sonnet 4.6** — balanced (speed/cost/quality)
- **Claude Haiku 4.5** — eng tez va arzon

#### Google
- **Gemini 2.5 Pro** — 1M context
- **Gemini 2.5 Flash** — tez va arzon
- **Gemma 2** — open weights

#### Meta (open)
- **Llama 3.1** — 8B, 70B, 405B
- **Llama 3.2** — multimodal versiyalar

#### Boshqalar (open)
- **Mistral / Mixtral** — Europe (MoE arxitektura)
- **Qwen 2.5** — Alibaba (kuchli multilingual)
- **DeepSeek V3** — kuchli reasoning model

## Kod misollari (kirish)

### Token sanash

```python
import tiktoken

# OpenAI uchun
enc = tiktoken.encoding_for_model("gpt-4o")
text = "Salom dunyo, mashina o'rganish qiziq"
tokens = enc.encode(text)
print(f"Token count: {len(tokens)}")
print(f"Tokens: {tokens}")

# Approximate (boshqa modellar uchun)
# 1 token ≈ 4 chars (English), ≈ 2 chars (uzbek/rus)
def estimate_tokens(text: str) -> int:
    return len(text) // 3  # rough
```

### Context window monitoring

```python
class ConversationManager:
    def __init__(self, max_tokens: int = 100_000):
        self.max_tokens = max_tokens
        self.messages = []
        self.enc = tiktoken.encoding_for_model("gpt-4o")
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._truncate_if_needed()
    
    def _count_tokens(self) -> int:
        return sum(len(self.enc.encode(m["content"])) for m in self.messages)
    
    def _truncate_if_needed(self):
        """System message'ni saqlab, eskilarni o'chirish."""
        while self._count_tokens() > self.max_tokens and len(self.messages) > 2:
            # System message (index 0) ni saqlash
            self.messages.pop(1)
```

### Cost calculator

```python
PRICES = {
    "gpt-4o": {"input": 2.50, "output": 10.00},          # $ per 1M tokens
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-opus-4-7": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICES[model]
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
```

## Backend integratsiyasi (preview)

Keyingi boblarda batafsil. Mental model:

```
User → FastAPI → LLM API → Response
              ↓
           PostgreSQL (history)
              ↓
           Redis (caching)
              ↓
           Sentry / Datadog (observability)
```

LLM API call — bu **HTTP request**, faqat AI tomonida. Backend uchun siz allaqachon:
- Retry logic bilan ishlay olasiz
- Timeout va circuit breaker
- Rate limiting
- Async (FastAPI'da `async def`)
- Streaming responses (SSE yoki WebSocket)

## Resurslar

- **Andrej Karpathy — "Intro to LLMs"**(YouTube, 1 soat) — **MUST WATCH**
- **3Blue1Brown — "But what is GPT?"**(vizual tushuntirish)
- **Anthropic Cookbook** — [github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)
- **OpenAI Cookbook** — [cookbook.openai.com](https://cookbook.openai.com/)
- **"Hands-On Large Language Models"** — Jay Alammar va Maarten Grootendorst (O'Reilly, 2024)
- **Hugging Face NLP Course (LLM section)**
- **Latent Space Podcast** — industry trends

## 🏋️ Mashqlar

### 🟢 Easy
1. `tiktoken` bilan bir nechta inglizcha va o'zbekcha matnda token sonini solishtiring.
2. Different models'ning context window'larini ro'yxat qiling.
3. Bitta savolni 3 ta turli temperature (0, 0.5, 1.5) bilan kerakli LLM'ga yuboring, javoblarni solishtiring.

### 🟡 Medium
1. **Conversation manager**: tarixiy xabarlarni saqlaydigan, context window'dan oshmasligini ta'minlaydigan class.
2. **Cost tracker**: har LLM call'ni log qilib, kunlik/oylik xarajatlar tahlilini chiqarish.
3. **Model comparison**: bir xil 20 ta savolni GPT-4o-mini, Claude Haiku, Llama 3.1 8B'ga yuboring, sifat va vaqt jihatdan solishtiring.

### 🔴 Hard
1. **LLM Router**: input'ga qarab eng arzon va sifatli modelni avtomatik tanlaydigan servis (oddiy savol → Haiku, murakkab → Sonnet, kod → Opus).
2. **Token budget manager**: foydalanuvchining oylik kvota tizimi (FastAPI + Redis + Postgres).

## Capstone

`notebooks/month-05/01_llm_fundamentals.ipynb`:
- 5 ta turli LLM (GPT-4o-mini, Claude Haiku, Gemini Flash, Llama 3.1, Mistral) — bir xil 10 ta savol
- Har biri uchun: javob, vaqt, token soni, cost
- Markdown report yarating

## ✅ Tekshirish ro'yxati

- [ ] LLM next-token prediction'ni tushunaman
- [ ] Token va context window nima
- [ ] Pretraining → SFT → RLHF jarayonini bilaman
- [ ] Temperature, top_p, top_k farqini bilaman
- [ ] Hallucination nima va qanday kamaytirish (RAG, tools)
- [ ] Proprietary va Open Source LLM'lar farqini bilaman
- [ ] Asosiy model family'larni (GPT, Claude, Gemini, Llama) bilaman
- [ ] Cost calculator yoza olaman

[Prompt Engineering](./02-prompt-engineering.md) ga o'tamiz.
