# Vector Databases

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Vector database (vector DB) nima va nima uchun kerakligini bilasiz
- Qdrant, ChromaDB, pgvector, Pinecone, Weaviate farqlarini bilasiz
- Production'da vector DB tanlash mezonlarini bilasiz
- Hybrid search (vector + keyword) qura olasiz
- Million-scale vector indexlarni boshqara olasiz

## Nimani o'rganish kerak

- **Vector embeddings** — eslab qoling, Oy 4'dan
- **Similarity metrics** — cosine, dot product, Euclidean
- **ANN (Approximate Nearest Neighbor)**algoritmlari — HNSW, IVF
- **Vector DB'lar** — Qdrant, ChromaDB, pgvector, Pinecone, Weaviate, Milvus
- **Hybrid search** — vector + BM25 (keyword)
- **Reranking** — Cross-encoder bilan top-k natijani qayta tartibga solish
- **Metadata filtering**
- **Sharding va indexing** — million-scale

## Vector DB nima va nima uchun kerak?

### Muammo
Klassik SQL'da: "name = 'John'" — aniq match.
Lekin: "Python developer kerak" → "Python dasturchi izlanmoqda" — semantically bir xil, lekin string'da farqli.

### Yechim
Matnni vector (embedding) ga aylantirib, **cosine similarity**asosida qidirish.

```
"Python developer" → [0.12, 0.45, ..., -0.23]  (1536-dim)
"Python dasturchi" → [0.14, 0.47, ..., -0.21]
cosine_similarity > 0.95 — juda yaqin!
```

### Vector DB nima qiladi?
1. **Index** — millionlab vektorlarni samarali saqlash
2. **Search** — query vektoriga eng yaqin K ta vektorni topish (ms ichida)
3. **Metadata** — har vector bilan birga JSON saqlash
4. **Filtering** — `metadata.category = "tech"` shartda qidirish

### ANN (Approximate NN) — nima uchun "approximate"?

Million vektorlar orasidan eng yaqinini topish — O(N) operatsiya, sekin.
**HNSW**(Hierarchical Navigable Small Worlds) — O(log N) — milliard scale'da.

Trade-off: 99% accuracy lekin 1000x tezroq.

## Asosiy Vector DB'lar

### Comparison table

| | **Qdrant** | **ChromaDB** | **pgvector** | **Pinecone** | **Weaviate** | **Milvus** |
|---|------------|--------------|--------------|--------------|--------------|------------|
| **Type** | Standalone | Standalone | Postgres ext | SaaS | Standalone | Standalone |
| **Open source** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Self-host** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Cloud option** | ✅ | ✅ | ✅ (Supabase) | ✅ | ✅ | ✅ (Zilliz) |
| **Rust/Go** | Rust | Python | C | - | Go | Go/C++ |
| **Scale** | Billions | Millions | Millions | Billions | Billions | Billions |
| **Hybrid search** | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Metadata filter** | ✅✅ | ✅ | ✅✅ | ✅ | ✅ | ✅ |
| **Ease of use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Production** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost** | Free/self | Free | Free | $$$ | Free/self | Free/self |

### Tavsiyalar

- **Boshlanish (prototype):**ChromaDB (Python ichida, no setup)
- **Backend dev (Postgres allaqachon bor):**pgvector
- **Production (self-hosted):****Qdrant**(eng yaxshi sifat/oson o'rnatish)
- **Production (managed):**Pinecone
- **Enterprise (millions+):**Milvus, Weaviate

## Kod misollari

### ChromaDB — eng oson boshlash

```python
import chromadb

client = chromadb.Client()
# yoki persistent:
# client = chromadb.PersistentClient(path="./chroma_db")

collection = client.create_collection("docs")

# Add documents
collection.add(
    documents=["Python — yuqori darajadagi til", "JavaScript — web tilida"],
    metadatas=[{"category": "language"}, {"category": "language"}],
    ids=["doc1", "doc2"],
)
# ChromaDB avtomatik embed qiladi (default: all-MiniLM-L6-v2)

# Query
results = collection.query(
    query_texts=["Python dasturlash"],
    n_results=5,
    where={"category": "language"},
)
print(results)
```

### ChromaDB with custom embeddings

```python
from chromadb.utils import embedding_functions

# OpenAI embeddings
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="...",
    model_name="text-embedding-3-small",
)

collection = client.create_collection(
    name="docs",
    embedding_function=openai_ef,
)
```

### Qdrant — production grade

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Local Docker:
# docker run -p 6333:6333 qdrant/qdrant
client = QdrantClient(url="http://localhost:6333")

# 1. Create collection
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# 2. Add points
from openai import OpenAI
openai_client = OpenAI()

texts = ["Python is a programming language", "JavaScript is for web"]
embeddings = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)

