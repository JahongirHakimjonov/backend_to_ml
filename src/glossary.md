# Glossary (Lug'at)

ML/AI/MLOps sohasidagi muhim terminlarning inglizcha-o'zbekcha lug'ati. Har termin uchun **qisqacha izoh** va **kontekst**.

## A

- **Activation function** (faollik funksiyasi) — neural network'da nonlinearity qo'shadigan funksiya (ReLU, Sigmoid, Tanh).
- **AdamW** — Adam optimizatori + better weight decay; modern default.
- **Agent (AI Agent)** — LLM + tools + memory; goal'ga erishish uchun ketma-ket harakatlar.
- **Anchor box** — object detection'da predefined bounding box shape.
- **ANN (Approximate Nearest Neighbor)** — yaqin vektorlarni tez topish (HNSW, IVF).
- **API (Application Programming Interface)** — dasturlash interfeysi.
- **Async / await** — Python'da concurrent operations.
- **Attention mechanism** — sequence'dagi muhim qismlarga "diqqat" qaratish.
- **AUC (Area Under Curve)** — ROC curve ostidagi maydon (classification metric).
- **AutoGrad** — PyTorch'ning avtomatik gradient hisoblash mexanizmi.

## B

- **Backpropagation** — gradient'larni orqaga tarqatish; neural network o'rgatish algoritmi.
- **Bagging (Bootstrap Aggregating)** — parallel ensemble (Random Forest asosi).
- **Batch** — bir vaqtda model'ga uzatilgan sample'lar to'plami.
- **Batch Normalization (BN)** — activation'larni batch ichida normallashtirish.
- **Bayesian Optimization** — smart hyperparameter qidiruv (Optuna).
- **Bias (matematik)** — model output'iga qo'shiladigan constant.
- **Bias (xulosa)** — algoritmda noto'g'ri prediction'larga moyillik.
- **Boosting** — sequential ensemble (XGBoost, LightGBM).
- **BPE (Byte-Pair Encoding)** — subword tokenization (GPT, Llama'da).
- **Broadcasting** — NumPy/PyTorch'da turli shape'dagi tensor'larga operatsiya.

## C

- **Calibration** — model probability'larini ishonchli qilish.
- **Canary deployment** — yangi versiyani kichik traffic'da sinash.
- **Categorical feature** — diskret qiymatli feature (city, color).
- **Chain-of-Thought (CoT)** — LLM'da step-by-step reasoning prompt.
- **Checkpoint** — model state saqlash (resume training uchun).
- **Classification** — sample'ni diskret class'larga ajratish.
- **Clustering** — o'xshashlarni guruhlash (unsupervised).
- **CNN (Convolutional NN)** — image processing uchun neural network.
- **Cold start** — yangi user/item haqida data yo'q muammosi.
- **Concept drift** — input → output relationship vaqt o'tishi bilan o'zgarishi.
- **Confusion Matrix** — TP, FP, TN, FN ko'rsatadigan jadval.
- **Context window** — LLM bir vaqtda ko'ra oladigan token soni.
- **Cosine similarity** — ikki vektor orasidagi cos burchak.
- **CRD (Custom Resource Definition)** — Kubernetes custom obyekt.
- **Cross-encoder** — sentence pair'lar uchun classifier (reranking'da).
- **Cross-validation (CV)** — model'ni bir necha bo'lakda baholash.
- **CUDA** — NVIDIA GPU'larda parallel computation.

## D

