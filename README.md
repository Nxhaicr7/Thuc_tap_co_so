# 🐾 Animal Classification AI

Ứng dụng web phân loại động vật sử dụng Deep Learning và Computer Vision.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Tính năng

- 🎯 **Phân loại 19 loài động vật** với độ chính xác cao
- 📸 **Upload ảnh** để nhận diện động vật
- 🎥 **Real-time webcam** detection
- 🚀 **Sẵn sàng chạy** - Bao gồm model đã train
- 🎨 **Giao diện đẹp** - Responsive web UI

## 🦁 Các loài động vật được hỗ trợ

```
Beetle (Bọ hung)      Butterfly (Bướm)     Cat (Mèo)
Chicken (Gà)          Cow (Bò)             Dog (Chó)
Elephant (Voi)        Gorilla (Khỉ đột)    Hippo (Hà mã)
Horse (Ngựa)          Lizard (Thằn lằn)    Monkey (Khỉ)
Mouse (Chuột)         Panda (Gấu trúc)     Sheep (Cừu)
Spider (Nhện)         Squirrel (Sóc)       Tiger (Hổ)
Zebra (Ngựa vằn)
```

## 🚀 Quick Start

### 1. Clone repository

```bash
git clone https://github.com/Nxhaicr7/Thuc_tap_co_so.git
cd Thuc_tap_co_so/source_code
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng

```bash
python app.py
```

Truy cập: **http://localhost:5000**

## 📦 Cấu trúc Project

```
Thuc_tap_co_so/
├── source_code/
│   ├── app.py                              # Flask web application
│   ├── Model.py                            # EfficientNet-B0 model
│   ├── Inference.py                        # Inference logic
│   ├── Train.py                            # Training script
│   ├── Class_animals.py                    # Dataset loader
│   ├── CallBack.py                         # Training callbacks
│   ├── requirements.txt                    # Dependencies
│   ├── Dockerfile                          # Docker config
│   ├── efficientnet_b0_rwightman-3dd342df.pth  # Pretrained weights
│   ├── checkpoint/animals/
│   │   └── best.pt                         # Trained model ✅
│   ├── templates/
│   │   ├── index.html                      # Upload page
│   │   └── webcam.html                     # Webcam page
│   └── static/                             # Uploaded images
└── README.md                                # This file
```

## 🎯 Kiến trúc Model

- **Base Model**: EfficientNet-B0 (pretrained on ImageNet)
- **Input Size**: 224x224x3
- **Number of Classes**: 19
- **Optimizer**: SGD (lr=0.0001, momentum=0.9)
- **Loss**: CrossEntropyLoss

## 💻 Sử dụng

### Web Interface

1. **Upload Image**: Tải ảnh lên và nhận kết quả phân loại
2. **Webcam**: Sử dụng camera để phát hiện real-time

### Command Line Inference

```bash
cd source_code
python Inference.py -i test_image/ -f your_image.jpg
```

### Training (Nếu có dataset)

```bash
python Train.py -r animals -b 32 -e 200 -l 0.0001
```

**Arguments:**
- `-r`: Đường dẫn dataset
- `-b`: Batch size
- `-e`: Số epochs
- `-l`: Learning rate

## 🐳 Docker

```bash
# Build image
docker build -t animal-classifier .

# Run container
docker run -p 5000:5000 animal-classifier
```

## 📊 API Endpoints

### `POST /`
Upload ảnh và nhận kết quả

### `GET /webcam`
Trang webcam detection

### `POST /api/predict_webcam`
API nhận ảnh base64 từ webcam

**Request:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "label": "Cat",
  "score": "0.95"
}
```

## 🛠 Tech Stack

- **Backend**: Flask, PyTorch, OpenCV
- **Frontend**: HTML, CSS, JavaScript
- **Model**: EfficientNet-B0
- **Training**: TensorBoard, scikit-learn

## 📝 Requirements

- Python 3.8+
- PyTorch 2.0+
- Flask
- OpenCV
- See `requirements.txt` for full list

## 🎓 Về Project

Đây là project thực tập cơ sở về Deep Learning và Computer Vision, sử dụng:
- Transfer Learning với EfficientNet-B0
- Data Augmentation
- Early Stopping
- Model Checkpointing

## 📄 License

Educational Project - Free to use

## 👥 Author

**Nguyễn Xuân Hải** - B22DCCN271

## 🔗 Links

- [Source Code](./source_code/)
- [Documentation](./source_code/README.md)
- [Model Checkpoint](./source_code/checkpoint/animals/)

---

⭐ Star this repo if you find it helpful!
