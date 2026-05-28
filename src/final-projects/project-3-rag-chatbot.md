# Loyiha 3: RAG Chatbot

## 🎯 Maqsad

To'liq production-ready RAG (Retrieval Augmented Generation) chatbot. O'zbek tilidagi hujjatlar uchun ko'p tilli, mahalliy kontekstda foydali AI assistant.

## 📋 Tavsiya etilgan use case'lar

| Use case | Manba | Qiyinchilik |
|----------|-------|-------------|
| **O'zbekiston Konstitutsiya/QHK chatbot** | lex.uz | ⭐⭐⭐⭐ |
| **Texnik documentation bot** | GitHub repo docs | ⭐⭐⭐ |
| **Customer support bot** | FAQ + product docs | ⭐⭐⭐ |
| **HR / Internal docs** | Notion / Confluence | ⭐⭐⭐ |
| **Wikipedia chatbot (O'zbek)** | uz.wikipedia.org | ⭐⭐⭐⭐ |
| **Medical knowledge base** | Public medical docs | ⭐⭐⭐⭐⭐ |
| **Legal advice bot** | lex.uz + qonun.uz | ⭐⭐⭐⭐⭐ |

**Tavsiya:** **Texnik documentation bot** (oson) yoki **O'zbek qonunlar chatbot** (zo'r portfolio).

## 🏗 Architecture

```
┌────────────────┐
│  Web / Mobile  │
│  Telegram bot  │
└────────┬───────┘
         │
         ▼
┌────────────────────┐
│   FastAPI + WS     │
│   (Streaming)      │
└──────┬─────────────┘
       │
       ▼
┌──────────────────────────────────┐
│   RAG Pipeline                   │
│  ┌──────────┐  ┌──────────────┐ │
│  │  Query   │─>│  Embedding   │ │
│  │  Routing │  │  (OpenAI)    │ │
│  └──────────┘  └──────┬───────┘ │
│                       ▼          │
│  ┌─────────────────────────────┐ │
│  │  Qdrant Vector Search       │ │
│  │  + BM25 Hybrid + Rerank     │ │
│  └──────────┬──────────────────┘ │
│             ▼                    │
│  ┌─────────────────────────────┐ │
│  │  LLM (Claude / GPT)         │ │
│  │  + Citation                 │ │
│  └──────────┬──────────────────┘ │
└─────────────┼────────────────────┘
              │
              ▼
       ┌──────────────┐
       │  Postgres    │
       │  - History   │
       │  - Feedback  │
       └──────────────┘
              │
              ▼
       ┌──────────────┐
       │  Langfuse    │
       │  Observation │
       └──────────────┘
```

## 📦 Tech Stack

### Required
- **Backend:** FastAPI (streaming + WebSocket)
- **LLM:** OpenAI yoki Anthropic
- **Vector DB:** Qdrant (yoki ChromaDB)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Framework:** LlamaIndex yoki raw API
- **Frontend:** Streamlit yoki Next.js
- **Container:** Docker + docker-compose

### Nice to have
- **Reranking:** Cross-encoder (BAAI)
- **Observability:** Langfuse
- **Telegram bot:** aiogram
- **Cache:** Redis
- **Authentication:** JWT

## 📋 Features

### MVP (1-hafta)
- [ ] Document ingestion (PDF, URL, MD)
- [ ] Chunking + embeddings
- [ ] Qdrant collection
- [ ] FastAPI `/chat` endpoint
- [ ] LLM API integration
- [ ] Citation (basic)
- [ ] Streamlit UI
- [ ] Docker

### V2 (2-hafta)
- [ ] Multi-source ingestion (PDF + URL + Notion)
- [ ] Hybrid search (vector + BM25)
- [ ] Reranking
- [ ] Streaming responses (SSE)
- [ ] Postgres conversation history
- [ ] Multi-turn context
- [ ] Tests
- [ ] CI/CD

### V3 (3-hafta)
- [ ] Telegram bot integration
- [ ] Multi-language (uz/ru/en)
- [ ] Langfuse observability
- [ ] Feedback collection
- [ ] RAGAS evaluation
- [ ] Cloud deployment
- [ ] Blog post

## 📝 API spec

### `POST /ingest`
```bash
# PDF upload
curl -X POST -F "file=@doc.pdf" -F "metadata={\"source\":\"law\"}" http://api/ingest

# URL
curl -X POST -d '{"url":"https://lex.uz/...","metadata":{}}' http://api/ingest
```
```json
{
    "task_id": "uuid",
    "chunks_added": 234
}
```

