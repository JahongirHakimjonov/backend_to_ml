# Jupyter Notebooks

Har oy uchun mashqlar va capstone loyihalari uchun Jupyter notebook'lar.

## 📁 Struktura

```
notebooks/
├── README.md                    # Bu fayl
├── month-01/                    # Foundations
├── month-02/                    # Klassik ML
├── month-03/                    # Deep Learning
├── month-04/                    # CV + NLP
├── month-05/                    # LLM + RAG
└── month-06/                    # MLOps
```

Dependencies loyiha root'idagi `pyproject.toml` da, **`uv`** package manager bilan boshqariladi.

## 🚀 Boshlash (uv bilan)

### 1. `uv` o'rnatish (agar mavjud bo'lmasa)

```bash
# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# yoki Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# yoki pip orqali (universal)
pip install uv
```

Tekshirish:
```bash
uv --version
```

### 2. Loyiha root'iga o'tish

```bash
cd /Users/jakhangir/MyStuff/PythonJob/my/backend_to_ml
```

### 3. Dependencies o'rnatish

`uv` avtomatik tarzda virtual environment yaratadi va `pyproject.toml`'dan paketlarni o'rnatadi.

```bash
# Faqat core (numpy, pandas, matplotlib, jupyter)
uv sync

# Bitta oy uchun (eng tavsiya etiladigan)
uv sync --group month-01
uv sync --group month-02
uv sync --group month-03
uv sync --group month-04
uv sync --group month-05
uv sync --group month-06

# Bir nechta group birga
uv sync --group month-01 --group month-02

# Hamma narsa (10+ GB disk kerak!)
uv sync --all-groups

# Streamlit / Gradio demo'lar
uv sync --group demo

# Dev tools (ruff, pytest, mypy)
uv sync --group dev
```

### 4. Jupyter Lab ishga tushirish

```bash
# uv venv'da ishga tushirish
uv run jupyter lab

# yoki manual activate
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows
jupyter lab
```

VS Code'da:
1. Python extension + Jupyter extension o'rnating
2. `.ipynb` faylni oching
3. Yuqori o'ng burchakda kernel'ni tanlang: `.venv/bin/python`

## ⚡ uv buyruqlari (cheatsheet)

| Buyruq | Vazifa |
|--------|--------|
| `uv venv` | Virtual env yaratish (alohida) |
| `uv sync` | `pyproject.toml`'dan o'rnatish |
| `uv sync --group month-01` | Bitta group |
| `uv sync --all-groups` | Hammasi |
| `uv add pandas` | Yangi paket qo'shish |
| `uv add --group month-05 openai` | Group'ga qo'shish |
| `uv add --dev pytest` | Dev'ga qo'shish |
| `uv remove pandas` | Olib tashlash |
| `uv lock` | `uv.lock` yangilash |
| `uv lock --upgrade` | Barchasini yangilash |
| `uv run jupyter lab` | Venv'da run |
| `uv run python script.py` | Skript run |
| `uv pip list` | Paketlar ro'yxati |
| `uv tree` | Dependency tree |
| `uv cache clean` | Cache tozalash |
| `uv self update` | uv'ni yangilash |

## 🖥 GPU support (PyTorch)

### NVIDIA CUDA (Linux/Windows)

`pyproject.toml`'da PyTorch CUDA index sozlangan. CUDA bilan o'rnatish uchun:

```bash
# Variant 1: index orqali
uv sync --group month-03 --index pytorch-cu121

# Variant 2: manual
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Tekshirish:
```bash
uv run python -c "import torch; print(torch.cuda.is_available())"
```

### Mac M1/M2/M3 (MPS)

Default `uv sync --group month-03` to'g'ri PyTorch'ni o'rnatadi — qo'shimcha sozlash kerak emas.

Tekshirish:
```bash
uv run python -c "import torch; print(torch.backends.mps.is_available())"
```

### CPU only

```bash
uv sync --group month-03 --index pytorch-cpu
```

## ☁️ Cloud alternatives

Lokal GPU yo'q bo'lsa:

### Google Colab (bepul)

Colab'da `uv` ishlatish uchun cell ichida:

```python
!pip install -q uv
!uv pip install --system numpy pandas torch
# yoki: !uv sync --no-project --group month-03 (loyiha clone qilgandan keyin)
```

Bepul T4 GPU — 12 soat/sessiya.

### Kaggle Notebooks (bepul)

Free P100/T4 GPU — 30 soat/hafta. `pip install uv` qilib, yuqoridagi kabi.

### Lightning AI, Paperspace

Free tier'larga ega.

## 🚀 Tezkor misol — to'liq pipeline

```bash
# 1. Loyihani clone qilish (yoki yangi yaratish)
git clone <your-repo>
cd backend-to-ml

