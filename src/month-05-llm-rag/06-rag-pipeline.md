# RAG Pipeline

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- RAG (Retrieval Augmented Generation) ning to'liq arxitekturasini bilasiz
- Production-grade RAG pipeline qura olasiz
- Chunking strategiyalarini va trade-off'larni tushunasiz
- Advanced RAG texnikalarini (HyDE, multi-query, re-ranking) qo'llay olasiz
- RAG'ning sifatini o'lchash va yaxshilashni bilasiz

## 📖 Nimani o'rganish kerak

- **RAG arxitekturasi** — Naive, Advanced, Modular
- **Chunking strategiyalari** — fixed, semantic, sliding window, recursive
- **Retrieval strategiyalari** — dense, sparse, hybrid, multi-query
- **Reranking** — Cross-encoder, LLM-based
- **HyDE** (Hypothetical Document Embeddings)
- **Citation va source attribution**
- **Context window management**
- **RAG evaluation** — RAGAS, custom metrics

## 🧠 RAG nima va nima uchun?

### Muammo
LLM hallucination — noto'g'ri ma'lumot bera oladi:
- Training data eski (2024 yilgacha)
- Sizning shaxsiy hujjatlaringizni bilmaydi
- Aniq fakt'larda noto'g'ri javob

### Yechim — RAG
```
1. User savol beradi: "Bizning kompaniya policiyasi nima?"
2. Retrieval: vector DB'dan 5 ta o'xshash chunk olish
3. Augment: chunklarni prompt'ga qo'shish
4. Generate: LLM kontekst asosida javob beradi
5. Cite: qaysi chunkdan olganini ko'rsatish
```

### RAG vs Fine-tuning

| | RAG | Fine-tuning |
|---|-----|-------------|
| **Yangi knowledge** | ✅ Real-time | ❌ Retrain kerak |
| **Citation** | ✅ Aniq | ❌ Qiyin |
| **Cost** | Per-query | One-time + inference |
| **Quality on style** | ❌ O'rta | ✅ Yaxshi |
| **Complexity** | O'rta | Yuqori |
| **Maintenance** | Index update | Retrain |

**Qoida:** Knowledge uchun **RAG**, behavior/style uchun **fine-tuning**.

## 🧠 RAG arxitekturasi

### Naive RAG
```
Query → Embed → Vector DB Search → Top-K chunks → LLM prompt → Answer
```

Muammolar:
- Yomon retrieval → yomon javob
- Chunks contextda qarama-qarshilik
- LLM kontekst'dan tashqarida hallucinatsiya

### Advanced RAG (modern)
```
Query
  ↓
Query Transformation:
  - Multi-query (3 ta variant)
  - HyDE (sintetik javob → embed)
  - Step-back (umumiyroq savol)
  ↓
Hybrid Retrieval:
  - Dense (semantic)
  - Sparse (BM25)
  - Metadata filter
  ↓
Reranking (Cross-encoder)
  ↓
Context Construction:
  - Deduplication
  - Sort by relevance
  - Compress (LLM summary)
  ↓
LLM Generation:
  - Structured prompt
  - Citation markers
  ↓
Post-processing:
  - Source attribution
  - Confidence score
```

## 💻 Kod misollari

### Production RAG pipeline