- **DAG (Directed Acyclic Graph)** — Airflow'da workflow ko'rinishi.
- **Data augmentation** — sun'iy ravishda training data kengaytirish.
- **Data drift** — input distribution vaqt o'tishi bilan o'zgarishi.
- **Data leakage** — test/validation data training'ga "sizib o'tishi" (xato).
- **DataFrame** — Pandas'da tabular data strukturasi.
- **DataLoader** — PyTorch'da batch yuklash.
- **Decision Tree** — qoidalar daraxtidan iborat klassik ML algoritmi.
- **Deep Learning (DL)** — chuqur (ko'p qatlamli) neural network'lar.
- **DevOps** — software development + operations integratsiyasi.
- **Diffusion model** — image generation (Stable Diffusion, DALL-E).
- **Dimensionality reduction** — feature'lar sonini kamaytirish (PCA, t-SNE).
- **Docker** — application containerization.
- **Dropout** — overfitting'ni kamaytirish uchun neuron'larni tasodifiy "o'chirish".
- **DVC (Data Version Control)** — Git for data.

## E

- **EDA (Exploratory Data Analysis)** — ma'lumotlarni tahlil qilish bosqichi.
- **Embedding** — diskret obyektni dense vektorga aylantirish.
- **Encoder-Decoder** — translation/summarization arxitekturasi.
- **Ensemble** — bir nechta model birgalikda.
- **Epoch** — butun dataset bo'yicha bir martalik training.
- **Evaluation** — model sifatini o'lchash.
- **Evidently AI** — drift detection va monitoring tool.

## F

- **F1 Score** — precision va recall'ning harmonic mean.
- **FastAPI** — modern Python web framework (Pydantic asosida).
- **Feature** — model input'idagi har bir o'lchov.
- **Feature engineering** — yangi feature'lar yaratish.
- **Feature store** — feature'larni saqlash va serve qilish (Feast).
- **Few-shot learning** — kam misol bilan o'rgatish.
- **Fine-tuning** — pretrained modelni o'z task'ga moslashtirish.
- **Flask** — micro web framework (FastAPI'dan oldingi standard).
- **F-score** — F1 ning umumiy holati (beta parametri bilan).
- **Function calling / Tool use** — LLM'ga tashqi function'larni chaqirishga ruxsat.

## G

- **GAN (Generative Adversarial Network)** — generator + discriminator.
- **Gemini** — Google'ning LLM oilasi.
- **Generative AI** — content yaratuvchi AI (matn, rasm, audio).
- **Gini index** — Decision Tree'da split quality.
- **GitHub Actions** — CI/CD platform.
- **GPT (Generative Pretrained Transformer)** — OpenAI LLM oilasi.
- **GPU (Graphics Processing Unit)** — parallel computation uchun.
- **Gradient** — funksiyaning eng tez o'sish yo'nalishi.
- **Gradient Boosting** — sequential boosting algoritm.
- **Gradient Descent** — loss'ni minimize qilish algoritmi.
- **Grafana** — monitoring dashboard.
- **GridSearch** — hyperparameter exhaustive qidiruv.

## H

- **Hallucination** — LLM'ning ishonchli ko'rinishda noto'g'ri javob berishi.
- **Helm** — Kubernetes package manager.
- **HNSW (Hierarchical Navigable Small Worlds)** — fast ANN algorithm.
- **HPA (Horizontal Pod Autoscaler)** — Kubernetes auto-scaling.
- **HuggingFace** — ML modellar va datasetlar uchun platform.
- **Hybrid search** — vector + keyword (BM25) qidiruv.
- **HyDE (Hypothetical Document Embeddings)** — RAG texnikasi.
- **Hyperparameter** — training'dan oldin belgilangan parametr (lr, batch).

## I

- **Image segmentation** — pixel-level classification.
- **Imbalanced data** — class'lar soni teng emas.
- **Inference** — model bilan prediction qilish.
- **Ingress** — Kubernetes external HTTP routing.
- **Instance segmentation** — har object'ga alohida mask.
- **Instruction tuning** — instructions bilan fine-tuning.
- **IoU (Intersection over Union)** — object detection metric.

## J

- **Jupyter Notebook** — interactive Python environment.

## K

- **Keras** — high-level NN API (TensorFlow'da).
- **K-Fold Cross-validation** — dataset'ni K ta foldga bo'lish.
- **K-Means** — clustering algoritmi.
- **KNN (K-Nearest Neighbors)** — yaqin K ta sample asosida classification.
- **Kubernetes (K8s)** — container orchestration.
- **Kubeflow** — Kubernetes-native ML platform.

## L

- **L1, L2 regularization** — Lasso (L1), Ridge (L2).
- **LangChain** — LLM application framework.
- **LangGraph** — stateful multi-agent workflows.
- **Langfuse** — LLM observability platform.
- **LayerNorm** — Layer normalization (Transformer'larda).
- **Learning rate (lr)** — gradient descent qadam kattaligi.
- **LightGBM** — fast gradient boosting (Microsoft).
- **Linear Regression** — eng oddiy regression algoritmi.
- **LLM (Large Language Model)** — katta til modeli.
- **LlamaIndex** — RAG framework.
- **LoRA (Low-Rank Adaptation)** — efficient fine-tuning.
- **Loss function** — model xatosini o'lchaydigan funksiya.

## M

- **MAE (Mean Absolute Error)** — regression metric.
- **MAP (mean Average Precision)** — object detection metric.
- **MAPE (Mean Absolute Percentage Error)** — % ko'rinishidagi xato.
- **MCP (Model Context Protocol)** — Anthropic'ning agent tool standarti.
- **MinMaxScaler** — feature'larni [0, 1]'ga keltirish.
- **MLflow** — experiment tracking platform.
- **MLOps** — ML + DevOps integratsiyasi.
- **Model registry** — versionlangan modellar saqlash.
- **MSE (Mean Squared Error)** — regression loss.
- **Multi-class classification** — 3+ class'lar orasida tanlash.
- **Multi-label classification** — bir sample'ga bir nechta label.
- **Multi-task learning** — bir model bir nechta task.

## N

- **N-gram** — N ta consecutive so'zlar.
- **Naive Bayes** — probabilistic classifier (text uchun mashhur).
- **NER (Named Entity Recognition)** — matnda nomlangan obyektlar.
- **Neural Network (NN)** — bir-biriga bog'langan neuronlar tarmog'i.
- **NLP (Natural Language Processing)** — matn bilan ishlash.
- **NMS (Non-Maximum Suppression)** — overlapping detection'larni filter.
- **Normalization** — feature'larni bir xil scale'ga keltirish.
- **NumPy** — numerical computation library.

## O

- **One-Hot Encoding** — categorical → binary vektor.
- **ONNX (Open Neural Network Exchange)** — cross-framework model format.
- **OpenAI** — GPT yaratuvchi kompaniya.
- **Optimizer** — gradient'ni qanday qo'llash (SGD, Adam, AdamW).
- **Optuna** — Bayesian hyperparameter tuning.
- **Overfitting** — model train'da yaxshi, test'da yomon.

## P

- **Pandas** — tabular data manipulation.
- **Parameter** — modelda o'rganiladigan qiymat (weight).
- **PCA (Principal Component Analysis)** — dimensionality reduction.
- **PEFT (Parameter-Efficient Fine-Tuning)** — LoRA, QLoRA va h.k.
- **Perceptron** — eng oddiy neuron.
- **Pipeline** — sklearn'da preprocessing + model.
- **Pod** — Kubernetes'da eng kichik unit.
- **Pooling** — CNN'da downsampling (MaxPool, AvgPool).
- **POS tagging (Part-Of-Speech)** — gap bo'laklarini aniqlash.
- **Postgres / PostgreSQL** — relational database.
- **Precision** — TP / (TP + FP).
- **Prefect** — modern workflow orchestrator.
- **Pretrained model** — katta corpus'da oldindan o'rgatilgan model.
- **Prompt** — LLM'ga beriladigan input matn.
- **Prompt engineering** — yaxshi prompt yozish san'ati.
- **Prometheus** — metrics monitoring system.
- **PSI (Population Stability Index)** — drift detection metric.
- **Pydantic** — Python data validation.
- **PyTorch** — deep learning framework.

## Q

- **QLoRA** — 4-bit quantization + LoRA.
- **Qdrant** — vector database (Rust).
- **Quantization** — model precision'ini kamaytirish (8-bit, 4-bit).
- **Query** — LLM/search'ga beriladigan savol.

## R

- **R²** — coefficient of determination (regression).
- **RAG (Retrieval Augmented Generation)** — LLM + knowledge retrieval.
- **RAGAS** — RAG evaluation framework.
- **Random Forest** — bagging Decision Trees.
- **RandomizedSearch** — random hyperparameter qidiruv.
- **Recall** — TP / (TP + FN).
- **Recommender system** — tavsiya sistemasi.
- **ReAct (Reasoning + Acting)** — agent pattern.
- **Recurrent Neural Network (RNN)** — sequence uchun NN.
- **Redis** — in-memory database.
- **Regex (Regular Expression)** — pattern matching.
- **Regression** — uzluksiz qiymat bashorat.
- **Regularization** — overfitting'ni kamaytirish (L1, L2, Dropout).
- **Reranking** — search natijalarini qayta tartibga solish.
- **REST API** — HTTP-based API standard.
- **ResNet** — skip connection'lari bo'lgan CNN.
- **RLHF (Reinforcement Learning from Human Feedback)** — LLM alignment.
- **RMSE (Root Mean Squared Error)** — sqrt(MSE).
- **ROC-AUC** — Receiver Operating Characteristic Area Under Curve.

## S

- **SageMaker** — AWS ML platform.
- **Scaler** — feature normalization (Standard, MinMax).
- **scikit-learn** — Python ML library.
- **Self-attention** — sequence ichidagi token'lar orasidagi attention.
- **Self-supervised learning** — labels'siz pretraining.
- **Semantic search** — meaning-based qidiruv (vector search).
- **Sentence Transformer** — sentence embeddings.
- **SFT (Supervised Fine-Tuning)** — instruction'lar bilan fine-tune.
- **SGD (Stochastic Gradient Descent)** — klassik optimizer.
- **SHAP (SHapley Additive exPlanations)** — model interpretation.
- **Shadow deployment** — yangi modelni traffic'siz sinash.
- **Sigmoid** — activation function (binary class uchun).
- **Softmax** — multi-class output activation.
- **spaCy** — NLP library.
- **Standardization** — (x - mean) / std.
- **Streaming** — real-time response (SSE, WebSocket).
- **Supervised learning** — labels bilan o'rganish.
- **SVM (Support Vector Machine)** — klassik classifier.

## T

- **Tensor** — multi-dimensional array (NumPy ndarray'ning generalizatsiyasi).
- **TensorFlow** — Google'ning DL framework'i.
- **Test set** — yakuniy baholash uchun ajratilgan data.
- **TF-IDF** — text feature representation.
- **Threshold** — classification decision chegarasi.
- **Token** — tokenization'dan keyingi atomic unit.
- **Tokenizer** — matnni token'larga ajratish.
- **TorchServe** — PyTorch production serving.
- **Train set** — model o'rganadigan data.
- **Transfer learning** — pretrained model'ni o'z task'ga qo'llash.
- **Transformer** — attention-based arxitektura (BERT, GPT).
- **Triton** — NVIDIA inference server.

## U

- **Underfitting** — model juda oddiy, train'da ham yomon.
- **Unicode** — character encoding standard.
- **Unsupervised learning** — labels'siz o'rganish.

## V

- **Validation set** — hyperparameter tuning uchun data.
- **Variance** — data tarqoqlik darajasi.
- **Vector** — 1-D array.
- **Vector Database** — embeddings saqlash va search.
- **ViT (Vision Transformer)** — rasm uchun Transformer.
- **vLLM** — fastest LLM inference server.

## W

- **WandB (Weights & Biases)** — experiment tracking.
- **Weight** — neuron coefficient.
- **WebSocket** — bidirectional connection.
- **Word2Vec** — word embedding model.
- **Workflow orchestration** — task'lar ketma-ketligini boshqarish (Airflow).

## X

- **XGBoost** — popular gradient boosting library.
- **XLM-R** — multilingual RoBERTa.

## Y

- **YAML** — config fayl formati.
- **YOLO (You Only Look Once)** — fast object detection.

## Z

- **Zero-shot learning** — pre-existing knowledge bilan misol'siz task.

---

[Asosiy sahifaga qaytish](./introduction.md) yoki [Resurslar](./resources/README.md) ga o'ting.
