# TensorFlow va Keras

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- TensorFlow va Keras'ning PyTorch'dan farqini bilasiz
- Keras Sequential va Functional API bilan model qurasiz
- TensorFlow ekosistemasini (TF Serving, TF Lite, TF.js) bilasiz
- O'z asosiy framework'ingizni ongli ravishda tanlaysiz

> **Eslatma:** Sizning asosiy framework'ingiz **PyTorch** bo'ladi (industry default). TF/Keras ni **shunchaki tanish bo'lish** uchun o'rganamiz, chunki:
> - Eski loyihalarda hali ham bor
> - Google Cloud (Vertex AI) integratsiyasi
> - TF Lite — mobile/edge deployment

## 📖 Nimani o'rganish kerak

- **TensorFlow 2.x** — eager execution, `tf.function`
- **Keras Sequential API** — qatlam ketma-ket qo'shish
- **Keras Functional API** — murakkab arxitekturalar
- **Model.compile, fit, predict** — high-level API
- **Callbacks** — EarlyStopping, ModelCheckpoint, TensorBoard
- **tf.data.Dataset** — efficient data pipeline
- **TF Serving** — production deployment
- **TF Lite** — mobile/edge inference
- **TF.js** — browser'da inference

## 📦 Kutubxonalar

```bash
pip install tensorflow
# yoki
pip install tensorflow-macos tensorflow-metal  # Mac M-chip uchun
```

Versiya: **TensorFlow 2.15+** (2.x faqat).

## 🧠 PyTorch vs TensorFlow/Keras

| Aspect | PyTorch | TF/Keras |
|--------|---------|----------|
| **API style** | Pythonic, imperative | Declarative (Keras), imperative (TF 2) |
| **Boilerplate** | Ko'proq (training loop) | Kam (`.fit()`) |
| **Debugging** | Oddiy (Python) | Ba'zan qiyin (graph mode'da) |
| **Research** | Dominant | Kamayib bormoqda |
| **Production** | Kuchayib bormoqda | Tarixiy ustun |
| **Mobile** | PyTorch Mobile | TF Lite (yaxshiroq) |
| **Browser** | ONNX.js | TF.js (yaxshi) |
| **Industry adoption** | ⬆️ (LLM era) | ⬇️ (Google'dan tashqari) |

**Maslahat:** PyTorch'ni asosiy bilim sifatida o'rganing, TF/Keras'ni esa "tanish bo'lish darajasi"da.

## 💻 Kod misollari

### Sequential API — eng oddiy

```python
import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Input(shape=(784,)),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()
```

### Training (fit API)

```python
from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1,
)

# Evaluation
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.4f}")
```

### Functional API — murakkabroq

```python
inputs = layers.Input(shape=(784,))
x = layers.Dense(256, activation="relu")(inputs)
x = layers.Dropout(0.3)(x)

# Branching (Functional API ning afzalligi)
branch_a = layers.Dense(64, activation="relu")(x)
branch_b = layers.Dense(64, activation="relu")(x)
merged = layers.Concatenate()([branch_a, branch_b])

outputs = layers.Dense(10, activation="softmax")(merged)
model = models.Model(inputs=inputs, outputs=outputs)
```

### Callbacks

```python
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

callbacks = [
    EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
    ModelCheckpoint("best_model.keras", monitor="val_accuracy", save_best_only=True),
    TensorBoard(log_dir="./logs"),
]

model.fit(X_train, y_train, epochs=50, callbacks=callbacks, validation_split=0.1)
# TensorBoard: $ tensorboard --logdir=./logs
```

### Custom training loop (PyTorch-like)

```python
optimizer = tf.keras.optimizers.Adam()
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()
acc_metric = tf.keras.metrics.SparseCategoricalAccuracy()

@tf.function  # graph mode (tezroq)
def train_step(X, y):
    with tf.GradientTape() as tape:
        logits = model(X, training=True)
        loss = loss_fn(y, logits)
    grads = tape.gradient(loss, model.trainable_weights)
    optimizer.apply_gradients(zip(grads, model.trainable_weights))
    acc_metric.update_state(y, logits)
    return loss

for epoch in range(10):
    for X_batch, y_batch in train_dataset:
        loss = train_step(X_batch, y_batch)
    print(f"Epoch {epoch+1}: loss={loss:.4f}, acc={acc_metric.result():.4f}")
    acc_metric.reset_state()
```

### tf.data.Dataset — efficient pipeline

```python
import tensorflow as tf

dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
dataset = (dataset
    .shuffle(buffer_size=10000)
    .batch(128)
    .prefetch(tf.data.AUTOTUNE))

for X_batch, y_batch in dataset.take(1):
    print(X_batch.shape, y_batch.shape)
```

### Saqlash va yuklash

```python
# Saqlash (Keras format — yangi standard)
model.save("model.keras")

# Yuklash
loaded = tf.keras.models.load_model("model.keras")

# Faqat weights
model.save_weights("weights.h5")
new_model.load_weights("weights.h5")

# SavedModel format (TF Serving uchun)
model.export("saved_model_dir/")
```

### TFLite — mobile/edge

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)

