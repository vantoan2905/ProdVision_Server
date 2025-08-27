import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN
from torchvision.ops import MultiScaleRoIAlign


class FasterRCNNTrainer:
    def __init__(self, num_classes, device="cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = self.build_model(num_classes).to(self.device)
        self.optimizer = optim.SGD(
            self.model.parameters(),
            lr=0.005,
            momentum=0.9,
            weight_decay=0.0005
        )
        self.lr_scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=3, gamma=0.1)

    def build_model(self, num_classes):
        # Load pretrained model
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        return model

    def train_one_epoch(self, data_loader, epoch, print_freq=10):
        self.model.train()
        total_loss = 0.0

        for i, (images, targets) in enumerate(data_loader):
            images = [img.to(self.device) for img in images]
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            self.optimizer.zero_grad()
            losses.backward()
            self.optimizer.step()

            total_loss += losses.item()
            if i % print_freq == 0:
                print(f"Epoch [{epoch}] Iter [{i}/{len(data_loader)}] Loss: {losses.item():.4f}")

        return total_loss / len(data_loader)

    @torch.no_grad()
    def evaluate(self, data_loader):
        self.model.eval()
        results = []
        for images, targets in data_loader:
            images = [img.to(self.device) for img in images]
            outputs = self.model(images)
            results.extend(outputs)
        return results

    def fit(self, train_loader, val_loader=None, num_epochs=10):
        for epoch in range(num_epochs):
            loss = self.train_one_epoch(train_loader, epoch)
            print(f"Epoch [{epoch}] Avg Loss: {loss:.4f}")

            self.lr_scheduler.step()

            if val_loader is not None:
                outputs = self.evaluate(val_loader)
                print(f"Validation samples: {len(outputs)}")


# ============================
# Ví dụ cách dùng:
# ============================
# num_classes = 2  # background + object
# trainer = FasterRCNNTrainer(num_classes)
# trainer.fit(train_loader, val_loader, num_epochs=10)
