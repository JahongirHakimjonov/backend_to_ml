# Month 03 — Deep Learning Notebooks

| Notebook | Mavzu | Bob |
|----------|-------|-----|
| `01_neural_network_scratch.ipynb` | NumPy NN | [Neural Networks](../../src/month-03-deep-learning/01-neural-networks.md) |
| `02_pytorch_mnist.ipynb` | PyTorch MNIST | [PyTorch basics](../../src/month-03-deep-learning/02-pytorch-basics.md) |
| `03_keras_mnist.ipynb` | Keras MNIST | [TF/Keras](../../src/month-03-deep-learning/03-tensorflow-keras.md) |
| `04_training_techniques.ipynb` | Augmentation, AMP | [Training](../../src/month-03-deep-learning/04-training-techniques.md) |
| `05_cnn_image_classification.ipynb` | CIFAR-10 + transfer | [CNN](../../src/month-03-deep-learning/05-cnn.md) |
| `06_rnn_timeseries.ipynb` | LSTM forecasting | [RNN](../../src/month-03-deep-learning/06-rnn-lstm.md) |

## 🛠 Dependencies

```bash
# PyTorch + tools (asosiy)
uv sync --group month-03

# TensorFlow/Keras qo'shimcha kerak bo'lsa
uv sync --group month-03 --group tf-extras

# NVIDIA CUDA bilan PyTorch (Linux/Windows)
uv sync --group month-03 --index pytorch-cu121

uv run jupyter lab
```

Tarkibida: torch, torchvision, torchaudio, wandb, tensorboard, albumentations. `timm` Oy 4'da CV uchun.

## 🖥 GPU recommendation

- **Mac M1/M2/M3:** MPS automatic
- **NVIDIA:** CUDA + cuDNN
- **Bepul:** Google Colab T4, Kaggle P100

## 📚 Datasets

- **MNIST, Fashion-MNIST** — torchvision
- **CIFAR-10** — torchvision
- **ImageNet subset** — Kaggle
- **Stock data** — yfinance

[Asosiy bob](../../src/month-03-deep-learning/README.md).