# Loading (mobile)
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
```

## 🔌 Backend integratsiyasi

### TF Serving (RECOMMENDED for TF models)

```bash
# Docker bilan
docker run -p 8501:8501 \
  --mount type=bind,source=$(pwd)/saved_model_dir,target=/models/my_model \
  -e MODEL_NAME=my_model \
  tensorflow/serving

# REST API
curl -X POST http://localhost:8501/v1/models/my_model:predict \
  -d '{"instances": [[1.0, 2.0, 3.0, ...]]}'
```

### FastAPI proxy to TF Serving

```python
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
TF_SERVING_URL = "http://localhost:8501/v1/models/my_model:predict"

class Input(BaseModel):
    features: list[float]

@app.post("/predict")
async def predict(data: Input):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TF_SERVING_URL,
            json={"instances": [data.features]},
        )
    return response.json()
```

### Keras model'ni FastAPI'da to'g'ridan-to'g'ri

```python
import tensorflow as tf
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.model = tf.keras.models.load_model("model.keras")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(data: Input):
    X = tf.constant([data.features])
    logits = app.state.model(X, training=False).numpy()
    return {"prediction": int(logits.argmax()), "confidence": float(logits.max())}
```

## 📚 Resurslar

- **TensorFlow tutorials** — [tensorflow.org/tutorials](https://www.tensorflow.org/tutorials)
- **Keras docs** — [keras.io](https://keras.io/)
- **"Deep Learning with Python"** — François Chollet (Keras yaratuvchisi, 2-nashr)
- **Andrew Ng — TensorFlow Professional Certificate** (Coursera)
- **TensorFlow YouTube channel** — official tutorials

## 🏋️ Mashqlar

### 🟢 Easy
1. Sequential API bilan 3 layer MLP yarating va MNIST'da train qiling.
2. `model.summary()` ko'rsatadigan parametrlar sonini interpret qiling.
3. EarlyStopping callback ishlatib training'ni avtomatik to'xtating.

### 🟡 Medium
1. **Custom callback**: har 5 epoch'da loss/acc'ni chiqaradigan custom callback yozing.
2. **Functional API**: 2 ta input (numeric + categorical) bo'lgan model yarating.
3. **Same model, two frameworks**: bir xil MLP'ni PyTorch va Keras'da yozing, accuracy va training time'ni solishtiring.

### 🔴 Hard
1. **TF Serving deployment**: MNIST modelni TF Serving'da Docker bilan deploy qiling, REST API orqali predict qiling.
2. **TF Lite mobile**: modelni `.tflite`'ga export qiling, Python'da yoki Android emulator'da inference qiling.

## 🚀 Capstone

`notebooks/month-03/03_keras_mnist.ipynb`:
- MNIST'da Keras Sequential va Functional API bilan modellar yarating
- TensorBoard'ga loglar yozing
- Callbacks bilan EarlyStopping + ModelCheckpoint
- TF Lite'ga export
- PyTorch capstone'i bilan solishtirish

## ✅ Tekshirish ro'yxati

- [ ] Sequential va Functional API farqini bilaman
- [ ] `model.compile / fit / evaluate` workflow'ni bilaman
- [ ] Callbacks ishlataman (EarlyStopping, ModelCheckpoint)
- [ ] `tf.data.Dataset` pipeline yarata olaman
- [ ] Modelni `.keras`, SavedModel, TFLite formatlarda saqlay olaman
- [ ] TF Serving haqida tushunchaga egaman
- [ ] PyTorch va TF/Keras orasidagi tanlovni asoslab beraman

[Training texnikalari](./04-training-techniques.md) ga o'tamiz — fokus yana PyTorch'da.
