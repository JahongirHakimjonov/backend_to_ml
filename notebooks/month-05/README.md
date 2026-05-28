# Month 05 — LLM + RAG Notebooks

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `01_llm_fundamentals.ipynb` | Tokens, models | [LLM](../../src/month-05-llm-rag/01-llm-fundamentals.md) |
| `02_prompt_engineering.ipynb` | Prompts | [Prompts](../../src/month-05-llm-rag/02-prompt-engineering.md) |
| `03_llm_apis.ipynb` | OpenAI, Anthropic | [APIs](../../src/month-05-llm-rag/03-openai-anthropic-api.md) |
| `04_langchain_llamaindex.ipynb` | Frameworks | [LangChain](../../src/month-05-llm-rag/04-langchain-llamaindex.md) |
| `05_vector_db.ipynb` | Qdrant, ChromaDB | [Vector DB](../../src/month-05-llm-rag/05-vector-databases.md) |
| `06_rag_pipeline.ipynb` | Full RAG | [RAG](../../src/month-05-llm-rag/06-rag-pipeline.md) |
| `07_ai_agents.ipynb` | Agents | [Agents](../../src/month-05-llm-rag/07-ai-agents.md) |
| `08_finetuning.ipynb` | LoRA, QLoRA | [Fine-tuning](../../src/month-05-llm-rag/08-fine-tuning.md) |

## 🛠 Dependencies

```bash
# Asosiy LLM/RAG stack
uv sync --group month-05

# GPU bilan fine-tuning (Linux/Windows + NVIDIA)
uv sync --group month-05 --group finetune-gpu

uv run jupyter lab
```

Tarkibida: openai, anthropic, google-generativeai, groq, instructor, pydantic-ai, litellm, langchain, langgraph, llama-index, chromadb, qdrant-client, peft, trl, ragas va h.k.

### 🔑 API keylar

`.env` faylda saqlang (loyiha root'ida):

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

Notebook'da:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 💰 API budget

- **OpenAI** — $5-10 yetadi (GPT-4o-mini juda arzon)
- **Anthropic** — $5-10 (Claude Haiku/Sonnet)
- **OpenRouter** — bitta accountda barchasi
- **Groq** — bepul tier (Llama, Mixtral)

## 📚 Datasets

- O'zbek Wikipedia dump
- lex.uz hujjatlari
- Custom PDF documents

[Asosiy bob](../../src/month-05-llm-rag/README.md).