```python
from dataclasses import dataclass
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from qdrant_client import AsyncQdrantClient
from sentence_transformers import CrossEncoder

@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int
    score: float

@dataclass
class RAGAnswer:
    answer: str
    sources: list[RetrievedChunk]
    confidence: float

class RAGPipeline:
    def __init__(self):
        self.openai = AsyncOpenAI()
        self.anthropic = AsyncAnthropic()
        self.qdrant = AsyncQdrantClient(url="http://localhost:6333")
        self.reranker = CrossEncoder("BAAI/bge-reranker-base")
        self.collection = "docs"
    
    async def embed(self, text: str) -> list[float]:
        response = await self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=[text],
        )
        return response.data[0].embedding
    
    async def retrieve(self, query: str, top_k: int = 20) -> list[RetrievedChunk]:
        embedding = await self.embed(query)
        results = await self.qdrant.search(
            collection_name=self.collection,
            query_vector=embedding,
            limit=top_k,
        )
        return [
            RetrievedChunk(
                text=r.payload["text"],
                source=r.payload.get("source", ""),
                page=r.payload.get("page", 0),
                score=r.score,
            )
            for r in results
        ]
    
    def rerank(self, query: str, chunks: list[RetrievedChunk], top_k: int = 5):
        pairs = [(query, c.text) for c in chunks]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(scores, chunks), key=lambda x: -x[0])
        # Yangi score'ni saqlash
        for new_score, chunk in ranked[:top_k]:
            chunk.score = float(new_score)
        return [c for _, c in ranked[:top_k]]
    
    def build_prompt(self, query: str, chunks: list[RetrievedChunk]) -> str:
        context = "\n\n".join([
            f"[Source {i+1}: {c.source}, page {c.page}]\n{c.text}"
            for i, c in enumerate(chunks)
        ])
        
        return f"""Sen tajribali assistantsan. Quyidagi kontekst asosida savolga aniq javob ber.

QOIDALAR:
1. FAQAT berilgan kontekst asosida javob ber
2. Agar javob kontekstda yo'q bo'lsa, "Berilgan ma'lumotlarda javob topilmadi" deb javob ber
3. Har bir fact uchun [Source N] formatida ko'rsatma ber
4. O'zbek tilida javob ber

KONTEKST:
{context}

SAVOL: {query}

JAVOB:"""
    
    async def generate(self, prompt: str) -> tuple[str, float]:
        response = await self.anthropic.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
        # Confidence estimation (simple heuristic)
        confidence = 0.9 if "[Source" in text else 0.3
        return text, confidence
    
    async def query(self, query: str) -> RAGAnswer:
        # 1. Retrieve
        chunks = await self.retrieve(query, top_k=20)
        
        # 2. Rerank
        top_chunks = self.rerank(query, chunks, top_k=5)
        
        # 3. Build prompt
        prompt = self.build_prompt(query, top_chunks)
        
        # 4. Generate
        answer, confidence = await self.generate(prompt)
        
        return RAGAnswer(
            answer=answer,
            sources=top_chunks,
            confidence=confidence,
        )

# Usage
rag = RAGPipeline()
result = await rag.query("Bizning ish vaqti qaysi?")
print(result.answer)
for src in result.sources:
    print(f"  - {src.source} (p.{src.page}): {src.score:.3f}")
```

### Multi-query — savolni 3 ta variantga ajratish

```python
async def multi_query_search(query: str, top_k: int = 5):
    """Bitta query → 3 ta variant → birlashtirilgan natija."""
    
    # 1. Generate query variants
    variant_prompt = f"""Quyidagi savolni 3 xil yo'l bilan qayta yozing:

Savol: {query}

Variantlar (har birini yangi qatorda):
1.
2.
3."""
    
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": variant_prompt}],
    )
    variants = response.choices[0].message.content.strip().split("\n")
    variants = [v.split(". ", 1)[1] for v in variants if ". " in v]
    
    # 2. Retrieve for each
    all_chunks = []
    for q in [query] + variants:
        chunks = await retrieve(q, top_k=top_k)
        all_chunks.extend(chunks)
    
    # 3. Deduplicate (by id yoki content hash)
    seen = set()
    unique = []
    for c in all_chunks:
        key = hash(c.text[:100])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    
    return unique
```

### HyDE — Hypothetical Document Embeddings

```python
async def hyde_search(query: str, top_k: int = 5):
    """Query'dan to'g'ridan-to'g'ri search emas, sintetik 'javob' yaratib, uni embed."""
    
    # 1. Sintetik javob yaratish
    hypothesis = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": 
            f"Quyidagi savolga to'liq, batafsil javob yozing (haqiqat bo'lmasa ham):\n{query}"}],
    )
    hypothetical_answer = hypothesis.choices[0].message.content
    
    # 2. Hypothetical javobni embed qilish
    embedding = await openai.embeddings.create(
        model="text-embedding-3-small",
        input=[hypothetical_answer],
    )
    
    # 3. Search bu embedding bilan (javob → javob similarity!)
    results = await qdrant.search(
        collection_name="docs",
        query_vector=embedding.data[0].embedding,
        limit=top_k,
    )
    
    return results
```

### Smart chunking strategiyalari

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Strategy 1: Fixed-size (eng oddiy)
fixed = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

# Strategy 2: Markdown-aware
from langchain.text_splitter import MarkdownHeaderTextSplitter

md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
    ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"),
])

# Strategy 3: Semantic (LangChain experimental)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic = SemanticChunker(
    OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type="percentile",
)

# Strategy 4: Sliding window (overlap)
def sliding_window_chunks(text: str, window: int = 500, stride: int = 250):
    chunks = []
    for i in range(0, len(text) - window + 1, stride):
        chunks.append(text[i:i + window])
    return chunks
```

### Context window management

```python
def build_context_within_budget(
    chunks: list[RetrievedChunk],
    max_tokens: int = 8000,
    encoder=tiktoken.encoding_for_model("gpt-4o"),
) -> list[RetrievedChunk]:
    """Faqat budget'ga sig'adigan chunklarni qaytarish."""
    included = []
    total = 0
    
    for chunk in chunks:  # already sorted by relevance
        tokens = len(encoder.encode(chunk.text))
        if total + tokens > max_tokens:
            break
        included.append(chunk)
        total += tokens
    
    return included
