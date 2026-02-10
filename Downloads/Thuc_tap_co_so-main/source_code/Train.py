import argparse
import os.path
import shutil
from torchsummary import summary
import numpy as np
import torch.nn as nn
from torchvision.transforms import ToTensor, Compose, Resize, Normalize
import torch
from Model import get_efficient
from Class_animals import Animals
from torch.utils.data import DataLoader
from torch.optim import SGD
import warnings
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import accuracy_score,confusion_matrix, ConfusionMatrixDisplay
from CallBack import EarlyStopping, ModelCheckPoint
import matplotlib.pyplot as plt

def argument():
    parser = argparse.ArgumentParser(prog= "Argument Parameter")
    parser.add_argument("--root_path", "-r", type = str, default= "animals")
    parser.add_argument("--batch_size", "-b", type = int, default = 32)
    parser.add_argument("--num_workers", "-n", type = int, default = 2)
    parser.add_argument("--learning_rate", "-l", type = float, default = 0.0001)
    parser.add_argument("--momentum", "-m", type = float, default = 0.9)
    parser.add_argument("--size", "-s", type = int, default = 224)
    parser.add_argument("--epoch", "-e", type = int, default = 200)
    parser.add_argument("--pre_checkpoint", "-p", type=str, default="precheckpoint/animals")
    parser.add_argument("--log_file", "-f", type=str, default= "tensorboard/animals")
    parser.add_argument("--checkpoint", "-c", type = str, default = "checkpoint/animals")
    args = parser.parse_args()
    return args

def img_classifier(args):
    warnings.filterwarnings("ignore", category=UserWarning)
    transform = Compose([
        ToTensor(),
        Resize((args.size, args.size)),
        Normalize([0.485, 0.456, 0.406],
                  [0.229, 0.224, 0.225])
    ])

    train_data = Animals(root_path = args.root_path, is_train = True, transform = transform)
    train_loader = DataLoader(train_data, batch_size= args.batch_size, shuffle=True, num_workers = args.num_workers, drop_last=True)

    test_data = Animals(root_path = args.root_path, is_train = False, transform = transform)
    test_loader = DataLoader(test_data, batch_size= args.batch_size, shuffle=False, num_workers= args.num_workers, drop_last=False)

    model = get_efficient(19, "efficientnet_b0_rwightman-3dd342df.pth")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    summary(model, (3, args.size, args.size))
    criterion = nn.CrossEntropyLoss()
    optimize = SGD(model.parameters(), lr= args.learning_rate, momentum= args.momentum)
    num_iter = len(train_loader)

    # Load checkpoint nếu file tồn tại
    if args.pre_checkpoint:
        checkpoint_path = os.path.join(args.pre_checkpoint, "last.pt")
        if os.path.isfile(checkpoint_path):
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            checkpoint = torch.load(checkpoint_path, map_location=device)
            model.load_state_dict(checkpoint["model"])
            optimize.load_state_dict(checkpoint["optimize"])
            start_epoch = checkpoint["epoch"]
            best_acc = checkpoint["best_acc"]
        else:
            start_epoch = 0
            best_acc = -1
    else:
        start_epoch = 0
        best_acc = -1

    if os.path.isdir(args.log_file):
        shutil.rmtree(args.log_file)
    os.makedirs(args.log_file)
    writer = SummaryWriter(args.log_file)

    if not os.path.isdir(args.checkpoint):
        os.makedirs(args.checkpoint)

    early_stopping = EarlyStopping(patience=10, verbose=True)
    best_checkpoint = ModelCheckPoint(os.path.join(args.checkpoint, "best.pt"))

    # Ensure that the model is moved to GPU if available


    for epoch in range(start_epoch, args.epoch):
        # train_step
        model.train()
        train_loss = []
        progress_bar = tqdm(train_loader, colour = "cyan")

        for iter, (image, label) in enumerate(progress_bar):
            image, label = image.to(device), label.to(device)
            output = model(image)
            loss = criterion(output, label)
            optimize.zero_grad()
            loss.backward()
            optimize.step()
            train_loss.append(loss.item())
            avg_loss = np.mean(train_loss)
            writer.add_scalar('train_loss', avg_loss, epoch * num_iter + iter)

            progress_bar.set_description(f"train_epoch {epoch+1}/{args.epoch}")
            progress_bar.set_postfix(loss=f"{avg_loss:.4f}")

        # Validation
        all_label = []
        all_predict = []
        all_loss = []
        model.eval()
        with torch.no_grad():
            progress_bar = tqdm(test_loader, colour = "yellow")
            for image, label in progress_bar:
                image, label = image.to(device), label.to(device)  # Move data to GPU if available
                predict = model(image)
                loss = criterion(predict, label)
                max_predict = torch.argmax(predict, dim=1)
                all_loss.append(loss.item())
                all_predict.extend(max_predict.tolist())
                all_label.extend(label.tolist())

        loss = np.mean(all_loss)
        acc = accuracy_score(all_label, all_predict)

        cm = confusion_matrix(all_label, all_predict)
        class_names = train_data.classes

        # Display confusion matrix by matplotlib
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
        fig, ax = plt.subplots(figsize=(10, 8))
        disp.plot(ax=ax, cmap="Blues", colorbar=False)
        plt.title(f"Confusion Matrix - Epoch {epoch + 1}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        #Save plot as png with epoch number
        plt.savefig(f"confusion_matrix_epoch_{epoch + 1}.png")
        plt.close()

        writer.add_scalar("avg_loss", loss, epoch)
        writer.add_scalar("accuracy", acc, epoch)

        progress_bar.set_description(f"test_epoch: {epoch + 1}/{args.epoch}")
        progress_bar.set_postfix(loss=f"{loss:.4f}")

        # Saving checkpoint
        checkpoint = {
            "epoch": epoch + 1,
            "best_acc": best_acc,
            "model": model.state_dict(),
            "optimize": optimize.state_dict()
        }

        if args.pre_checkpoint:
            torch.save(checkpoint, os.path.join(args.pre_checkpoint, "last.pt"))
        if acc > best_acc:
            best_acc = acc
            torch.save(checkpoint, os.path.join(args.checkpoint, "best.pt"))
        best_checkpoint(epoch, acc, model, optimize)

        early_stopping(acc)
        if early_stopping.early_stop:
            print("Model doesn't optimize, so it will stop early!")
            break

    writer.close()

if __name__ == "__main__":
    args = argument()
    img_classifier(args)

