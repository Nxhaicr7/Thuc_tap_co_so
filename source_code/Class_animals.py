import os.path
from torch.utils.data import Dataset
import cv2
from torchvision.transforms import Compose, Resize, ToTensor
import numpy as np
import torch

class Animals(Dataset):
    def __init__(self, root_path, is_train = True, transform = None):
        self.transform = transform
        if is_train:
            data_paths = os.path.join(root_path, "Training")
        else:
            data_paths = os.path.join(root_path, "Validation")
        self.labels = []
        self.images = []
        self.catelogies = ['Beetle','Butterfly', 'Cat', 'Chicken', 'Cow',
                           'Dog', 'Elephant', 'Gorilla', 'Hippo', 'Horse',
                           'Lizard', 'Monkey', 'Mouse', 'Panda', 'Sheep',
                           'Spider', 'Squirrel', 'Tiger', 'Zebra']
        self.classes = self.catelogies
        for ind, catelogy in enumerate(self.catelogies):
            catelogy_path = os.path.join(data_paths, catelogy)
            for file in os.listdir(catelogy_path):
                file_path = os.path.join(catelogy_path, file)
                self.images.append(file_path)
                self.labels.append(ind)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, item):
        image_path = self.images[item]
        image = cv2.imread(image_path)
        if self.transform:
            image = self.transform(image)
        label = self.labels[item]
        return image, torch.tensor(label, dtype=torch.long)


if __name__ == "__main__":
    transform = Compose([
        ToTensor(),        #Transform to Tensor
        Resize((224, 224)) #Resize image
    ])
    data = Animals("animals", True, transform) #Choose training image
    test_image, test_label = data[1234]
    label = data.catelogies[test_label]
    test_image = test_image.permute(1, 2, 0).numpy() #Convert tensor(C,H,W) to NumPy(H,W,C) for display with OpenCV
    test_image = (test_image * 255).astype(np.uint8) #Return [0,1] to [0,255]
    cv2.imshow("{}".format(label), test_image)
    cv2.waitKey(0)
