import cv2
from data_loader.load_yolo_data import  LoadYoloData
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

from faster_R_CNN import model
# def collate_fn(batch):
#     return tuple(zip(*batch))
# # ===============================
# # 1. Setup paths
# # ===============================
# from torch.utils.data import DataLoader

# train_images_path = r"D:\pcb_defect\ProdVision_django\PCB_DATASET_yolo_version\images\train"
# train_labels_path = r"D:\pcb_defect\ProdVision_django\PCB_DATASET_yolo_version\labels\train"
# val_images_path   = r"D:\pcb_defect\ProdVision_django\PCB_DATASET_yolo_version\images\val"
# val_labels_path   = r"D:\pcb_defect\ProdVision_django\PCB_DATASET_yolo_version\labels\val"
# yaml_path = r"D:\pcb_defect\ProdVision_django\PCB_DATASET_yolo_version\data.yaml"


# print("Loading training data...")
# train_dataset = LoadYoloData(train_images_path, train_labels_path, yaml_path)

# print("Loading validation data...")
# val_dataset = LoadYoloData(val_images_path, val_labels_path, yaml_path)




# # collate_fn cho object detection
# def collate_fn(batch):
#     return tuple(zip(*batch))

# train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=collate_fn)
# val_loader   = DataLoader(val_dataset, batch_size=2, shuffle=False, collate_fn=collate_fn)
# print("Train loader shape:", len(train_loader))
# print("Val loader shape:", len(val_loader))
# # Test load 1 batch
# images, targets = next(iter(train_loader))
# print("Batch image shape:", images[0].shape)
# print("Batch target example:", targets[0])



model = model.FasterRCNNTrainer(num_classes=2)

print("Model loaded:", model.build_model(num_classes=2))