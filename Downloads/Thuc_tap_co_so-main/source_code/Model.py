import torch
import torch.nn as nn
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0

def get_efficient(number_classes, pretrained_path=None):
    model = efficientnet_b0(weights=None)
    if pretrained_path:
        state_dict = torch.load(pretrained_path, map_location="cpu")
        model.load_state_dict(state_dict)

    #Extract in_features from model (1280)
    in_features = model.classifier[1].in_features
    #Replace classifier layer
    model.classifier[1] = nn.Linear(in_features, number_classes)
    return model

if __name__ == "__main__":
    model = get_efficient(19, pretrained_path="efficientnet_b0_rwightman-3dd342df.pth")
    batch_size = 64
    x = torch.rand(batch_size, 3, 224, 224)
    output = model(x)
    print(output)
