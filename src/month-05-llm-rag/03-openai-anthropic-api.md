# OpenAI va Anthropic API

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- OpenAI va Anthropic API'lar bilan ishlashni bilasiz
- Streaming responses, function calling, vision API'larini ishlatasiz
- Prompt caching bilan xarajatlarni 90%'gacha kamaytirishni bilasiz
- Production'ga retry, rate limit, error handling qo'shasiz

## 📖 Nimani o'rganish kerak

- **OpenAI SDK** — Python client
- **Anthropic SDK** — Python client
- **Chat completions** — asosiy API
- **Streaming** — real-time response
- **Function calling / Tool use** — structured actions
- **Vision** — rasm bilan ishlash
- **Embeddings** — semantic search uchun
- **Prompt caching** (Anthropic) — narxni 90% kamaytirish
- **Batching** — async parallel calls
- **Rate limiting** va retry strategiyalari
- **Token tracking va observability**

## 📦 Kutubxonalar

```bash
pip install openai anthropic
pip install instructor              # structured output
pip install tenacity                # retry logic
pip install backoff                 # exponential backoff
```

## 💻 Kod misollari

### OpenAI — basic chat

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")  # yoki os.getenv("OPENAI_API_KEY")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Sen yordamchi assistantsan."},
        {"role": "user", "content": "Salom! Python da list comprehension nima?"},
    ],
    temperature=0.7,
    max_tokens=500,
)

print(response.choices[0].message.content)
print(f"Tokens: in={response.usage.prompt_tokens}, out={response.usage.completion_tokens}")
```

### Anthropic — basic message

```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="Sen yordamchi assistantsan.",
    messages=[
        {"role": "user", "content": "Python da list comprehension nima?"},
    ],
)

print(response.content[0].text)
print(f"Tokens: in={response.usage.input_tokens}, out={response.usage.output_tokens}")
```

### Streaming — real-time

#### OpenAI streaming
```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Uzun hikoya yozing"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### Anthropic streaming
```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Uzun hikoya yozing"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Function Calling / Tool Use

#### OpenAI function calling
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Berilgan shahar uchun ob-havoni qaytaradi",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Shahar nomi"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["city"],
        },
    },
}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Toshkentda ob-havo qanday?"}],
    tools=tools,
)

# Tool call'ni bajarish
tool_call = response.choices[0].message.tool_calls[0]
if tool_call.function.name == "get_weather":
    args = json.loads(tool_call.function.arguments)
    weather = get_weather(args["city"], args.get("unit", "celsius"))
    
    # Natijani qaytarib LLM'ga yuborish
    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Toshkentda ob-havo qanday?"},
            response.choices[0].message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": str(weather)},
        ],
        tools=tools,
    )
    print(response2.choices[0].message.content)
```

#### Anthropic tool use
```python
tools = [{
    "name": "get_weather",
    "description": "Berilgan shahar uchun ob-havoni qaytaradi",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["city"],
    },
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Toshkentda ob-havo qanday?"}],
)

# Tool use'ni bajarish
for block in response.content:
    if block.type == "tool_use":
        if block.name == "get_weather":
            result = get_weather(**block.input)
            # Natijani qaytarib yuborish
            response2 = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {"role": "user", "content": "Toshkentda ob-havo qanday?"},
                    {"role": "assistant", "content": response.content},
                    {"role": "user", "content": [{
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    }]},
                ],
            )
```

### Vision API

#### OpenAI vision
```python
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Bu rasmda nima ko'ryapsiz?"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encode_image('photo.jpg')}"},
            },
        ],
    }],
)
```

#### Anthropic vision
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Bu rasmda nima ko'ryapsiz?"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": encode_image("photo.jpg"),
                },
            },
        ],
    }],
)
```

### Prompt Caching (Anthropic) — 90% arzonroq!

```python
# Katta system prompt cache qilinadi, qayta-qayta to'lanmaydi
LARGE_SYSTEM = open("docs.md").read()  # 50K token docs

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LARGE_SYSTEM,
            "cache_control": {"type": "ephemeral"},  # CACHE!
        },
    ],
    messages=[{"role": "user", "content": "Ma'lumotnoma haqida savol..."}],
)

# Birinchi marta: full price + cache write (1.25x)
# Keyingi 5 daqiqada: 0.1x price (90% cheaper!)
```

### Embeddings

#### OpenAI embeddings
```python
response = client.embeddings.create(
    model="text-embedding-3-small",  # 1536-dim, $0.02 / 1M tokens
    input=["Salom dunyo", "Machine learning"],
)

embeddings = [d.embedding for d in response.data]
# Shape: [(1536,), (1536,)]
```

#### Anthropic embeddings? — yo'q
Anthropic'da o'z embeddings API yo'q. Variantlar:
- OpenAI text-embedding-3-small
- Voyage AI (Anthropic tavsiya etadi)
- Cohere embeddings
- Sentence Transformers (local)

### Retry + Rate Limiting

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import RateLimitError, APIError

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=lambda e: isinstance(e, (RateLimitError, APIError)),
)
async def call_llm_with_retry(messages: list, model: str = "gpt-4o-mini"):
    response = await async_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content
```

### Async batching

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def process_one(text: str):
    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize: {text}"}],
    )
    return response.choices[0].message.content

