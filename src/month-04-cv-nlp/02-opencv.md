# OpenCV bilan ishlash

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- OpenCV'ning asosiy operatsiyalarini bilasiz
- Klassik image processing (filtering, edge detection, contour) qila olasiz
- Real-time video processing yoza olasiz
- ML modellaridan oldin preprocessing qadamlarni bajara olasiz

## 📖 Nimani o'rganish kerak

- **Loading/Saving** — `imread`, `imwrite`, `VideoCapture`
- **Color spaces** — RGB, HSV, Grayscale, Lab
- **Geometric transformations** — resize, rotate, crop, warp
- **Filtering** — blur, Gaussian, median, bilateral
- **Edge detection** — Sobel, Canny
- **Thresholding** — binary, adaptive, Otsu
- **Morphological ops** — erosion, dilation, opening, closing
- **Contours** — finding, drawing, properties
- **Histograms** — equalization, matching
- **Feature detection** — Harris corners, SIFT, ORB
- **Image stitching, perspective correction**

## 📦 Kutubxonalar

```bash
pip install opencv-python opencv-contrib-python
# opencv-contrib-python — qo'shimcha modullar (SIFT, etc.)
```

## 💻 Kod misollari

### Loading va Saving

```python
import cv2

# Image
img = cv2.imread("photo.jpg")               # BGR
img_rgb = cv2.imread("photo.jpg", cv2.IMREAD_COLOR)  # BGR default
gray = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imwrite("output.jpg", img)

# Video
cap = cv2.VideoCapture("video.mp4")        # yoki 0 (webcam)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # process frame
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
```

### Geometric transformations

```python
# Resize
small = cv2.resize(img, (640, 480))
large = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Rotate
h, w = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle=30, scale=1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# Affine transformation (3 nuqta)
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])
M = cv2.getAffineTransform(pts1, pts2)
warped = cv2.warpAffine(img, M, (w, h))

# Perspective transformation (4 nuqta) — masalan, hujjatni "tekislash"
pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
M = cv2.getPerspectiveTransform(pts1, pts2)
warped = cv2.warpPerspective(img, M, (300, 300))
```

### Filtering

```python
# Gaussian blur — shovqinni kamaytirish
blurred = cv2.GaussianBlur(img, (5, 5), sigmaX=1.0)

# Median blur — salt-and-pepper noise uchun
median = cv2.medianBlur(img, 5)

# Bilateral — edge'larni saqlab blur
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# Custom kernel
import numpy as np
sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
sharpened = cv2.filter2D(img, -1, sharpen_kernel)
```

### Edge Detection

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny — eng mashhur
edges = cv2.Canny(gray, threshold1=100, threshold2=200)

# Sobel — gradient
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Laplacian
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```

### Thresholding

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Binary threshold
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Adaptive (per-region)
adaptive = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# Otsu — avtomatik optimal threshold
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### Morphological operations

```python
kernel = np.ones((5, 5), np.uint8)

# Erosion — kichraytiradi (oq nuqtalarni)
eroded = cv2.erode(binary, kernel, iterations=1)

# Dilation — kattalashtiradi
dilated = cv2.dilate(binary, kernel, iterations=1)

# Opening = erosion + dilation (kichik shovqinni o'chiradi)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Closing = dilation + erosion (kichik teshiklarni to'ldiradi)
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

### Contours

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# Chizish
img_with_contours = img.copy()
cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)

# Har contour uchun bounding box
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img_with_contours, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Area
    area = cv2.contourArea(contour)
    
    # Perimeter
    perimeter = cv2.arcLength(contour, closed=True)
    
    # Approximated polygon
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, closed=True)
    # len(approx) — burchaklar soni (4 → to'rtburchak)
```

### Histogram va Equalization

```python
import matplotlib.pyplot as plt

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Histogram
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(hist)
plt.show()

# Histogram equalization — kontrast yaxshilash
equalized = cv2.equalizeHist(gray)