### `POST /chat`
```json
// Request
{
    "message": "O'zbekistondagi mehnat haftaning maksimal soati nima?",
    "session_id": "uuid",
    "user_id": "user_123",
    "language": "uz"
}

// Response
{
    "answer": "O'zbekiston Mehnat kodeksi 122-moddasiga ko'ra, ish vaqti haftada 40 soatdan oshmasligi kerak [Source 1].",
    "sources": [
        {
            "text": "Ish vaqtining oddiy davomiyligi haftasiga 40 soatdan oshmaydi...",
            "document": "Mehnat kodeksi",
            "section": "Modda 122",
            "url": "https://lex.uz/...#122",
            "score": 0.89
        }
    ],
    "session_id": "uuid",
    "model": "claude-sonnet-4-6",
    "tokens_used": 1245,
    "cost_usd": 0.003,
    "latency_ms": 1230
}
```

### `POST /chat/stream` (SSE)
```
data: {"type": "sources", "data": [...]}
data: {"type": "token", "text": "O'zbekiston "}
data: {"type": "token", "text": "Mehnat "}
...
data: {"type": "done", "total_tokens": 1245}
```

### `POST /feedback`
```json
{
    "session_id": "uuid",
    "message_id": "uuid",
    "rating": "thumbs_up",  // or thumbs_down
    "comment": "Aniq javob"
}
```

### `GET /sessions/{user_id}`
- Conversation history

### `POST /telegram-webhook`
- Telegram bot integration

## 🗂 Project structure

```
rag-chatbot/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── .github/workflows/
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── ingest.py
│   │   │   ├── feedback.py
│   │   │   └── telegram.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── config.py
│   │   └── prompts.py
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   ├── reranking.py
│   │   ├── generation.py
│   │   └── pipeline.py             # full RAG
│   ├── llm/
│   │   ├── openai_client.py
│   │   └── anthropic_client.py
│   ├── vectordb/
│   │   └── qdrant_client.py
│   ├── data/
│   │   └── models.py               # Postgres
│   └── integrations/
│       └── telegram_bot.py
├── tests/
├── evaluation/
│   ├── test_set.json               # 100 Q&A pairs
│   └── ragas_eval.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   └── documents/                  # source files
├── prompts/
│   └── system_v1.md
└── pyproject.toml
```

## 🚀 Implementatsiya plani (3 hafta)

### Hafta 1 — MVP RAG
- Day 1-2: Source documents collection + preparation
- Day 3: Ingestion pipeline (chunking, embeddings, Qdrant)
- Day 4: Basic RAG pipeline (retrieve → LLM → respond)
- Day 5: FastAPI endpoint
- Day 6: Streamlit UI
- Day 7: Docker + GitHub

### Hafta 2 — Advanced RAG
- Day 8: Multi-source ingestion (PDF, URL, MD)
- Day 9: Hybrid search (Qdrant native)
- Day 10: Reranking (cross-encoder)
- Day 11: Streaming SSE
- Day 12: Postgres history + multi-turn
- Day 13: Tests
- Day 14: CI/CD

### Hafta 3 — Production + Evaluation
- Day 15: Telegram bot
- Day 16: Multi-language support
- Day 17: Langfuse observability
- Day 18: Feedback + RAGAS evaluation
- Day 19: Cloud deployment
- Day 20: Demo video
- Day 21: Blog post + LinkedIn

## 📊 Success metrics

### RAG quality (RAGAS metrics)
- **Faithfulness:** > 0.85
- **Answer Relevancy:** > 0.85
- **Context Precision:** > 0.80
- **Context Recall:** > 0.80

### Performance
- **Retrieval latency:** < 500ms
- **End-to-end latency:** < 3s (non-streaming), TTFT < 1s (streaming)
- **Cost per query:** < $0.01

### User satisfaction
- **Thumbs up rate:** > 75%
- **Session retention:** users come back

## 📚 Resurslar

- **LlamaIndex docs** — [docs.llamaindex.ai](https://docs.llamaindex.ai/)
- **Qdrant tutorials** — [qdrant.tech/documentation](https://qdrant.tech/documentation/)
- **OpenAI Cookbook RAG** — examples
- **Langfuse docs** — observability
- **RAGAS docs** — evaluation
- **Anthropic prompt caching** — cost optimization

## 🏆 Bonus features

- **Multi-modal RAG** — text + images (PDFs with charts)
- **Agentic RAG** — LLM tools (search, calculator, DB)
- **Auto-evaluation** — model judging model
- **Custom embedding model** — domain-specific
- **Hybrid retrieval** — vector + BM25 + knowledge graph
- **Multi-language search** — query in EN, docs in UZ
- **Voice interface** — Whisper STT + TTS
- **Mobile app** — React Native

## ✅ Submission checklist

- [ ] 100+ ta hujjat ingestion qilingan
- [ ] Hybrid search + reranking
- [ ] Streaming responses
- [ ] Multi-turn conversation
- [ ] Citation with source links
- [ ] Telegram bot working
- [ ] Multi-language (kamida 2 til)
- [ ] RAGAS evaluation report
- [ ] Langfuse dashboard
- [ ] Streamlit UI live
- [ ] Demo video
- [ ] Blog post

Tugatdingiz? [Loyiha 4: MLOps Pipeline](./project-4-mlops-pipeline.md) — eng katta va eng muhim loyiha.