async def process_batch(texts: list[str], max_concurrent: int = 10):
    sem = asyncio.Semaphore(max_concurrent)
    
    async def bounded(text):
        async with sem:
            return await process_one(text)
    
    return await asyncio.gather(*[bounded(t) for t in texts])

# 100 ta matnni 10 ta concurrent bilan
results = asyncio.run(process_batch(texts, max_concurrent=10))
```

### Cost tracking middleware

```python
import logging
from contextlib import contextmanager

logger = logging.getLogger("llm_costs")

PRICES = {
    "gpt-4o-mini": (0.15, 0.60),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5": (0.80, 4.00),
}

@contextmanager
def track_llm_call(model: str, user_id: int = None):
    """Usage: with track_llm_call("gpt-4o-mini"): ..."""
    response_holder = {}
    
    def hook(response):
        response_holder["response"] = response
    
    yield hook
    
    response = response_holder.get("response")
    if response and hasattr(response, "usage"):
        u = response.usage
        in_price, out_price = PRICES[model]
        cost = (u.prompt_tokens * in_price + u.completion_tokens * out_price) / 1_000_000
        
        logger.info(f"model={model} in={u.prompt_tokens} out={u.completion_tokens} "
                    f"cost=${cost:.6f} user={user_id}")
```

## 🔌 Backend integratsiyasi

### FastAPI'da streaming chat endpoint (SSE)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

app = FastAPI()
client = AsyncOpenAI()

class ChatRequest(BaseModel):
    message: str
    session_id: str

async def stream_chat(messages: list):
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'text': text})}\n\n"
    
    yield "data: [DONE]\n\n"

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    history = await get_history(req.session_id)
    messages = history + [{"role": "user", "content": req.message}]
    
    return StreamingResponse(
        stream_chat(messages),
        media_type="text/event-stream",
    )
```

### WebSocket chat

```python
from fastapi import WebSocket

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            messages = data["messages"]
            
            async with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=messages,
            ) as stream:
                async for text in stream.text_stream:
                    await websocket.send_json({"type": "delta", "text": text})
                
                await websocket.send_json({"type": "done"})
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        await websocket.close()
```

### Multi-provider abstraction

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list, **kwargs) -> str: ...

class OpenAIProvider(LLMProvider):
    def __init__(self, model="gpt-4o-mini"):
        self.client = AsyncOpenAI()
        self.model = model
    
    async def chat(self, messages, **kwargs):
        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, **kwargs)
        return response.choices[0].message.content

class AnthropicProvider(LLMProvider):
    def __init__(self, model="claude-sonnet-4-6"):
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic()
        self.model = model
    
    async def chat(self, messages, **kwargs):
        # System message ni alohida ajratish
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        msgs = [m for m in messages if m["role"] != "system"]
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.pop("max_tokens", 1024),
            system=system,
            messages=msgs,
            **kwargs,
        )
        return response.content[0].text

# Usage
provider = OpenAIProvider("gpt-4o-mini")
# yoki
provider = AnthropicProvider("claude-haiku-4-5")

response = await provider.chat([{"role": "user", "content": "Salom"}])
```

## 📚 Resurslar

- **OpenAI docs** — [platform.openai.com/docs](https://platform.openai.com/docs)
- **Anthropic docs** — [docs.anthropic.com](https://docs.anthropic.com)
- **OpenAI Cookbook** — [cookbook.openai.com](https://cookbook.openai.com/)
- **Anthropic Cookbook** — GitHub
- **LiteLLM** — universal LLM wrapper: [litellm.ai](https://litellm.ai/)
- **OpenRouter** — bitta API ko'p model'lar uchun: [openrouter.ai](https://openrouter.ai/)

## 🏋️ Mashqlar

### 🟢 Easy
1. OpenAI va Anthropic API bilan "Hello World" — 5 ta savol-javob.
2. Streaming response oling, har char'ni alohida chiqaring.
3. Embedding'ni 2 ta gap orasidagi similarity uchun.

### 🟡 Medium
1. **Function calling**: weather, calculator, search — 3 ta tool bilan agent.
2. **Vision**: rasm yuklab, undan structured data ajrating (Instructor + vision).
3. **Prompt caching**: katta system prompt bilan 10 ta savol — narx farqini ko'ring.

### 🔴 Hard
1. **Multi-provider chat**: OpenAI/Anthropic/Google — bitta abstraction, auto-fallback.
2. **Cost-aware router**: input murakkabligi va kontekst kattaligi bo'yicha mos modelni avtomatik tanlash.
3. **Streaming chatbot**: FastAPI + WebSocket + Postgres history + Redis caching.

## 🚀 Capstone

`notebooks/month-05/03_llm_apis.ipynb`:
- 3 ta provider (OpenAI, Anthropic, OpenRouter) bilan to'liq tanish bo'lish
- Multi-turn chatbot streaming bilan
- Function calling — 5 ta tool
- Vision — rasm classification
- Cost tracking dashboard

## ✅ Tekshirish ro'yxati

- [ ] OpenAI va Anthropic API'ni bilaman
- [ ] Streaming responses ishlataman
- [ ] Function calling / tool use
- [ ] Vision API bilan ishlash
- [ ] Embeddings hisoblash va saqlash
- [ ] Prompt caching (Anthropic)
- [ ] Async batching
- [ ] Retry va rate limit handling
- [ ] Cost tracking va observability

[LangChain va LlamaIndex](./04-langchain-llamaindex.md) ga o'tamiz.
