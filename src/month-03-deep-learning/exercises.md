# Oy 3 — Mashqlar to'plami

## 🟢 Easy

### PyTorch Basics
1. 5 ta turli shape'dagi tensor yarating va shape, dtype, device atributlarini chiqaring.
2. `requires_grad=True` bilan oddiy funksiyalar uchun gradient'larni hisoblang.
3. `nn.Module` subclass yarating — input → 3 ta hidden → output.

### Training
1. MNIST'da MLP 95%+ accuracy.
2. Optimizers solishtirish: SGD, SGD+momentum, Adam, AdamW.
3. Learning rate ni 1e-1, 1e-3, 1e-5 qilib effect ko'rish.

### CNN
1. SimpleCNN CIFAR-10'da train (5 epoch).
2. Pretrained ResNet-18 yuklang, ImageNet rasm classifier.
3. `torchvision.transforms` bilan augmentation qatorini yarating.

### RNN/LSTM
1. `nn.RNN`, `nn.LSTM`, `nn.GRU` ni bir xil masala uchun solishtiring.
2. Sin function uchun next-step forecasting.
3. Bidirectional LSTM yarating, oddiy LSTM bilan farqi.

## 🟡 Medium

### Production-ready training
1. **Full training pipeline**: Mixed precision + early stopping + checkpoint + W&B logging.
2. **Hyperparameter tuning**: Optuna bilan PyTorch model uchun.
3. **Multi-GPU**(Colab Pro yoki Kaggle bilan): `nn.DataParallel`.

### Transfer learning
1. **Flower classification**: 102 turdagi gullar — pretrained EfficientNet, 92%+ accuracy.
2. **Custom domain**: O'zingiz tasvir to'plang (telefon kamerasi), 5 ta sinf, 50 ta rasm har sinfda — transfer learning bilan ishlatish.
3. **Few-shot learning**: 5 ta rasm har sinfdan, 90%+ accuracy olishga harakat.

### Time series
1. **Real stock data**(yfinance): LSTM + sliding window forecasting.
2. **Multivariate**: bir nechta xususiyat (price, volume, indicators) bilan LSTM.
3. **Prophet vs LSTM**solishtirish.

### Text
1. **IMDB sentiment**: LSTM bilan 85%+ accuracy.
2. **News classification**: 4-5 ta kategoriya (AG News).
3. **Char-level language model**: Shakespeare yoki o'zbek matnda.

## 🔴 Hard

### 1. Production ML API
- Image classification (EfficientNet) FastAPI
- Multi-stage Dockerfile (build → runtime)
- Async batching (vakt va GPU optimization)
- Healthcheck, metrics endpoint
- Load test (Locust bilan): 100 req/s ga chiday oladigan optimization

### 2. Distributed training
- Kaggle Notebooks Pro yoki Colab Pro
- `DistributedDataParallel` bilan 2 GPU
- Mixed precision + gradient accumulation
- Trening vaqtini single GPU bilan solishtirish

### 3. Model interpretation service
- ResNet bilan rasm classification
- Grad-CAM ham qaytaradigan endpoint
- Streamlit yoki React UI

### 4. End-to-end CV pipeline
- Data: web'dan rasmlar to'plash (Selenium yoki API)
- Labelling (Label Studio yoki manual)
- Training (PyTorch + W&B)
- Deploying (FastAPI + Docker + Nginx)
- Monitoring (Prometheus + Grafana)

## Mini-loyihalar

### Mini-loyiha 1: Plant Disease Detector
- Dataset: PlantVillage (Kaggle)
- Transfer learning bilan 95%+ accuracy
- Mobile-friendly (TFLite yoki PyTorch Mobile)
- Streamlit demo

### Mini-loyiha 2: Real-time Pose Estimation
- MediaPipe yoki MMPose
- Webcam streaming
- WebSocket + FastAPI

### Mini-loyiha 3: Music Genre Classifier
- GTZAN dataset
- Mel-spectrogram + CNN
- FastAPI: audio upload → genre

### Mini-loyiha 4: Time Series Anomaly Detection
- Server metrics (CPU, RAM)
- LSTM autoencoder
- Real-time alert system

## Quiz

### Fundamentals
1. Backpropagation qanday ishlaydi (chain rule)?
2. Vanishing gradient nima va qanday hal qilinadi?
3. Batch size va learning rate orasidagi munosabat?
4. Why ReLU > Sigmoid (modern NN'larda)?
5. Dropout test paytida nima qiladi?

### PyTorch
1. `model.eval()` va `torch.no_grad()` farqi?
2. `state_dict()` nimani saqlaydi?
3. `DataLoader` da `num_workers` va `pin_memory` ta'siri?
4. Mixed precision (AMP) qachon foyda beradi?
5. TorchScript va ONNX export'ning afzallik/kamchiligi?

### CNN
1. 3x3 kernel nima uchun keng tarqalgan?
2. Max va Average pooling qachon qaysi birini ishlatasiz?
3. ResNet'ning skip connection'i nima uchun ishlatiladi?
4. EfficientNet'ning compound scaling'i nima?
5. Receptive field nima va qanday hisoblanadi?

### RNN
1. RNN va Feedforward NN farqi?
2. LSTM gate'lari va vazifalari?
3. Bidirectional RNN qachon foyda beradi?
4. Why gradient clipping is critical for RNN?
5. RNN'dan Transformer'ga ko'chish sabablari?

## ✅ Oy 3 oxiri checklist

- [ ] Pure NumPy bilan oddiy NN yozdim
- [ ] PyTorch'da `nn.Module` va training loop
- [ ] TensorFlow/Keras bilan tanishlik
- [ ] CNN bilan image classification (CIFAR-10 yoki o'xshash)
- [ ] Transfer learning (pretrained model bilan)
- [ ] RNN/LSTM bilan sequence task (time series yoki text)
- [ ] W&B yoki TensorBoard'da experiment tracking
- [ ] FastAPI'da DL model serving (CPU yoki GPU'da)
- [ ] Capstone loyiha GitHub'da
- [ ] LinkedIn'ga post

Tabriklayman! [Oy 4 — Computer Vision + NLP](../month-04-cv-nlp/README.md) ga o'tamiz.