# CLAHE — adaptive histogram equalization (yaxshiroq)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_img = clahe.apply(gray)
```

### Face Detection (klassik — Haar cascade)

```python
# Pretrained Haar cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    roi = gray[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img[y:y+h, x:x+w], (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
```

> **Eslatma:** Modern face detection uchun **MediaPipe** yoki **DeepFace** ko'p marotaba yaxshi.

### Webcam'dan real-time processing

```python
cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Edges
    edges = cv2.Canny(gray, 100, 200)
    
    cv2.imshow("Original", frame)
    cv2.imshow("Edges", edges)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

## 🔌 Backend integratsiyasi

### Image preprocessing service

```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import Response
import cv2
import numpy as np

app = FastAPI()

@app.post("/preprocess/document")
async def preprocess_document(file: UploadFile):
    """Hujjat rasmini OCR uchun tayyorlash."""
    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # 3. Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        11, 2
    )
    
    # 4. Morphology
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Encode and return
    _, buf = cv2.imencode(".png", cleaned)
    return Response(content=buf.tobytes(), media_type="image/png")
```

### Background removal (oddiy)

```python
@app.post("/remove-background")
async def remove_background(file: UploadFile):
    contents = await file.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    # GrabCut algorithm
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    rect = (10, 10, img.shape[1] - 10, img.shape[0] - 10)
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    result = img * mask2[:, :, np.newaxis]
    
    _, buf = cv2.imencode(".png", result)
    return Response(content=buf.tobytes(), media_type="image/png")
```

> **Modern alternative:** **rembg** kutubxonasi (U-Net asosli) ko'p marotaba yaxshi natija beradi.

### Document Scanner-like Perspective Correction

```python
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
```

## 📚 Resurslar

- **OpenCV docs** — [docs.opencv.org](https://docs.opencv.org/)
- **PyImageSearch tutorials** — yuzlab amaliy misollar
- **"Learning OpenCV"** — Adrian Kaehler
- **"Practical Python and OpenCV"** — Adrian Rosebrock
- **OpenCV samples** — GitHub'da `opencv/samples`

## 🏋️ Mashqlar

### 🟢 Easy
1. Rasmni Grayscale, HSV, LAB color space'larga aylantirib chizing.
2. Canny edge detection bilan rasm konturlarini chizing.
3. Adaptive threshold bilan hujjat rasmini binarize qiling.

### 🟡 Medium
1. **Document Scanner**: telefon kamerasidagi hujjatni "tekislash" — contour topish + perspective transform.
2. **Color picker**: rasm yuklang, dominant 5 ta rangni K-Means bilan toping.
3. **Real-time face detection**: webcam'da Haar cascade bilan.

### 🔴 Hard
1. **OCR pipeline preprocessor**: FastAPI servis — hujjat rasmini OCR'ga tayyorlash (denoise, deskew, perspective correction).
2. **Image deduplication**: feature hashing (pHash, dHash) bilan o'xshash rasmlarni topish.
3. **Sport analytics**: video'da harakatlanuvchi obektlarni track qilish (background subtraction + tracking).

## 🚀 Capstone

`notebooks/month-04/02_opencv_pipeline.ipynb`:
- Custom dataset (telefondan 20 ta hujjat rasmi)
- To'liq pipeline: detect → perspective correct → enhance → OCR uchun tayyor
- FastAPI'da endpoint
- Streamlit demo

## ✅ Tekshirish ro'yxati

- [ ] OpenCV va PIL farqini bilaman (BGR vs RGB)
- [ ] Asosiy filtering (Gaussian, median, bilateral)
- [ ] Edge detection (Canny)
- [ ] Thresholding (adaptive, Otsu)
- [ ] Contours topish va analiz
- [ ] Morphological operations
- [ ] Perspective transformation
- [ ] Real-time video processing
- [ ] Image preprocessing endpoint yozdim

[YOLO va Object Detection](./03-yolo-detection.md) ga o'tamiz.
