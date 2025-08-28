import torch
import torch.optim as optim
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import seaborn as sns


class FasterRCNNTrainer:
    def __init__(self, num_classes, device="cuda", run_name="run1"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = self.build_model(num_classes).to(self.device)
        self.optimizer = optim.SGD(
            self.model.parameters(),
            lr=0.005,
            momentum=0.9,
            weight_decay=0.0005
        )
        self.lr_scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=3, gamma=0.1)

        # setup folder run
        self.run_dir = os.path.join("run", run_name)
        os.makedirs(self.run_dir, exist_ok=True)

        self.save_path = os.path.join(self.run_dir, "best_model.pth")
        self.best_loss = float("inf")

        self.history = {"train": [], "val": []}

    def build_model(self, num_classes):
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
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

    # @torch.no_grad()
    # def evaluate(self, data_loader, epoch):
    #     self.model.eval()
    #     total_loss = 0.0
    #     loop = tqdm(data_loader, desc=f"Epoch [{epoch}] Val", leave=True)

    #     for images, targets in loop:
    #         images = [img.to(self.device) for img in images]
    #         targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

    #         loss_dict = self.model(images, targets)
    #         losses = sum(loss for loss in loss_dict.values())
    #         total_loss += losses.item()
    #         loop.set_postfix(val_loss=losses.item())

    #     return total_loss / len(data_loader)
    # @torch.no_grad()
    # def evaluate(self, data_loader, epoch):
    #     self.model.eval()
    #     results = []
    #     for images, _ in data_loader:
    #         images = [img.to(self.device) for img in images]
    #         outputs = self.model(images)   # list prediction
    #         results.extend(outputs)
    #     return results  
    @torch.no_grad()
    def evaluate(self, data_loader, epoch):
        self.model.train()   # 👈 bắt buộc để trả về loss_dict
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

            val_loss = None
            if val_loader is not None:
                val_loss = self.evaluate(val_loader, epoch)
                self.history["val"].append(val_loss)
                print(f"Epoch {epoch}: Val Loss = {val_loss:.4f}")

                if val_loss < self.best_loss:
                    self.best_loss = val_loss
                    torch.save(self.model.state_dict(), self.save_path)
                    print(f"✅ Saved best model at {self.save_path}")

            self.lr_scheduler.step()

        self.plot_losses()

    def plot_losses(self):
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

    def predict(self, image):
        self.model.eval()
        with torch.no_grad():
            image = image.to(self.device)
            output = self.model([image])
        return output

    def save(self, path=None):
        torch.save(self.model.state_dict(), path or self.save_path)

    def load(self, path=None):
        self.model.load_state_dict(torch.load(path or self.save_path, map_location=self.device))



# num_classes = 2  # background + object
# trainer = FasterRCNNTrainer(num_classes, run_name="exp1")
# trainer.fit(train_loader, val_loader, num_epochs=10)
