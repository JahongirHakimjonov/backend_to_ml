# LangChain va LlamaIndex

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- LangChain va LlamaIndex frameworks farqini bilasiz
- Document loading, splitting, embedding pipeline qura olasiz
- Chain'lar va agent'lar (LangChain) bilan ishlay olasiz
- Index'lar (LlamaIndex) bilan tez RAG yaratasiz
- Modern alternatives (Pydantic AI, Instructor, raw API) bilan ham tanishasiz

> **Diqqat:**2024-2026 da industry sentiment LangChain'dan **chetlanmoqda**(juda murakkab, ortiqcha abstraction). Modern yondashuv: **raw API + Instructor + minimal framework**. Lekin LangChain hali ko'p loyihalarda ishlatiladi — bilish kerak.

## Nimani o'rganish kerak

- **LangChain**: chains, agents, memory, callbacks
- **LangChain LCEL**(LangChain Expression Language)
- **LlamaIndex**: indexes, retrievers, query engines
- **Document loaders** — PDF, HTML, Notion, GitHub
- **Text splitters** — RecursiveCharacter, Markdown, Code
- **Modern alternatives** — Pydantic AI, Instructor, raw API
- **LangGraph** — multi-agent workflows
- **LangSmith** — observability

## Kutubxonalar

```bash
pip install langchain langchain-openai langchain-anthropic langchain-community
pip install llama-index llama-index-llms-openai
pip install pydantic-ai instructor
pip install unstructured pypdf                # document loading
```

## Framework comparison

| | LangChain | LlamaIndex | Raw API + Instructor |
|---|-----------|-----------|---------------------|
| **Learning curve** | Tik | O'rta | Past |
| **RAG support** | Yaxshi | Excellent | Manual |
| **Agents** | Murakkab | Yaxshi | LangGraph kerak |
| **Production** | Mixed reviews | Yaxshi | Eng yaxshi |
| **Performance** | Slow | OK | Eng tez |
| **Industry trend** | ⬇️ | ⬆️ | ⬆️⬆️ |
| **Code clarity** | Abstract | Better | Eng aniq |

**Tavsiya:**
- Yangi loyiha → **raw API + Instructor + LlamaIndex**(RAG uchun)
- Mavjud LangChain — qoldiring, lekin yangi feature'lar uchun migrate qiling
- Complex agent workflows → **LangGraph**

## Kod misollari

### LangChain — basic chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LCEL syntax (yangi, tavsiya)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yordamchi assistantsan. Til: {language}"),
    ("user", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# Run
result = chain.invoke({"language": "o'zbek", "question": "Python nima?"})
print(result)
```

### LangChain — RAG (simple)

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 3. Embed + store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. Retrieve + answer
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=retriever,
    return_source_documents=True,
)

result = qa_chain.invoke({"query": "Hujjat haqida nima deyilgan?"})
print(result["result"])
```

### LlamaIndex — quickest RAG

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# Settings (global)
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 1. Load (PDF, txt, markdown — har xil)
documents = SimpleDirectoryReader("data/").load_data()

# 2. Index (avtomatik embedding + chunk)
index = VectorStoreIndex.from_documents(documents)

# 3. Query
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("Bu hujjat haqida")
print(response)
print(response.source_nodes)  # qaysi chunklardan olingan
```

### LlamaIndex — Chat engine (multi-turn)

```python
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt="Sen tajribali assistantsan. Faqat berilgan kontekst asosida javob bering.",
)

response = chat_engine.chat("Bu loyiha haqida tushuntiring")
print(response.response)

# Follow-up
response = chat_engine.chat("Asosiy qiyinchiliklar nima?")
```

### Pydantic AI — modern alternative

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class WeatherInfo(BaseModel):
    temperature: float
    condition: str
    humidity: int

weather_agent = Agent(
    model="openai:gpt-4o-mini",
    result_type=WeatherInfo,
    system_prompt="Sen ob-havo agentisan. Berilgan shahar uchun ma'lumotlarni tahmin qiling.",
)

result = weather_agent.run_sync("Toshkentdagi ob-havo")
print(result.data)  # Type-safe WeatherInfo object
```

### Instructor — fully type-safe

```python
import instructor
from openai import OpenAI
from pydantic import BaseModel

client = instructor.from_openai(OpenAI())

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Guaranteed structured output (retries on failure)
person = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=Person,
    messages=[{"role": "user", "content": "Mening ismim Ali, 30 yoshda, developerman"}],
)

print(person)  # Person(name="Ali", age=30, occupation="developer")
```

### LangGraph — multi-agent

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    question: str
    research: str
    answer: str

# Node functions
def researcher(state):
    # Search/research
    return {"research": "Topilgan ma'lumotlar..."}

def writer(state):
    # Generate answer
    return {"answer": f"Javob: {state['research']}"}