points = [
    PointStruct(
        id=i,
        vector=emb.embedding,
        payload={"text": text, "category": "language"},
    )
    for i, (text, emb) in enumerate(zip(texts, embeddings.data))
]

client.upsert(collection_name="docs", points=points)

# 3. Search
query_emb = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=["Python dasturlash"],
).data[0].embedding

results = client.search(
    collection_name="docs",
    query_vector=query_emb,
    limit=5,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="language"))]
    ),
)

for r in results:
    print(f"Score: {r.score:.4f}, Text: {r.payload['text']}")
```

### pgvector — Postgres extension

```sql
-- Install (one time)
CREATE EXTENSION vector;

-- Create table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or IVFFlat
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

```python
import psycopg
from psycopg.rows import dict_row

conn = psycopg.connect("dbname=mydb", row_factory=dict_row)

# Insert
embedding = openai.embeddings.create(input="text", model="text-embedding-3-small").data[0].embedding
conn.execute(
    "INSERT INTO documents (content, embedding, metadata) VALUES (%s, %s, %s)",
    ("Python is great", embedding, '{"category": "language"}'),
)

# Search (cosine distance)
query_emb = openai.embeddings.create(input="Python dasturlash", model="text-embedding-3-small").data[0].embedding

results = conn.execute("""
    SELECT id, content, metadata,
           1 - (embedding <=> %s::vector) AS similarity
    FROM documents
    WHERE metadata->>'category' = %s
    ORDER BY embedding <=> %s::vector
    LIMIT 5
""", (query_emb, "language", query_emb)).fetchall()

# Distance operators:
# <-> Euclidean (L2)
# <#> Negative dot product
# <=> Cosine distance
```

### Hybrid search (Qdrant)

```python
from qdrant_client.models import SparseVectorParams, SparseVector

# Hybrid: vector (dense) + BM25 (sparse)
client.create_collection(
    collection_name="docs_hybrid",
    vectors_config={
        "dense": VectorParams(size=1536, distance=Distance.COSINE),
    },
    sparse_vectors_config={
        "bm25": SparseVectorParams(),
    },
)

# Search with reciprocal rank fusion
from qdrant_client.models import Prefetch, Fusion, FusionQuery

results = client.query_points(
    collection_name="docs_hybrid",
    prefetch=[
        Prefetch(query=dense_query, using="dense", limit=20),
        Prefetch(query=sparse_query, using="bm25", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=10,
)
```

### Reranking — sifatni oshirish

```python
from sentence_transformers import CrossEncoder

# Cross-encoder yuqoriroq aniqlik beradi (lekin sekinroq)
reranker = CrossEncoder("BAAI/bge-reranker-base")

# 1. Vector search bilan top 50 ta olish
candidates = client.search(collection_name="docs", query_vector=q, limit=50)

# 2. Cross-encoder bilan rerank
pairs = [(query_text, c.payload["text"]) for c in candidates]
scores = reranker.predict(pairs)

# 3. Top 5 ta
reranked = sorted(zip(scores, candidates), key=lambda x: -x[0])[:5]
```

## Backend integratsiyasi

### RAG ingestion pipeline

