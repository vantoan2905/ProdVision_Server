import cv2
import numpy as np
import yaml
import torch
from pathlib import Path
from torch.utils.data import Dataset


class LoadYoloData(Dataset):
    def __init__(self, img_dir, label_dir, yaml_dir, transforms=None, to_tensor=True):
        self.img_dir = Path(img_dir)
        self.label_dir = Path(label_dir)
        self.yaml_dir = Path(yaml_dir)
        self.transforms = transforms
        self.to_tensor = to_tensor

        self.images = sorted(list(self.img_dir.glob("*.jpg")) + list(self.img_dir.glob("*.png")))

        with open(self.yaml_dir, "r") as f:
            yaml_content = yaml.safe_load(f)
        self.class_dict = yaml_content.get("names", {})

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        label_path = self.label_dir / f"{img_path.stem}.txt"

        image = cv2.imread(str(img_path))
        if image is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]

        boxes, labels = [], []
        if label_path.exists():
            with open(label_path, "r") as f:
                for line in f.readlines():
                    class_id, x_center, y_center, bw, bh = map(float, line.strip().split())

                    x_center *= w
                    y_center *= h
                    bw *= w
                    bh *= h

                    xmin = x_center - bw / 2
                    ymin = y_center - bh / 2
                    xmax = x_center + bw / 2
                    ymax = y_center + bh / 2

                    boxes.append([xmin, ymin, xmax, ymax])
                    labels.append(int(class_id) + 1) 

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        target = {"boxes": boxes, "labels": labels}

        if self.to_tensor:
            image = torch.as_tensor(image / 255.0, dtype=torch.float32).permute(2, 0, 1)

        if self.transforms:
            image, target = self.transforms(image, target)

        return image, target

    @staticmethod
    def collate_fn(batch):
        return tuple(zip(*batch))