# 2. uv o'rnatish (bir marta)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Birinchi oy bilan boshlash
uv sync --group month-01

# 4. Jupyter Lab
uv run jupyter lab

# 5. Brauzer ochiladi → notebooks/month-01/ ichida ishlay boshlang
```

## 📋 Notebook'lar ro'yxati

### Oy 1 — Foundations
- `00_math_warmup.ipynb`
- `01_numpy_basics.ipynb`
- `02_pandas_practice.ipynb`
- `03_visualization.ipynb`
- `04_eda_titanic.ipynb`
- `capstone_house_prices_eda.ipynb`

### Oy 2 — Klassik ML
- `00_ml_intro.ipynb`
- `01_regression.ipynb`
- `02_classification_models.ipynb`
- `03_clustering.ipynb`
- `04_feature_engineering.ipynb`
- `05_model_evaluation.ipynb`
- `06_kaggle_competition.ipynb`

### Oy 3 — Deep Learning
- `01_neural_network_scratch.ipynb`
- `02_pytorch_mnist.ipynb`
- `03_keras_mnist.ipynb`
- `04_training_techniques.ipynb`
- `05_cnn_image_classification.ipynb`
- `06_rnn_timeseries.ipynb`

### Oy 4 — CV + NLP
- `01_cv_intro.ipynb`
- `02_opencv_pipeline.ipynb`
- `03_yolo_detection.ipynb`
- `04_nlp_basics.ipynb`
- `05_text_preprocessing.ipynb`
- `06_transformers.ipynb`

### Oy 5 — LLM + RAG
- `01_llm_fundamentals.ipynb`
- `02_prompt_engineering.ipynb`
- `03_llm_apis.ipynb`
- `04_langchain_llamaindex.ipynb`
- `05_vector_db.ipynb`
- `06_rag_pipeline.ipynb`
- `07_ai_agents.ipynb`
- `08_finetuning.ipynb`

### Oy 6 — MLOps
- `01_mlops_intro.ipynb`
- `02_mlflow.ipynb`
- `03_dvc.ipynb`
- `04_fastapi_serving.ipynb`
- `05_monitoring.ipynb`

## 💡 Best practices

### Notebook yozish
1. **Markdown bo'limlar** — har section uchun
2. **Cell'lar atomic** — bitta cell bitta vazifa
3. **Random seed** — `np.random.seed(42)` reproducibility uchun
4. **Imports yuqorida** — qayta-qayta yozmang
5. **Function'lar** — modular kod
6. **Output'larni clear** — git commit'dan oldin

### Git va notebooks
```bash
# nbstripout — output'larni clear qiladi
uv sync --group dev   # nbstripout dev group'da
uv run nbstripout --install

# .gitignore allaqachon ipynb_checkpoints'ni e'tiborsiz qoldiradi
```

### Performance maslahatlar
- GPU'da ishlash — ko'p marotaba tez
- `tqdm.notebook` — progress bar
- `%%time` — cell timing
- `%load_ext autoreload` + `%autoreload 2` — module'larni auto-reload
- `uv` o'zi juda tez (pip'dan 10-100x) — qayta o'rnatishdan qo'rqmang

## 🔧 Troubleshooting

### Kernel topilmadi
```bash
uv run python -m ipykernel install --user --name=ml-roadmap --display-name="ML Roadmap"
```

### Out of memory (GPU)
- `batch_size` ni kichraytiring
- Mixed precision (`torch.cuda.amp`)
- `torch.cuda.empty_cache()`
- Colab'da: Runtime → Restart

### `uv sync` xato
```bash
# Cache'ni tozalash
uv cache clean

# Lock'ni qayta yaratish
rm uv.lock
uv lock
uv sync --group month-XX
```

### Conflicting dependencies (masalan, tensorflow + torch ikkalasini)
PyTorch va TF ikkalasini birga ishlatish memory'ga og'irlik beradi. `pyproject.toml`'da `tf-extras` alohida group'da — kerak bo'lsa qo'shing:

```bash
uv sync --group month-03 --group tf-extras
```

## 📚 uv haqida ko'proq

- **Docs:** [docs.astral.sh/uv](https://docs.astral.sh/uv/)
- **GitHub:** [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- **Migration from pip:** [docs.astral.sh/uv/pip](https://docs.astral.sh/uv/pip/)
- **PEP 735 dependency groups:** [peps.python.org/pep-0735](https://peps.python.org/pep-0735/)

[Asosiy kitobga qaytish](../src/SUMMARY.md)