def reviewer(state):
    # Review
    if len(state["answer"]) < 50:
        return {"answer": state["answer"], "needs_revision": True}
    return {"answer": state["answer"], "needs_revision": False}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)
workflow.add_node("reviewer", reviewer)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    lambda x: "writer" if x.get("needs_revision") else END,
)

app = workflow.compile()
result = app.invoke({"question": "Python nima?"})
```

### Document loaders — variety

```python
# PDF
from langchain_community.document_loaders import PyPDFLoader
docs = PyPDFLoader("file.pdf").load()

# HTML / Website
from langchain_community.document_loaders import WebBaseLoader
docs = WebBaseLoader("https://example.com").load()

# YouTube transcript
from langchain_community.document_loaders import YoutubeLoader
docs = YoutubeLoader.from_youtube_url("https://...", add_video_info=True).load()

# Notion
from langchain_community.document_loaders import NotionDirectoryLoader
docs = NotionDirectoryLoader("notion_export/").load()

# GitHub
from langchain_community.document_loaders import GitHubIssuesLoader
docs = GitHubIssuesLoader("owner/repo", access_token="...").load()

# CSV/Excel
from langchain_community.document_loaders import CSVLoader
docs = CSVLoader("data.csv").load()
```

### Text splitters

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    CharacterTextSplitter,
)

# Recursive — eng keng tarqalgan (har xil separator'lar bilan)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# Markdown — header bo'yicha
md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
])

# Code — semantic splitting
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
py_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=1000, chunk_overlap=100
)
```

## Backend integratsiyasi

### FastAPI + LlamaIndex RAG service

```python
from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Load persisted index
    storage_context = StorageContext.from_defaults(persist_dir="./index_storage")
    app.state.index = load_index_from_storage(storage_context)
    app.state.query_engine = app.state.index.as_query_engine(similarity_top_k=5)
    yield

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(req: QueryRequest):
    response = await app.state.query_engine.aquery(req.question)
    return {
        "answer": str(response),
        "sources": [
            {"text": node.text[:200], "score": node.score}
            for node in response.source_nodes
        ],
    }
```

### Production architecture

```
User → FastAPI → LlamaIndex (in-memory) → Qdrant (vectors) → LLM API
                       ↓
                   Redis (cache)
                       ↓
                 Postgres (history, logs)
                       ↓
                  Langfuse (observability)
```

## Resurslar

### LangChain
- **docs**: [python.langchain.com](https://python.langchain.com/)
- **LangChain Academy** — bepul kurs
- **LangGraph docs** — multi-agent

### LlamaIndex
- **docs**: [docs.llamaindex.ai](https://docs.llamaindex.ai/)
- **LlamaIndex bootcamp** — bepul

### Modern alternatives
- **Pydantic AI** — [ai.pydantic.dev](https://ai.pydantic.dev/) — type-safe agents
- **Instructor** — [python.useinstructor.com](https://python.useinstructor.com/) — guaranteed JSON
- **Haystack** — [haystack.deepset.ai](https://haystack.deepset.ai/) — production RAG framework

### Observability
- **Langfuse** — [langfuse.com](https://langfuse.com/) (open source)
- **LangSmith** — LangChain'dan
- **Phoenix (Arize)** — open source

## 🏋️ Mashqlar

### 🟢 Easy
1. LangChain LCEL bilan oddiy chain (prompt | llm | parser).
2. LlamaIndex bilan PDF'ni 5 qatorda RAG qiling.
3. Instructor bilan resume → structured Pydantic.

### 🟡 Medium
1. **Multi-source RAG**: PDF + website + YouTube transcript — birlashtirgan index.
2. **Conversational RAG**: chat history bilan multi-turn.
3. **LangGraph workflow**: 3 agentli pipeline (researcher → writer → reviewer).

### 🔴 Hard
1. **Production RAG service**: LlamaIndex + Qdrant + FastAPI + Langfuse. 100+ hujjat, async query, source citations, monitoring.
2. **Framework comparison**: bir xil RAG'ni LangChain, LlamaIndex va raw API'da yozing, vaqt va aniqlik solishtiring.
3. **Migration**: mavjud LangChain kodni Pydantic AI yoki raw API'ga ko'chiring.

## Capstone

`notebooks/month-05/04_langchain_llamaindex.md`:
- O'zbek tilidagi 50+ ta hujjat (PDF, websites)
- LlamaIndex bilan RAG index
- Multi-turn chat engine
- Source citations
- FastAPI + Streamlit UI

## ✅ Tekshirish ro'yxati

- [ ] LangChain LCEL syntax
- [ ] LlamaIndex basic RAG
- [ ] Pydantic AI / Instructor (modern)
- [ ] Document loaders va text splitters
- [ ] Multi-source RAG
- [ ] Chat engine memory
- [ ] LangGraph multi-agent
- [ ] Production observability (Langfuse)

[Vector Databases](./05-vector-databases.md) ga o'tamiz.
