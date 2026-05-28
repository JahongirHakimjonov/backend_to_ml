# Fine-tuning (LoRA, QLoRA, PEFT)

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Fine-tuning va RAG farqini va qachon qaysi birini tanlashni bilasiz
- LoRA, QLoRA, PEFT (Parameter-Efficient Fine-Tuning) bilan ishlay olasiz
- HuggingFace SFTTrainer bilan kichik LLM'larni fine-tune qila olasiz
- OpenAI/Anthropic fine-tuning API'larini ishlatasiz
- Custom dataset tayyorlashni va sintetik data generation'ni bilasiz

## 📖 Nimani o'rganish kerak

- **Full fine-tuning vs LoRA vs QLoRA vs Prompt tuning**
- **PEFT library** — HuggingFace
- **LoRA** — Low-Rank Adaptation, mathematical intuition
- **QLoRA** — 4-bit quantization + LoRA
- **Datasets** — formatlar (chat, instruction, completion)
- **SFTTrainer** — HuggingFace
- **Unsloth** — 2-5x tezroq fine-tuning
- **Evaluation** — perplexity, ROUGE, custom benchmarks
- **Cloud platforms** — RunPod, Lambda Labs, Vast.ai
- **OpenAI / Anthropic fine-tuning APIs**

## 📦 Kutubxonalar

```bash
pip install transformers peft trl bitsandbytes accelerate datasets
pip install unsloth  # 2-5x tezroq
```

## 🧠 RAG vs Fine-tuning — qachon qaysi?

| Use case | RAG | Fine-tuning |
|----------|-----|-------------|
| **Yangi knowledge qo'shish** | ✅ | ❌ |
| **Style/tone o'rgatish** | ❌ | ✅ |
| **Citation kerak** | ✅ | ❌ |
| **Format consistency** | O'rta | ✅ |
| **Latency optimization** | ❌ | ✅ (kichik model) |
| **Domain-specific terms** | ✅ | ✅ (yaxshiroq) |
| **Cost** | Per-query | One-time + cheaper inference |

**Qoida:** Avval RAG, agar yetishmasa — fine-tuning. Ko'p hollarda **RAG yetadi**.

## 🧠 Fine-tuning turlari

### 1. Full Fine-tuning
- Modelning **barcha parametrlari** yangilanadi
- Memory: 7B model uchun ~40GB GPU
- Tezligi: sekin (kunlar/haftalar)
- Sifat: eng yaxshi (lekin overfitting xavfi)

### 2. LoRA (Low-Rank Adaptation)
- Faqat **kichik adapter matrices**ni o'rgatadi (≤1% parameters)
- Memory: 7B model uchun ~14GB GPU
- Tezligi: tez (soatlar)
- Sifat: full fine-tuning'ga juda yaqin (95-99%)

```
Original matrix W (d × k)
↓
W ← W + ΔW
ΔW = A × B
A: d × r   (r << d)
B: r × k

Faqat A va B o'rganiladi. r=8, 16, 32, 64 odatda
```

### 3. QLoRA (Quantized LoRA)
- LoRA + 4-bit quantization
- Memory: 7B model uchun ~6GB GPU (consumer GPU!)
- Sifat: LoRA'ga teng
- **Eng tavsiya etiladigan usul**

### 4. Prompt Tuning / P-Tuning
- Faqat soft prompt embeddings o'rganiladi
- Eng kichik (<<1% params)
- Sifat: o'rta

### 5. Adapter Tuning
- Adapter layer'lar qo'shiladi
- LoRA'dan oldingi yondashuv

## 💻 Kod misollari

### Dataset tayyorlash — Instruction format

```python
# Format: instruction-following
data = [
    {
        "instruction": "Quyidagi matnni sentiment bo'yicha klassify qiling",
        "input": "Bu mahsulot ajoyib!",
        "output": "positive",
    },
    {
        "instruction": "Bu kodda xatoni toping",
        "input": "def foo(): print('hi'",
        "output": "Missing closing parenthesis on print() call",
    },
    # ... 1000+ misol
]

# Chat format (modern)
chat_data = [
    {
        "messages": [
            {"role": "system", "content": "Sen yordamchi assistantsan."},
            {"role": "user", "content": "Python da list nima?"},
            {"role": "assistant", "content": "Python da list — bu ..."},
        ],
    },
    # ...
]
```

