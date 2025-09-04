import os
import json
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns


class FastRCNNPredictorWithDropout(nn.Module):
    def __init__(self, in_channels, num_classes, dropout=0.5):
        super().__init__()
        self.cls_score = nn.Sequential(
            nn.Linear(in_channels, in_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(in_channels, num_classes),
        )
        self.bbox_pred = nn.Linear(in_channels, num_classes * 4)

    def forward(self, x):
        if x.dim() == 4:  # (N, C, 1, 1) -> (N, C)
            x = torch.flatten(x, start_dim=1)
        scores = self.cls_score(x)
        bbox_deltas = self.bbox_pred(x)
        return scores, bbox_deltas


class FasterRCNNTrainer:
    def __init__(self, num_classes, device="cuda", run_name="run1", patience=5):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = self.build_model(num_classes).to(self.device)

        self.optimizer = optim.SGD(
            self.model.parameters(),
            lr=0.005,
            momentum=0.9,
            weight_decay=0.0005,   # L2 regularization
        )
        self.lr_scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=3, gamma=0.1)

        self.run_dir = os.path.join("run", run_name)
        os.makedirs(self.run_dir, exist_ok=True)

        self.save_path = os.path.join(self.run_dir, "best_model.pth")
        self.best_loss = float("inf")
        self.history = {"train": [], "val": []}

        # Early Stopping
        self.patience = patience
        self.counter = 0

    def build_model(self, num_classes):
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictorWithDropout(in_features, num_classes, dropout=0.5)
        return model

    def train_one_epoch(self, data_loader):
        self.model.train()
        running_loss = 0.0
        for images, targets in tqdm(data_loader, desc="Training", leave=False):
            images = list(image.to(self.device) for image in images)
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            running_loss += losses.item()

            self.optimizer.zero_grad()
            losses.backward()
            self.optimizer.step()

        epoch_loss = running_loss / len(data_loader)
        return epoch_loss

    @torch.no_grad()
    def validate(self, data_loader):
        self.model.train()   # phải ở chế độ train để trả về loss
        running_loss = 0.0
        for images, targets in tqdm(data_loader, desc="Validation", leave=False):
            images = list(image.to(self.device) for image in images)
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            running_loss += losses.item()

        epoch_loss = running_loss / len(data_loader)
        return epoch_loss

    def fit(self, train_loader, val_loader, epochs=10):
        for epoch in range(1, epochs + 1):
            train_loss = self.train_one_epoch(train_loader)
            val_loss = self.validate(val_loader)
            self.lr_scheduler.step()

            self.history["train"].append(train_loss)
            self.history["val"].append(val_loss)

            print(f"Epoch [{epoch}/{epochs}] - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

            # Save best model
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                torch.save(self.model.state_dict(), self.save_path)
                print(f"✅ Best model saved with val loss: {self.best_loss:.4f}")
                self.counter = 0
            else:
                self.counter += 1
                if self.counter >= self.patience:
                    print("⏹️ Early stopping triggered")
                    break

    def plot_history(self):
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=range(1, len(self.history["train"]) + 1), y=self.history["train"], label="Train Loss")
        sns.lineplot(x=range(1, len(self.history["val"]) + 1), y=self.history["val"], label="Val Loss")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.title("Training and Validation Loss")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(self.run_dir, "loss_curve.png"))
        plt.show()

        with open(os.path.join(self.run_dir, "history.json"), "w") as f:
            json.dump(self.history, f)

    def save(self, path=None):
        if path is None:
            path = self.save_path
        torch.save(self.model.state_dict(), path)
        print(f"💾 Model saved to {path}")

    def load(self, path):
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.to(self.device)
        print(f"📂 Model loaded from {path}")

    def get_model(self):
        return self.model

    def save_predicted_bbox(self, name, boxes, labels, save_path):
        data = {"name": name, "boxes": boxes, "labels": labels}
        with open(save_path, "w") as f:
            json.dump(data, f)

    def draw_boxes(self, image, boxes, labels, colors=None, thickness=2, font_scale=0.5, save_path=None):
        if colors is None:
            colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]  # mặc định 3 màu

        img = image.clone().permute(1, 2, 0).cpu().numpy()
        img = (img * 255).astype("uint8")

        for box, label in zip(boxes, labels):
            color = colors[label % len(colors)]
            x1, y1, x2, y2 = box
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
            cv2.putText(img, str(label), (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

        plt.imshow(img)
        plt.axis("off")
        if save_path:
            plt.savefig(save_path)
            print(f"📷 Image with boxes saved to {save_path}")
        plt.show()

    def predict_one_image(self, image, threshold=0.5, save_path=None):
        self.model.eval()
        with torch.no_grad():
            image = image.to(self.device)
            outputs = self.model([image])[0]

        keep = outputs['scores'] >= threshold
        filtered_outputs = {k: v[keep].cpu() for k, v in outputs.items()}

        self.draw_boxes(image, filtered_outputs['boxes'], filtered_outputs['labels'], save_path=save_path)

        if save_path:
            name = os.path.splitext(os.path.basename(save_path))[0]
            self.save_predicted_bbox(
                name,
                filtered_outputs['boxes'].tolist(),
                filtered_outputs['labels'].tolist(),
                save_path=os.path.join(os.path.dirname(save_path), f"{name}_predicted_bboxes.json")
            )

        return filtered_outputs

    def predict_many_images(self, images, threshold=0.5, save_dir=None):
        for i, image in enumerate(images):
            save_path = os.path.join(save_dir, f"image_{i}.png") if save_dir else None
            yield self.predict_one_image(image, threshold, save_path=save_path)
