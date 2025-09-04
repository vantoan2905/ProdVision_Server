import os
import pandas as pd
import numpy as np
import torchinfo as ti
import argparse
import yaml
from torch.utils.data import DataLoader

from faster_R_CNN.model import FasterRCNNTrainer
from provision.ai_models.data_loader.object_detection.load_data import LoadYoloData
#  TODO: if update new model import here


class Main:
    def __init__(self, args):
        self.args = args
        self.faster_rcnn_model_trainer = FasterRCNNTrainer(num_classes=args.numclass, mode=args.mode)

        # default dataset type
        if args.dataset == "yolo":
            self.train_image_path = os.path.join(args.data_path, "train/images")
            self.train_label_path = os.path.join(args.data_path, "train/labels")
            self.val_image_path = os.path.join(args.data_path, "val/images")
            self.val_label_path = os.path.join(args.data_path, "val/labels")
            self.yaml_path = os.path.join(args.data_path, "data.yaml")
        else:
            raise ValueError(f"Dataset {args.dataset} not supported yet.")

        # dataset + dataloader
        self.train_dataset = LoadYoloData(self.train_image_path, self.train_label_path, self.yaml_path)
        self.val_dataset = LoadYoloData(self.val_image_path, self.val_label_path, self.yaml_path)

        self.train_loader = DataLoader(
            self.train_dataset,
            batch_size=args.batch_size,
            shuffle=True,
            collate_fn=self.collate_fn
        )
        self.val_loader = DataLoader(
            self.val_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            collate_fn=self.collate_fn
        )

    def collate_fn(self, batch):
        return self.train_dataset.collate_fn(batch)

    def train(self):
        self.faster_rcnn_model_trainer.fit(self.train_loader, self.val_loader)

    def summary(self):
        if self.faster_rcnn_model_trainer.model is not None:
            ti.summary(self.faster_rcnn_model_trainer.model, input_size=(1, 3, 224, 224))
        else:
            print("No model found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None, help="Path to config file")

    args, unknown = parser.parse_known_args()

    if args.config:
        print(f"Using config file: {args.config}")
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
        for key, value in config.items():
            parser.add_argument(f"--{key}", type=type(value), default=value)
    else:
        parser.add_argument("--numclass", type=int, default=80, help="Number of classes")
        parser.add_argument("--mode", type=str, default="train", help="Mode (train/val/test)")
        parser.add_argument("--model", type=str, default="faster_rcnn", help="Model name")
        parser.add_argument("--dataset", type=str, default="yolo", help="Dataset name")
        parser.add_argument("--data_path", type=str, default="data/yolo", help="Path to dataset")
        parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
        parser.add_argument("--device", type=str, default="cuda", help="Device (cpu/cuda)")
        parser.add_argument("--batch_size", type=int, default=2, help="Batch size")
        parser.add_argument("--learning_rate", type=float, default=0.001, help="Learning rate")

    args = parser.parse_args()

    main = Main(args)
    main.summary()
