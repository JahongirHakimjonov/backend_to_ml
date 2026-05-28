# Oy 3 — Deep Learning

## 🎯 Bu oydagi maqsad

Oy oxirida siz quyidagilarni qila olasiz:
- Neural network nima ekanini, qanday ishlashini tushunasiz
- PyTorch'da o'z neural network'ingizni quryasiz va o'rgatasiz
- TensorFlow/Keras bilan tanishasiz
- CNN bilan image classification qila olasiz
- RNN/LSTM bilan sequence data'ni qayta ishlay olasiz
- Transfer learning'ni qo'llay olasiz

## 📅 Haftalik taqsimot

| Hafta | Mavzu | Vaqt |
|-------|-------|------|
| **Hafta 1** | Neural Networks asoslari + PyTorch | 10-12 soat |
| **Hafta 2** | TensorFlow/Keras + Training texnikalari | 10-12 soat |
| **Hafta 3** | CNN va Image Classification | 10-12 soat |
| **Hafta 4** | RNN/LSTM + Transfer Learning | 10-12 soat |

## 📖 Boblar tartibi

1. [Neural Networks asoslari](./01-neural-networks.md) — perceptron, backprop, intuition
2. [PyTorch asoslari](./02-pytorch-basics.md) — tensor, autograd, nn.Module
3. [TensorFlow va Keras](./03-tensorflow-keras.md) — alternativ framework
4. [Training texnikalari](./04-training-techniques.md) — optimizers, regularization, callbacks
5. [CNN — Convolutional Networks](./05-cnn.md) — rasm classification
6. [RNN, LSTM, GRU](./06-rnn-lstm.md) — sequence data
7. [Mashqlar](./exercises.md)

## 🎓 Oy oxirida nima qila olasiz?

- PyTorch'da `nn.Module` yozish va training loop qurish
- MNIST, CIFAR-10 kabi datasetlarda 95%+ accuracy
- Pretrained model (ResNet, EfficientNet) ni fine-tune qilish
- FastAPI orqali GPU-powered prediction servis
- ML model'larni `torch.save` / `torch.jit` bilan production'ga olib chiqish

## 💡 Backend Dev uchun maslahat

DL = "Layered functions + Automatic differentiation". Sizga **2 ta narsa** kerak:

1. **Model arxitekturasi** — qatlamlarni yig'ish (LEGO kabi)
2. **Training loop** — for-each-batch: forward → loss → backward → optimizer

Birinchi marta murakkab tuyuladi, lekin 2-3 ta misol yozgandan keyin "patternni" sezasiz.

## 🖥 Hardware haqida

DL — bu CPU emas, **GPU** uchun yaratilgan. Variantlar:

1. **Mac M1/M2/M3** — `MPS` backend (PyTorch 2.0+) — kichik modellar uchun yetarli
2. **Local NVIDIA GPU** (RTX 3060+) — CUDA + cuDNN o'rnatish
3. **Google Colab** — bepul T4 GPU (12 soat/sessiya) — **TAVSIYA**
4. **Kaggle Notebooks** — bepul P100 GPU (30 soat/hafta)
5. **Pullik:** Lambda Labs, vast.ai, RunPod — soatiga $0.20-2

**Maslahat:** Lokal mashqlar uchun CPU/M-chip, capstone uchun Colab/Kaggle GPU.

## 🚀 Boshlash

[Neural Networks asoslari](./01-neural-networks.md) ga o'ting.
