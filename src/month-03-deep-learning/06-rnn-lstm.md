# RNN, LSTM, GRU

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- Sequence data (matn, time series, audio) bilan ishlash uchun NN arxitekturasini bilasiz
- RNN, LSTM, GRU farqini va qachon qaysi birini ishlatishni bilasiz
- Vanishing gradient muammosini va LSTM yechimini tushunasiz
- Time series forecasting va text classification yozasiz
- Transformers (Oy 4'da) ga o'tishga tayyor bo'lasiz

> **Eslatma:** Hozirgi era — **Transformers** (BERT, GPT, T5) erasi. RNN/LSTM ko'p hollarda eskirayotgan. Lekin time series'da hali ham foydali va NN tarixi/intuition uchun muhim.

## 📖 Nimani o'rganish kerak

- **RNN** — Recurrent Neural Network asoslari
- **Vanishing/Exploding Gradient** muammosi
- **LSTM** — Long Short-Term Memory
- **GRU** — Gated Recurrent Unit
- **Bidirectional RNN/LSTM**
- **Seq2Seq** — encoder-decoder
- **Attention mechanism** (Transformers'ga ko'prik)
- **Time series forecasting** — sliding window approach
- **Text classification with LSTM**

## 📦 Kutubxonalar

```bash
pip install torch torchtext pandas
```

## 🧠 Muhim mavzular

### RNN — Recurrent Neural Network

```
Sequence: [x₁, x₂, x₃, ...]

   x₁              x₂              x₃
    │               │               │
    ▼               ▼               ▼
  [RNN] ──h₁──> [RNN] ──h₂──> [RNN] ──h₃──>
                                              
h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)
```

Asosiy g'oya: avvalgi hidden state (`h_{t-1}`) joriy input bilan birgalikda yangi state hosil qiladi.

### Vanishing Gradient muammosi

Uzun sequence'larda gradient `tanh` orqali qayta-qayta o'tib **nolga yaqinlashadi** — model uzoq dependency'larni o'rgana olmaydi.

**Yechim — LSTM:** maxsus "gate"lar bilan ma'lumotni saqlash/o'chirish.

### LSTM — to'liq strukturasi

```
                    cell state (C)
                    ──────────────►
                       ↑    ↑    ↑
                       │    │    │
                    [forget] [input] [output]
                       gate    gate    gate
                       │    │    │
                       └────┴────┘
                          ↑
                       h_t-1, x_t
```

3 ta gate:
- **Forget gate (f):** cell state'dagi nimani o'chirish
- **Input gate (i):** yangi nima qo'shish
- **Output gate (o):** keyingi hidden state nima bo'lishi

### GRU — soddalashtirilgan LSTM

- 2 ta gate (reset, update)
- LSTM'dan tezroq, kam parametr
- Aniqlik LSTM'ga teng yoki yaqin

### Qaysi qachon?

| Use case | Tavsiya |
|----------|---------|
| **Text classification** | LSTM/GRU bidirectional, yoki **BERT** (Oy 4) |
| **Time series forecasting** | LSTM, yoki **Prophet/N-BEATS** |
| **Sentiment analysis** | **BERT** (transformer) |
| **Translation** | **Transformer** (T5, MarianMT) |
| **Sequence generation** | **GPT-style transformer** |
| **Audio processing** | Conv1D + LSTM yoki wav2vec |

**Qoida:** Yangi loyihada **transformer**dan boshlang. RNN/LSTM ni faqat real sabab bilan (kichik dataset, real-time inference, simple time series).

## 💻 Kod misollari

### Oddiy RNN

```python
import torch
import torch.nn as nn

class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # x shape: (batch, seq_len, input_size)
        out, hidden = self.rnn(x)
        # out shape: (batch, seq_len, hidden_size)
        # oxirgi timestep'ni olish
        last_output = out[:, -1, :]
        logits = self.fc(last_output)
        return logits

model = SimpleRNN(input_size=10, hidden_size=64, num_classes=5)
x = torch.randn(32, 20, 10)  # batch=32, seq_len=20, features=10
print(model(x).shape)  # (32, 5)
```

### LSTM — Time Series Forecasting

```python
class LSTMForecaster(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0,
        )
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # x shape: (batch, seq_len, input_size)
        out, (h_n, c_n) = self.lstm(x)
        # Oxirgi timestep
        last_output = out[:, -1, :]
        return self.fc(last_output)
```

### Sliding window approach

```python
def create_sequences(data, seq_length):
    """1D time series → (X, y) pairs."""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return torch.tensor(X, dtype=torch.float32).unsqueeze(-1), torch.tensor(y, dtype=torch.float32)

# Misol — sin function bashorat
import numpy as np
data = np.sin(np.linspace(0, 100, 1000))
X, y = create_sequences(data, seq_length=20)
# X shape: (980, 20, 1), y shape: (980,)
```

### Text classification with LSTM

```python
class TextClassifierLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes, n_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=n_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.3,
        )
        # Bidirectional → hidden_dim * 2
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x, lengths=None):
        # x shape: (batch, seq_len) — token IDs
        embedded = self.embedding(x)
        
        if lengths is not None:
            # Variable length sequences uchun
            packed = nn.utils.rnn.pack_padded_sequence(
                embedded, lengths.cpu(), batch_first=True, enforce_sorted=False
            )
            _, (hidden, _) = self.lstm(packed)
        else:
            _, (hidden, _) = self.lstm(embedded)
        
        # Bidirectional final hidden: forward + backward
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        hidden = self.dropout(hidden)
        return self.fc(hidden)
```

### Training loop (sequence data uchun)

```python
def train_sequence_model(model, train_loader, val_loader, epochs=20, lr=1e-3):
    device = next(model.parameters()).device
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()  # forecasting uchun; classification uchun CrossEntropy
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for X, y in train_loader:
            X, y = X.to(device), y.to(device)
            optimizer.zero_grad()
            
            pred = model(X)
            loss = criterion(pred.squeeze(), y)
            loss.backward()
            
            # MUHIM: RNN uchun gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            train_loss += loss.item()
        
        # Eval
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X, y in val_loader:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                val_loss += criterion(pred.squeeze(), y).item()
        
        print(f"Epoch {epoch+1}: train={train_loss/len(train_loader):.4f}  "
              f"val={val_loss/len(val_loader):.4f}")
```

### Encoder-Decoder (Seq2Seq) preview

```python
class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
    
    def forward(self, x):
        _, (h, c) = self.lstm(x)
        return h, c  # context

class Decoder(nn.Module):
    def __init__(self, output_size, hidden_size):
        super().__init__()
        self.lstm = nn.LSTM(output_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x, h, c):
        out, (h, c) = self.lstm(x, (h, c))
        return self.fc(out), h, c

# Seq2Seq:
# encoder(input) → context
# decoder(<START>, context) → output_1
# decoder(output_1, context) → output_2
# ...
```

## 🔌 Backend integratsiyasi

### Time series forecasting API

```python
from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np

app = FastAPI()
model = LSTMForecaster()
model.load_state_dict(torch.load("forecaster.pt"))
model.eval()

class ForecastInput(BaseModel):
    historical_values: list[float]
    forecast_steps: int = 7

class ForecastOutput(BaseModel):
    predictions: list[float]

@app.post("/forecast", response_model=ForecastOutput)
@torch.no_grad()
def forecast(data: ForecastInput):
    # Last 20 values as input
    history = torch.tensor(data.historical_values[-20:], dtype=torch.float32)
    history = history.unsqueeze(0).unsqueeze(-1)  # (1, 20, 1)
    
    predictions = []
    for _ in range(data.forecast_steps):
        pred = model(history).item()
        predictions.append(pred)
        # Slide window: drop first, append prediction
        history = torch.cat([history[:, 1:, :], torch.tensor([[[pred]]])], dim=1)
    
    return ForecastOutput(predictions=predictions)
```

### Text sentiment API (LSTM)

```python
@app.post("/sentiment")
@torch.no_grad()
def predict_sentiment(text: str):
    tokens = tokenizer(text, max_length=200, padding="max_length", truncation=True)
    X = torch.tensor([tokens]).long()
    
    logits = model(X)
    probs = torch.softmax(logits, dim=1).squeeze()
    
    labels = ["negative", "neutral", "positive"]
    return {
        "sentiment": labels[probs.argmax().item()],
        "scores": {label: float(p) for label, p in zip(labels, probs)},
    }
```

> **Diqqat:** Production sentiment uchun **HuggingFace BERT** ishlatish ko'p marotaba yaxshi natija beradi. LSTM bu yerda misol uchun.

## 📚 Resurslar

- **Andrej Karpathy — "The Unreasonable Effectiveness of RNNs"** (blog)
- **Colah's blog — Understanding LSTMs** ([colah.github.io/posts/2015-08-Understanding-LSTMs](https://colah.github.io/posts/2015-08-Understanding-LSTMs/))
- **PyTorch Sequence tutorials**
- **"Deep Learning for Time Series Forecasting"** — Jason Brownlee
- **fast.ai NLP course** (RNN va beyond)

## 🏋️ Mashqlar

### 🟢 Easy
1. `nn.RNN`, `nn.LSTM`, `nn.GRU` parametrlar sonini solishtiring.
2. Sinusoidal data uchun LSTM bilan next-step forecasting.
3. Bidirectional LSTM va unidirectional natijasini solishtiring.

### 🟡 Medium
1. **Time series**: Real stock price (yfinance) data bilan 30 kunlik forecasting.
2. **Text classification**: IMDB reviews datasetda LSTM bilan binary sentiment (80%+).
3. **Char-level RNN**: Karpathy uslubida character-level text generation.

### 🔴 Hard
1. **Seq2Seq translation** — kichik tilda uchirish (English ↔ German kichik dataset).
2. **Attention mechanism** — LSTM ustiga attention qo'shing (transformer'ga kirish).
3. **Time series API** — Prophet vs LSTM solishtiring, eng yaxshisini FastAPI'da deploy qiling.

## 🚀 Capstone

`notebooks/month-03/06_rnn_timeseries.ipynb`:
- **Yfinance** orqali biror aksiya narxini yuklang (5 yillik)
- Klassik baseline: Prophet, ARIMA
- LSTM modelingiz
- Test set'da forecasting accuracy solishtirish
- FastAPI endpoint

## ✅ Tekshirish ro'yxati

- [ ] RNN, LSTM, GRU farqini bilaman
- [ ] Vanishing gradient muammosini tushunaman
- [ ] LSTM gate'larining vazifasini bilaman
- [ ] Bidirectional va unidirectional farqi
- [ ] Sliding window approach bilan time series uchun data tayyorlay olaman
- [ ] Gradient clipping nima uchun RNN'da muhimligini bilaman
- [ ] Text classification LSTM bilan
- [ ] Transformer'lar (Oy 4) RNN'dan ustun ekanini va sabablarini bilaman

🎉 **Oy 3 tugadi!** [Mashqlar](./exercises.md) ni ko'rib chiqing va [Oy 4 — CV + NLP](../month-04-cv-nlp/README.md) ga o'ting.
