import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import json
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

    # def build_model(self, num_classes):
    #     model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
    #     in_features = model.roi_heads.box_predictor.cls_score.in_features

    #     # thêm Dropout trước fully connected
    #     model.roi_heads.box_predictor = nn.Sequential(
    #         nn.Linear(in_features, in_features),
    #         nn.ReLU(),
    #         nn.Dropout(0.5),
    #         nn.Linear(in_features, num_classes),
    #     )
    #     return model

    def build_model(self, num_classes):
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictorWithDropout(in_features, num_classes, dropout=0.5)
        return model

    def train_one_epoch(self, data_loader, epoch):
        self.model.train()
        total_loss = 0.0
        loop = tqdm(data_loader, desc=f"Epoch [{epoch}] Train", leave=True)

        for images, targets in loop:
            images = [img.to(self.device) for img in images]
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            self.optimizer.zero_grad()
            losses.backward()
            self.optimizer.step()

            total_loss += losses.item()
            loop.set_postfix(loss=losses.item())

        return total_loss / len(data_loader)

    @torch.no_grad()
    def evaluate(self, data_loader, epoch):
        self.model.train()  # cần thiết để trả về loss_dict
        total_loss = 0.0
        loop = tqdm(data_loader, desc=f"Epoch [{epoch}] Val", leave=True)

        for images, targets in loop:
            images = [img.to(self.device) for img in images]
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            total_loss += losses.item()
            loop.set_postfix(val_loss=losses.item())

        return total_loss / len(data_loader)

    def fit(self, train_loader, val_loader=None, num_epochs=10):
        for epoch in range(1, num_epochs + 1):
            train_loss = self.train_one_epoch(train_loader, epoch)
            self.history["train"].append(train_loss)
            print(f"Epoch {epoch}: Train Loss = {train_loss:.4f}")

            if val_loader is not None:
                val_loss = self.evaluate(val_loader, epoch)
                self.history["val"].append(val_loss)
                print(f"Epoch {epoch}: Val Loss = {val_loss:.4f}")

                if val_loss < self.best_loss:
                    self.best_loss = val_loss
                    torch.save(self.model.state_dict(), self.save_path)
                    print(f"✅ Saved best model at {self.save_path}")
                    self.counter = 0
                else:
                    self.counter += 1
                    if self.counter >= self.patience:
                        print("⏹ Early stopping triggered")
                        break

            self.lr_scheduler.step()

        self.plot_history()

    def plot_history(self):
        plt.figure(figsize=(8, 6))
        sns.set_style("whitegrid")
        plt.plot(self.history["train"], label="Train Loss")
        if self.history["val"]:
            plt.plot(self.history["val"], label="Val Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training & Validation Loss")
        plt.legend()
        plt.tight_layout()

        plot_path = os.path.join(self.run_dir, "loss_curve.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"📊 Saved loss curve at {plot_path}")



    def save(self, path=None):
        torch.save(self.model.state_dict(), path or self.save_path)

    def load(self, path=None):
        self.model.load_state_dict(torch.load(path or self.save_path, map_location=self.device))

    def get_model(self):
        return self.model
    
    def draw_box(self, image, boxes, labels=None, save_path=None, colors_bbox="red", colors_text="yellow"):
        plt.figure(figsize=(10, 10))
        plt.imshow(image.permute(1, 2, 0).cpu().numpy())
        ax = plt.gca()

        for i, box in enumerate(boxes):
            xmin, ymin, xmax, ymax = box
            rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                 fill=False, color=colors_bbox, linewidth=2)
            ax.add_patch(rect)
            if labels is not None:
                ax.text(xmin, ymin, f'{labels[i]}', fontsize=12,
                        bbox=dict(facecolor=colors_text, alpha=0.5))

        if save_path is not None:
            plt.savefig(save_path)
        plt.close()
    def save_predicted_bbox(self, name, boxes, labels=None, save_path=None):
        with open(save_path or f"{name}_predicted_bboxes.json", "w") as f:
            json.dump({"boxes": boxes, "labels": labels}, f)


    def predict_one_image(self, image, threshold=0.5, save_path=None):
        self.model.eval()
        with torch.no_grad():
            image = image.to(self.device)
            outputs = self.model([image])[0]

        keep = outputs['scores'] >= threshold
        filtered_outputs = {k: v[keep].cpu() for k, v in outputs.items()}
        # draw bounding boxes
        self.draw_box(image, filtered_outputs['boxes'], filtered_outputs['labels'], save_path=save_path)
        # save predicted bounding boxes
        if save_path:
            name = os.path.splitext(os.path.basename(save_path))[0]
            self.save_predicted_bbox(name, filtered_outputs['boxes'].tolist(),
                                     filtered_outputs['labels'].tolist(),
                                     save_path=os.path.join(os.path.dirname(save_path), f"{name}_predicted_bboxes.json"))
        return filtered_outputs
    
    def predict_many_images(self, images, threshold=0.5, save_dir=None):
        for i, image in enumerate(images):
            save_path = os.path.join(save_dir, f"image_{i}.png") if save_dir else None
            yield self.predict_one_image(image, threshold, save_path=save_path)


# num_classes = 2  # background + object
# trainer = FasterRCNNTrainer(num_classes, run_name="exp1")
# trainer.fit(train_loader, val_loader, num_epochs=10)