### LoRA bilan fine-tuning — HuggingFace

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
from datasets import load_dataset

# 1. Base model
model_name = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# 2. LoRA config
lora_config = LoraConfig(
    r=16,                          # rank
    lora_alpha=32,                 # scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 4M (0.4% of 1B) — juda kam!

# 3. Dataset
dataset = load_dataset("json", data_files="my_data.jsonl")

def format_prompt(example):
    return {
        "text": f"### Instruction: {example['instruction']}\n"
                f"### Input: {example['input']}\n"
                f"### Response: {example['output']}"
    }

dataset = dataset.map(format_prompt)

# 4. Training
training_args = TrainingArguments(
    output_dir="./llama-lora",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    dataset_text_field="text",
    max_seq_length=512,
    tokenizer=tokenizer,
)

trainer.train()

# 5. Save (faqat adapter weights)
model.save_pretrained("./llama-lora-adapter")
```

### QLoRA — eng samarali

```python
from transformers import BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)

# Prepare for training
from peft import prepare_model_for_kbit_training
model = prepare_model_for_kbit_training(model)

# LoRA config (same as before)
model = get_peft_model(model, lora_config)

# Rest is same as LoRA
```

### Unsloth — 2-5x tezroq

```python
from unsloth import FastLanguageModel

# Auto: 4-bit quantization + LoRA + optimizations
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-8b-bnb-4bit",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
)

# Training (same TRL API)
trainer = SFTTrainer(model=model, ...)
trainer.train()

# Inference
FastLanguageModel.for_inference(model)
```

### Inference bilan LoRA adapter

```python
from peft import PeftModel

# Base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./llama-lora-adapter")

# Generate
inputs = tokenizer("### Instruction: Hello\n### Response:", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))
```

### Sintetik data generation (LLM bilan dataset yaratish)

```python
from openai import AsyncOpenAI

async def generate_training_pair(topic: str) -> dict:
    """LLM yordamida (instruction, response) pair yaratish."""
    
    prompt = f"""Yaratish: Python o'qitish uchun 1 ta (savol, javob) pair.

Mavzu: {topic}

JSON format:
{{
  "instruction": "...",
  "response": "..."
}}
"""
    
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)

# 1000 ta sintetik misol generatsiya
import asyncio

topics = ["list comprehension", "decorators", "async/await", ...] * 50
tasks = [generate_training_pair(t) for t in topics]
dataset = await asyncio.gather(*tasks)

# Save
with open("synthetic_data.jsonl", "w") as f:
    for item in dataset:
        f.write(json.dumps(item) + "\n")
```

### OpenAI Fine-tuning API

```python
from openai import OpenAI
client = OpenAI()

# 1. Upload file
file = client.files.create(
    file=open("data.jsonl", "rb"),
    purpose="fine-tune",
)

# 2. Start fine-tuning
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 0.1,
    },
)

# 3. Monitor
job = client.fine_tuning.jobs.retrieve(job.id)
print(job.status)  # running → succeeded

# 4. Use fine-tuned model
response = client.chat.completions.create(
    model=f"ft:gpt-4o-mini-2024-07-18:my-org::{job.fine_tuned_model}",
    messages=[{"role": "user", "content": "Test"}],
)
```

## 🔌 Backend integratsiyasi

### Fine-tuned model serving (vLLM)

```bash
# vLLM — eng tez LLM inference server
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.2-1B-Instruct \
    --enable-lora \
    --lora-modules my-adapter=./llama-lora-adapter \
    --port 8000
```

```python
# OpenAI-compatible API
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy",
)

