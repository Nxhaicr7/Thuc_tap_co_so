# 🐾 Animal Classification - Deep Learning Project

Ứng dụng AI phân loại động vật sử dụng Computer Vision với EfficientNet-B0.

## 📋 Tính năng

- ✅ Phân loại 19 loài động vật
- 📸 Upload ảnh để phân loại
- 🎥 Sử dụng webcam real-time
- 🎯 Độ chính xác cao với EfficientNet-B0
- 🌐 Giao diện web đẹp với Flask

## 🦁 19 loài động vật được hỗ trợ

Beetle, Butterfly, Cat, Chicken, Cow, Dog, Elephant, Gorilla, Hippo, Horse, Lizard, Monkey, Mouse, Panda, Sheep, Spider, Squirrel, Tiger, Zebra

## 📁 Cấu trúc project

```
source_code/
├── app.py                                      # Flask application
├── Model.py                                    # EfficientNet model definition
├── Inference.py                                # Inference logic
├── Train.py                                    # Training script
├── Class_animals.py                            # Dataset class
├── CallBack.py                                 # Training callbacks
├── requirements.txt                            # Python dependencies
├── Dockerfile                                  # Docker configuration
├── efficientnet_b0_rwightman-3dd342df.pth     # Pretrained weights
├── templates/                                  # HTML templates
│   ├── index.html
│   └── webcam.html
├── static/                                     # Static files (uploaded images)
├── checkpoint/animals/                         # Best model checkpoint
│   └── best.pt
├── precheckpoint/animals/                      # Last epoch checkpoint
│   └── last.pt
├── animals/                                    # Dataset (download separately)
│   ├── Training/
│   └── Validation/
├── test_image/                                 # Test images
└── tensorboard/                                # Training logs
```

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống

- Python 3.8+
- pip
- (Optional) CUDA cho GPU training

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Tải dataset và model

1. Tải file từ: https://drive.google.com/file/d/1OU0h0KUqxxFefV1O1ayMb7gNjcETE2qE/view?usp=drive_link
2. Giải nén `animals.zip` vào thư mục `source_code/animals/`
3. File pretrained weights `efficientnet_b0_rwightman-3dd342df.pth` đã có sẵn

## 💻 Chạy ứng dụng

### Chạy web application

```bash
python app.py
```

Truy cập: http://localhost:5000

### Chạy inference trên ảnh đơn

```bash
python Inference.py -i test_image/ -f your_image.jpg
```

### Training model

```bash
python Train.py -r animals -b 32 -e 200 -l 0.0001
```

**Arguments:**
- `-r`: Đường dẫn đến dataset
- `-b`: Batch size
- `-e`: Số epoch
- `-l`: Learning rate
- `-p`: Pre-checkpoint path (để tiếp tục training)
- `-c`: Checkpoint save path

### Xem training progress với TensorBoard

```bash
tensorboard --logdir=tensorboard/animals
```

## 🐳 Chạy với Docker

```bash
# Build image
docker build -t animal-classifier .

# Run container
docker run -p 5000:5000 animal-classifier
```

## 📊 Kiến trúc Model

- **Base Model**: EfficientNet-B0 (pretrained on ImageNet)
- **Input Size**: 224x224
- **Number of Classes**: 19
- **Optimizer**: SGD with momentum
- **Loss Function**: CrossEntropyLoss

## 🎯 API Endpoints

### `POST /`
Upload ảnh và nhận kết quả phân loại

### `GET /webcam`
Trang sử dụng webcam

### `POST /api/predict_webcam`
API nhận ảnh từ webcam (base64) và trả về kết quả

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

## 📝 Lưu ý

- Ảnh upload phải có định dạng: PNG, JPG, JPEG
- Kích thước file tối đa: 5MB
- Kích thước ảnh: 100x100 đến 2000x2000 pixels
- Model được lưu tự động khi accuracy cải thiện
- Early stopping sau 10 epoch không cải thiện

## 🔧 Troubleshooting

### Lỗi: "No module named 'torch'"
```bash
pip install torch torchvision
```

### Lỗi: "Không tìm thấy checkpoint"
Đảm bảo đã train model hoặc tải checkpoint từ link Google Drive

### Lỗi: "Templates not found"
Đảm bảo file HTML nằm trong thư mục `templates/`

## 📄 License

Educational project - Free to use

## 👥 Contributors

Thực tập cơ sở - Deep Learning project
