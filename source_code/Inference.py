import argparse
import cv2
from Model import get_efficient
import numpy as np
import torch.nn as nn
import torch
import os
import base64

categories = ['Beetle', 'Butterfly', 'Cat', 'Chicken', 'Cow',
              'Dog', 'Elephant', 'Gorilla', 'Hippo', 'Horse',
              'Lizard', 'Monkey', 'Mouse', 'Panda', 'Sheep',
              'Spider', 'Squirrel', 'Tiger', 'Zebra']

def get_arg():
    parser = argparse.ArgumentParser("Inference")
    parser.add_argument("--image_path", "-i", type=str, default="./test_image/")
    parser.add_argument("--image_file", "-f", type=str, default="Pasted image (2).png")
    parser.add_argument("--size", "-s", type=int, default=224)
    parser.add_argument("--checkpoint", "-c", type=str, default="checkpoint/animals/best.pt")
    parser.add_argument("--webcam", action="store_true", help="Use webcam for real-time inference")
    return parser.parse_args()

def load_model(checkpoint_path, num_classes=19, device='cpu'):
    model = get_efficient(num_classes, "efficientnet_b0_rwightman-3dd342df.pth")
    checkpoint = torch.load(checkpoint_path, map_location=torch.device(device))
    model.load_state_dict(checkpoint["model"])
    model.eval()
    return model

def preprocess_image(image, size=224):
    img = cv2.resize(image, (size, size))
    img = np.transpose(img, (2, 0, 1)) / 255.0
    img = np.expand_dims(img, axis=0)
    return torch.from_numpy(img).float()

def inference_from_path(image_path, size=224, checkpoint_path="checkpoint/animals/best.pt"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

    # Save resized image for UI
    resized_image_path = os.path.join("static", "resized_" + os.path.basename(image_path))
    cv2.imwrite(resized_image_path, cv2.resize(image, (224, 224)))

    img_tensor = preprocess_image(image, size)
    model = load_model(checkpoint_path)
    softmax = nn.Softmax(dim=1)

    with torch.no_grad():
        predict = model(img_tensor)
        prob = softmax(predict)
        max_value, max_index = torch.max(prob, 1)

    label = categories[max_index.item()]
    score = max_value.item()
    return label, score, resized_image_path

def inference_from_base64(base64_data, size=224, checkpoint_path="checkpoint/animals/best.pt"):
    image_bytes = base64.b64decode(base64_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Không thể giải mã ảnh từ base64")

    img_tensor = preprocess_image(image, size)
    model = load_model(checkpoint_path)
    softmax = nn.Softmax(dim=1)

    with torch.no_grad():
        predict = model(img_tensor)
        prob = softmax(predict)
        max_value, max_index = torch.max(prob, 1)

    label = categories[max_index.item()]
    score = max_value.item()
    return label, score

def inference(args):
    full_path = os.path.join(args.image_path, args.image_file)
    label, score, _ = inference_from_path(full_path, size=args.size, checkpoint_path=args.checkpoint)
    image = cv2.imread(full_path)
    image = cv2.resize(image, (224, 224))
    cv2.imshow(f"{label} has {score:.2f} confidence", image)
    cv2.waitKey(0)
