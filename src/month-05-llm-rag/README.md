# Oy 5 — LLM, RAG va AI Agentlar

## 🎯 Bu oydagi maqsad

Oy oxirida siz quyidagilarni qila olasiz:
- LLM (Large Language Model) arxitekturasi va ekosistemasini bilasiz
- OpenAI, Anthropic, Google AI API'lar bilan ishlashni bilasiz
- Prompt engineering texnikalarini qo'llay olasiz
- Vector DB va RAG (Retrieval Augmented Generation) pipeline qura olasiz
- AI Agentlar (tool use, function calling) yarata olasiz
- LoRA/QLoRA bilan fine-tuning qilishni bilasiz
- O'zbek tilidagi hujjatlar uchun chatbot yarata olasiz

## Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | LLM fundamentals + Prompt Engineering + APIs | 10-12 soat |
| **Hafta 2** | LangChain/LlamaIndex + Vector DB | 10-12 soat |
| **Hafta 3** | RAG Pipeline (full implementation) | 10-12 soat |
| **Hafta 4** | AI Agents + Fine-tuning + Capstone | 12-15 soat |

## Boblar tartibi

1. [LLM fundamentals](./01-llm-fundamentals.md) — GPT, Claude, Llama qanday ishlaydi
2. [Prompt Engineering](./02-prompt-engineering.md) — yaxshi prompt yozish
3. [OpenAI va Anthropic API](./03-openai-anthropic-api.md) — amaliy ishlash
4. [LangChain va LlamaIndex](./04-langchain-llamaindex.md) — frameworks
5. [Vector Databases](./05-vector-databases.md) — Qdrant, ChromaDB, pgvector
6. [RAG Pipeline](./06-rag-pipeline.md) — to'liq RAG implementation
7. [AI Agents](./07-ai-agents.md) — tool use, multi-agent
8. [Fine-tuning](./08-fine-tuning.md) — LoRA, QLoRA, PEFT
9. [Mashqlar](./exercises.md)

## Oy oxirida nima qila olasiz?

- LLM API bilan to'liq chatbot yarata olish
- 1000+ ta hujjatdan RAG pipeline qurish
- Multi-agent AI sistemalar (CrewAI, LangGraph)
- O'zbek tilidagi documentation bot
- LoRA bilan kichik domain-specific fine-tuning
- Production'ga olib chiqish: streaming, caching, observability

## Backend Dev uchun maslahat

LLM bilan ishlash — **80% prompt engineering + 20% kod**. Backend dev sifatida sizning kuchli tomonlaringiz:

1. **API integratsiyasi** — REST, streaming, retry logic
2. **Schema design** — structured output (Pydantic + JSON)
3. **Caching va cost optimization** — Redis bilan
4. **Async/concurrent** — async LLM calls
5. **Observability** — har LLM call'ni log'lash

## LLM API budget

Bu oy uchun **$10-30 yetadi**:
- OpenAI: GPT-4o-mini (juda arzon — 1M tokens uchun $0.15)
- Anthropic: Claude Haiku 4.5 (Sonnet 4.6 ham arzon)
- Google: Gemini 2.5 Flash (bepul tier mavjud)
- Groq: bepul (Llama, Mixtral models)
- OpenRouter: ko'p model'lar uchun bitta API

**Tavsiya:**OpenRouter'da $10 yuklang — barcha modellarni sinab ko'rish uchun yetadi.

## Boshlash

[LLM fundamentals](./01-llm-fundamentals.md) bilan boshlang.
