DEEP LEARNING: Tạo AI COMPUTER VISION để phân biệt động vật
link file dataset và trọng số model: https://drive.google.com/file/d/1OU0h0KUqxxFefV1O1ayMb7gNjcETE2qE/view?usp=drive_link
HƯỚNG DẪN CHẠY ỨNG DỤNG

1. Cài đặt môi trường
a,Yêu cầu:
Python 3.8+, pip, tải link dataset và trọng số model, giải nén file animals.zip để lấy dataset
Điều chỉnh cấu trúc folder thành như sau:

source_code/

│

├── app.py    # File chính chạy ứng dụng Flask

├── Model.py                  # Định nghĩa model EfficientNet

├── Inference.py             # Xử lý inference cho ảnh

├── Train.py                 # Code training model

├── Class_animals.py         # Dataset class cho animals

├── CallBack.py              # Callback functions cho training

├── requirements.txt         # Danh sách các thư viện cần thiết

├── Dockerfile               # Cấu hình Docker

├── README.md                # Hướng dẫn sử dụng

├── efficientnet_b0_rwightman-3dd342df.pth # FIle trọng số EfficientNet_B0

├── static/                  # Thư mục chứa file tĩnh

│   ├── AnimalClassifier.jpeg

│   └── ... (các ảnh upload)


├── templates/               # Thư mục chứa file HTML

│   ├── index.html          # Trang chủ

│   └── webcam.html         # Trang webcam

│

├── animals/                 # Dataset gốc

│   ├── Training/           # Ảnh training

│   └── Validation/         # Ảnh validation

│

├── checkpoint/              # Lưu model đã train

│   └── animals/

│       └── best.pt         # Model tốt nhất

│

├── precheckpoint/          # Checkpoint trước khi train

│   └── animals/

│       └── last.pt         # Model chạy epoch sau cùng

├── test_image/ # Ảnh test

│   └── animals/

├── tensorboard/            # Log cho tensorboard




 
b, Cài đặt các thư viện cần thiết:
cd source_code
pip install -r requirements.txt


2. Chạy ứng dụng
python app.py