response = client.chat.completions.create(
    model="my-adapter",
    messages=[{"role": "user", "content": "Hello"}],
)
```

### Training as a service (Celery + FastAPI)

```python
@celery_app.task(bind=True)
def fine_tune_task(self, dataset_path: str, base_model: str, config: dict):
    # 1. Load dataset
    dataset = load_dataset("json", data_files=dataset_path)
    
    # 2. Setup model (QLoRA)
    model = setup_model_with_qlora(base_model)
    
    # 3. Training with progress updates
    trainer = SFTTrainer(...)
    
    class ProgressCallback(TrainerCallback):
        def on_log(self, args, state, control, logs=None, **kwargs):
            if logs:
                self.update_state(
                    state="PROGRESS",
                    meta={"step": state.global_step, "loss": logs.get("loss")}
                )
    
    trainer.add_callback(ProgressCallback())
    trainer.train()
    
    # 4. Save adapter
    output_path = f"models/{self.request.id}"
    model.save_pretrained(output_path)
    
    return {"model_path": output_path}

@app.post("/finetune")
async def start_finetuning(dataset_url: str, base_model: str = "llama-3.2-1b"):
    # Download dataset
    path = await download_dataset(dataset_url)
    
    # Queue task
    task = fine_tune_task.delay(path, base_model, {})
    return {"task_id": task.id}
```

## 📚 Resurslar

- **HuggingFace PEFT docs** — [huggingface.co/docs/peft](https://huggingface.co/docs/peft/)
- **TRL docs** — [huggingface.co/docs/trl](https://huggingface.co/docs/trl/)
- **Unsloth GitHub** — [github.com/unslothai/unsloth](https://github.com/unslothai/unsloth)
- **"QLoRA: Efficient Finetuning"** — paper (Dettmers et al., 2023)
- **"The Novice's LLM Training Guide"** — Alpin Dale
- **OpenAI fine-tuning docs** — [platform.openai.com/docs/guides/fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)
- **Maxime Labonne — LLM Course** ([github.com/mlabonne/llm-course](https://github.com/mlabonne/llm-course))

## 🏋️ Mashqlar

### 🟢 Easy
1. Pretrained Llama 3.2 1B'ni Colab GPU'da yuklang.
2. 50 ta sintetik instruction pair (GPT-4o-mini bilan) yarating.
3. LoRA config sintaksisini o'qing va parametrlarni tushuntiring.

### 🟡 Medium
1. **TinyLlama fine-tuning**: 100 ta misol, QLoRA, Colab T4 GPU.
2. **OpenAI fine-tuning**: GPT-4o-mini'ni custom dataset bilan (cost: ~$1).
3. **Unsloth speedrun**: Mistral-7B'ni 1 soatda fine-tune (Kaggle GPU).

### 🔴 Hard
1. **O'zbek tilda Llama**: 1000+ ta o'zbek instruction pair, Llama 3.1 8B QLoRA — natijani baseline'da solishtirish.
2. **DPO (Direct Preference Optimization)**: SFT'dan keyin preferences bilan tuning.
3. **Production training pipeline**: dataset versioning + training + evaluation + deployment.

## 🚀 Capstone

`notebooks/month-05/08_finetuning.ipynb`:
- **Loyiha:** O'zbek tilidagi customer support bot
- 200+ ta (savol, javob) pairs
- Llama 3.2 1B yoki TinyLlama
- QLoRA + Colab/Kaggle GPU
- Inference deploy (FastAPI + vLLM)
- Baseline vs fine-tuned solishtirish

## ✅ Tekshirish ro'yxati

- [ ] RAG vs Fine-tuning qachon qaysi
- [ ] LoRA matematik intuition
- [ ] QLoRA — eng tavsiya etiladigan usul
- [ ] PEFT library bilan ishlash
- [ ] Instruction dataset format
- [ ] SFTTrainer bilan training
- [ ] Adapter weights save/load
- [ ] vLLM bilan serving
- [ ] OpenAI fine-tuning API

🎉 **Oy 5 tugadi!** [Mashqlar](./exercises.md) ni ko'rib chiqing va [Oy 6 — MLOps va Production](../month-06-mlops-production/README.md) ga o'ting — oxirgi va eng muhim oy.