```python
from fastapi import FastAPI, UploadFile
from celery import Celery

celery_app = Celery("rag", broker="redis://localhost:6379")

@celery_app.task
def ingest_document(file_path: str, source_url: str = None):
    # 1. Load
    from langchain_community.document_loaders import PyPDFLoader
    docs = PyPDFLoader(file_path).load()
    
    # 2. Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    # 3. Embed
    openai_client = OpenAI()
    embeddings = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=[c.page_content for c in chunks],
    )
    
    # 4. Store in Qdrant
    points = [
        PointStruct(
            id=uuid.uuid4().hex,
            vector=emb.embedding,
            payload={
                "text": chunk.page_content,
                "page": chunk.metadata.get("page", 0),
                "source": source_url or file_path,
            },
        )
        for chunk, emb in zip(chunks, embeddings.data)
    ]
    qdrant.upsert(collection_name="docs", points=points)
    
    return {"chunks_added": len(points)}

@app.post("/ingest")
async def ingest(file: UploadFile, source_url: str = None):
    path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    
    task = ingest_document.delay(path, source_url)
    return {"task_id": task.id}
```

### Search endpoint

```python
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: dict = {}

@app.post("/search")
async def search(req: SearchRequest):
    # 1. Embed query
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=[req.query],
    ).data[0].embedding
    
    # 2. Vector search
    results = qdrant.search(
        collection_name="docs",
        query_vector=emb,
        limit=req.top_k * 4,  # over-fetch for reranking
        query_filter=build_filter(req.filters) if req.filters else None,
    )
    
    # 3. Rerank
    if len(results) > req.top_k:
        pairs = [(req.query, r.payload["text"]) for r in results]
        scores = reranker.predict(pairs)
        reranked = sorted(zip(scores, results), key=lambda x: -x[0])[:req.top_k]
        results = [r for _, r in reranked]
    
    return {
        "results": [
            {
                "text": r.payload["text"],
                "score": r.score,
                "source": r.payload.get("source"),
                "page": r.payload.get("page"),
            }
            for r in results
        ]
    }
```

## Resurslar

- **Qdrant docs** — [qdrant.tech](https://qdrant.tech/)
- **pgvector GitHub** — [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
- **ChromaDB docs** — [docs.trychroma.com](https://docs.trychroma.com/)
- **Pinecone Learning Center** — [pinecone.io/learn](https://www.pinecone.io/learn/)
- **HNSW paper** — Yu. Malkov, D. Yashunin
- **"Vector Databases: A First Principles Approach"** — Roie Schwaber-Cohen

## 🏋️ Mashqlar

### 🟢 Easy
1. ChromaDB'da 100 ta hujjatni saqlang va semantic search qiling.
2. Qdrant Docker'da ishga tushiring, oddiy collection yarating.
3. pgvector'ni Postgres'da o'rnatib, 50 ta vektor qo'shing.

### 🟡 Medium
1. **Hybrid search**: Qdrant'da dense + BM25 hybrid index.
2. **Reranking**: vector search → cross-encoder rerank — accuracy farqini ko'ring.
3. **Metadata filtering**: 1000+ hujjat, har xil kategoriyada — filter bilan search.

### 🔴 Hard
1. **Production RAG ingestion**: PDF/URL/Notion'dan FastAPI + Celery + Qdrant pipeline.
2. **Multi-tenant vector DB**: har user uchun alohida namespace/collection.
3. **Million-scale benchmark**: 1M ta hujjatni Qdrant va pgvector'da — query latency va recall solishtirish.

## Capstone

`notebooks/month-05/05_vector_db.ipynb`:
- O'zbek tilidagi 1000+ ta hujjat (Wikipedia, daryo.uz, kun.uz)
- Qdrant'da to'liq RAG index
- Hybrid search + reranking
- Multi-source ingestion pipeline

## ✅ Tekshirish ro'yxati

- [ ] Vector DB nima va nima uchun kerakligini bilaman
- [ ] Cosine similarity va Euclidean farqi
- [ ] HNSW algoritmining intuition
- [ ] ChromaDB, Qdrant, pgvector'dan kamida 2 tasini sinab ko'rdim
- [ ] Hybrid search nima
- [ ] Reranking pattern
- [ ] Metadata filtering
- [ ] FastAPI'da RAG ingestion pipeline

[RAG Pipeline](./06-rag-pipeline.md) ga o'tamiz.
