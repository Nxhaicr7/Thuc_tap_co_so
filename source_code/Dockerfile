FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update && apt-get install -y \
    tzdata gcc apt-utils git wget curl nano ffmpeg libsm6 libxext6 libgl1-mesa-glx python3-opencv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gdown

COPY . .

RUN mkdir -p /app/models && \
    gdown "https://drive.google.com/uc?id=1ZngLd066kQP7orXBJRRWnZW-fat43G9K" \
    -O /app/models/efficientnet_b0_rwightman-3dd342df.pth


EXPOSE 5050

CMD ["python", "app.py"]