```

### RAG evaluation — RAGAS

```python
# pip install ragas

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Test set
data = {
    "question": ["Ish vaqti qaysi?", "Manzil qayerda?"],
    "answer": ["8:00 dan 18:00 gacha", "Toshkent, Yunusobod"],
    "contexts": [
        ["Bizning ish vaqti dushanbadan jumagacha 8:00-18:00"],
        ["Office: Toshkent, Yunusobod tumani"],
    ],
    "ground_truth": ["8:00-18:00", "Toshkent, Yunusobod"],
}

dataset = Dataset.from_dict(data)
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(result)
# {faithfulness: 0.95, answer_relevancy: 0.88, ...}
```

## 🔌 Backend integratsiyasi

### Production RAG FastAPI endpoint

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.rag = RAGPipeline()
    yield

app = FastAPI(lifespan=lifespan)

class RAGRequest(BaseModel):
    query: str
    session_id: str = None
    top_k: int = 5
    rerank: bool = True
    multi_query: bool = False

class RAGResponse(BaseModel):
    answer: str
    sources: list[dict]
    confidence: float
    latency_ms: int

@app.post("/rag/query", response_model=RAGResponse)
async def rag_query(req: RAGRequest):
    start = time.time()
    
    result = await app.state.rag.query(req.query)
    
    # Log for monitoring
    await log_query(
        query=req.query,
        answer=result.answer,
        sources=[s.source for s in result.sources],
        confidence=result.confidence,
        session_id=req.session_id,
    )
    
    return RAGResponse(
        answer=result.answer,
        sources=[
            {"text": s.text[:200], "source": s.source, "page": s.page, "score": s.score}
            for s in result.sources
        ],
        confidence=result.confidence,
        latency_ms=int((time.time() - start) * 1000),
    )
```

### Streaming RAG answer (SSE)

```python
@app.post("/rag/stream")
async def rag_stream(req: RAGRequest):
    # 1. Retrieve (non-streaming)
    chunks = await app.state.rag.retrieve(req.query)
    top_chunks = app.state.rag.rerank(req.query, chunks)
    prompt = app.state.rag.build_prompt(req.query, top_chunks)
    
    async def event_stream():
        # Send sources first
        sources = [{"source": c.source, "score": c.score} for c in top_chunks]
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"
        
        # Stream LLM response
        async with anthropic.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'type': 'token', 'text': text})}\n\n"
        
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## 📚 Resurslar

- **"Advanced RAG Techniques"** — IVAN Ilin (Medium series)
- **LlamaIndex Advanced RAG cookbook**
- **RAGAS docs** — [docs.ragas.io](https://docs.ragas.io/)
- **"RAG vs Fine-tuning"** — Anthropic guide
- **HyDE paper** — Gao et al.
- **Cohere RAG guides** — production patterns

## 🏋️ Mashqlar

### 🟢 Easy
1. Naive RAG: 10 ta hujjatda — chunking → vector DB → query.
2. Citation: javobda `[Source N]` formatida manba ko'rsatish.
3. Chunking strategiyalarini solishtiring: 500 vs 1000 vs 2000 token.

### 🟡 Medium
1. **Multi-query RAG**: query → 3 variant → birlashtirish.
2. **HyDE**: sintetik javob → embed → search.
3. **Reranking**: cross-encoder bilan top 20 → top 5.

### 🔴 Hard
1. **Production RAG service**: FastAPI + Qdrant + Celery (ingestion) + Langfuse (observability).
2. **RAG evaluation**: 100 ta savol-javob test set yarating, RAGAS bilan baholang.
3. **Domain-specific tuning**: o'zbek qonunchilik hujjatlari uchun maxsus RAG (chunking, prompts).

## 🚀 Capstone

`notebooks/month-05/06_rag_pipeline.ipynb`:
- **Loyiha:** O'zbekiston Konstitutsiyasi yoki QHK uchun RAG chatbot
- 100+ ta hujjat ingestion
- Multi-query + HyDE + reranking
- Citation
- Streamlit UI
- RAGAS evaluation

## ✅ Tekshirish ro'yxati

- [ ] RAG arxitekturasini bilaman
- [ ] Chunking strategiyalarini (fixed, semantic) qo'llay olaman
- [ ] Hybrid retrieval (dense + sparse)
- [ ] Reranking (cross-encoder)
- [ ] HyDE va Multi-query
- [ ] Citation va source attribution
- [ ] Streaming RAG
- [ ] RAG evaluation (RAGAS)

[AI Agents](./07-ai-agents.md) ga o'tamiz.
