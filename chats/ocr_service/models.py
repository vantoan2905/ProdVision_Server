import cv2
import numpy as np
import pandas as pd
import paddle
from paddleocr import LayoutDetection, TableCellsDetection, TextDetection, TextRecognition

# %% [markdown]
# # Models

# %%
class OCRModels:
    def __init__(self, device="gpu"):
        self.device = device
        self.layout_model = LayoutDetection(model_name="PP-DocLayoutV2")
        self.table_model = TableCellsDetection(model_name="RT-DETR-L_wired_table_cell_det")
        self.text_det_model = TextDetection(device=device, model_name="PP-OCRv5_server_det")
        self.text_rec_model = TextRecognition(device=device, model_name="PP-OCRv5_mobile_rec")
    
    def get_models(self):
        return self.layout_model, self.table_model, self.text_det_model, self.text_rec_model



