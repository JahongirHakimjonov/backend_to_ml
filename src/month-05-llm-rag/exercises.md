# Oy 5 — Mashqlar to'plami

## 🟢 Easy

### LLM Fundamentals
1. `tiktoken` bilan inglizcha va o'zbekcha matnda token solishtirish.
2. 5 ta modelni (GPT-4o-mini, Claude Haiku, Gemini Flash, Llama 3.1, Mistral) bir xil savol bilan.
3. Temperature 0, 0.5, 1.5 — javob farqlarini ko'rish.

### Prompt Engineering
1. Zero-shot, few-shot, CoT — bir xil masala uchun.
2. Instructor bilan structured Pydantic output.
3. JSON output uchun prompt + validation.

### APIs
1. OpenAI streaming chat.
2. Anthropic prompt caching.
3. Function calling — 3 ta tool.

### Vector DB
1. ChromaDB'da 100 ta hujjat.
2. Qdrant Docker setup.
3. pgvector Postgres extension.

### RAG
1. Naive RAG — 10 hujjat, query.
2. Citation — `[Source N]` format.
3. Chunking strategiyalari solishtirish.

### Agents
1. Pydantic AI agent + 3 tool.
2. CrewAI hello world.
3. LangGraph oddiy workflow.

### Fine-tuning
1. Pretrained Llama 1B yuklash.
2. 50 ta sintetik dataset (GPT bilan).
3. LoRA config sintaksis tushunish.

## 🟡 Medium

### Real loyihalar
1. **Multi-turn chatbot**: history saqlash, context window manage.
2. **RAG over Wikipedia**: 100 ta o'zbek Wikipedia maqolasi.
3. **PDF Q&A bot**: PyPDF + Qdrant + Streamlit.
4. **Code review agent**: GitHub PR diff → suggestions.
5. **Email summarizer**: 50 ta email → daily digest.

### Advanced techniques
1. **Multi-query RAG**: query expansion bilan.
2. **HyDE**: hypothetical embeddings.
3. **Hybrid search**: dense + BM25.
4. **Reranking**: cross-encoder bilan.
5. **Multi-agent**: CrewAI 3 agentli tizim.

### Fine-tuning
1. **TinyLlama**: o'zbek instruction dataset bilan QLoRA (Colab).
2. **OpenAI fine-tuning**: customer support classifier ($1 budget).
3. **Sintetik data**: GPT-4 yordamida 500+ training pairs.

## 🔴 Hard (Production)

### 1. Documentation Q&A Bot

**Talab:**
- 100+ ta hujjat (PDF, markdown, websites) ingestion
- Qdrant + FastAPI + Celery
- Multi-query + reranking
- Citation va source links
- Streamlit UI
- Langfuse observability
- Cost tracking per user

### 2. AI Customer Support Agent

**Talab:**
- Telegram bot (aiogram)
- Multi-turn conversation
- Tools: FAQ search, order lookup, refund process, escalate to human
- LangGraph workflow
- Postgres memory
- Sentiment-based routing
- Admin dashboard

### 3. RAG Evaluation Framework

**Talab:**
- Test set yaratish (100+ Q&A pairs)
- RAGAS bilan automated evaluation
- A/B testing framework
- Continuous improvement loop
- Grafana dashboard

### 4. Domain-specific Fine-tuning Pipeline

**Talab:**
- Data collection + cleaning
- Synthetic data augmentation
- QLoRA fine-tuning (Llama 3.1 8B)
- vLLM serving
- Benchmark (vs base model)
- Production rollout strategy

## 🏆 Mini-loyihalar

### Mini-loyiha 1: Voice-to-Text Meeting Assistant
- Whisper (audio transcription)
- LLM summarization
- Action items extraction
- Slack integration

### Mini-loyiha 2: Code Review Bot
- GitHub webhook
- Diff parsing
- LLM analysis (security, performance)
- Inline PR comments

### Mini-loyiha 3: Personal Knowledge Base
- Notion + Obsidian export
- Vector DB ingestion
- "Second brain" chatbot
- Smart search

### Mini-loyiha 4: O'zbek Tilidagi Hukumat Hujjatlari Chatbot
- lex.uz, data.gov.uz scraping
- Multi-language (uz/ru)
- Citation
- Legal disclaimer

## 🧪 Quiz

### LLM
1. Token, context window, temperature, top_p — har birini tushuntiring.
2. Pretraining, SFT, RLHF — qanday navbat?
3. Hallucination nima va qanday kamaytirish?
4. Proprietary vs Open Source LLM — tanlov mezonlari?
5. Prompt caching qanday ishlaydi?

### Prompt Engineering
1. Zero-shot, few-shot, CoT qachon qaysi?
2. Structured output (JSON) uchun pattern'lar?
3. Prompt injection — xavf va himoya?
4. Self-consistency texnikasi?
5. ReAct pattern intuition?

### RAG
1. RAG vs Fine-tuning farqi?
2. Chunking strategiyalari trade-off?
3. HNSW algoritm qanday ishlaydi?
4. Hybrid search nima?
5. Cross-encoder reranking nima uchun yaxshilanish keltiradi?

### Agents
1. Agent va LLM call farqi?
2. ReAct pattern — Thought/Action/Observation?
3. Multi-agent qachon kerak?
4. MCP (Model Context Protocol) nima?
5. Agent xavfsizligi — sandbox patternlar?

### Fine-tuning
1. LoRA mathematik intuition?
2. QLoRA — nima uchun 4-bit?
3. Sintetik data generation strategiyalari?
4. RAG vs Fine-tuning — qachon birinchisini, qachon ikkinchisini?
5. vLLM nima uchun production'da tez?

## ✅ Oy 5 oxiri checklist

- [ ] LLM API'larni (OpenAI, Anthropic) ishlataman
- [ ] Prompt engineering texnikalarini bilaman
- [ ] Structured output (Instructor, Pydantic AI)
- [ ] Vector DB (kamida 2 ta) bilan tanish
- [ ] To'liq RAG pipeline yaratdim
- [ ] AI Agent (tool use) yozdim
- [ ] LoRA bilan kichik fine-tuning sinab ko'rdim
- [ ] Production'ga olib chiqdim (FastAPI + Docker)
- [ ] Langfuse / observability
- [ ] Capstone loyiha (chatbot/RAG)
- [ ] LinkedIn'ga post

Tabriklayman! 🎉 [Oy 6 — MLOps va Production](../month-06-mlops-production/README.md) — sizning asosiy maqsadingiz uchun eng muhim oy.
