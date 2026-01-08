
from typing import Dict, List, Any
import cv2
from PIL import Image
import numpy as np
import pandas as pd

class StructureAnalyzer:
    def __init__(self,
                    layout_model,
                    cell_det_model,
                    text_det_model,
                    text_rec_model):

        self.layout_model = layout_model
        self.cell_det_model = cell_det_model
        self.text_det_model = text_det_model
        self.text_rec_model = text_rec_model

    # ================= Layout =================
    def layout_analysis(self, img_path: str):
        return self.layout_model.predict(
            img_path,
            batch_size=1,
            layout_nms=True
        )

    def parse_layout_output(self, layout_output) -> List[Dict[str, Any]]:
        res = next(layout_output)

        results = []
        for item in res["boxes"]:
            results.append({
                "content_type": item["label"],
                "content_box": item["coordinate"],
                "content_score": item["score"],
                "content_cls_id": item["cls_id"],

  
            })
        return results

    # ================= Table Cell =================
    def cell_detection(self, patch, threshold: float = 0.3):
        return self.cell_det_model.predict(
            patch,
            threshold=threshold,
            batch_size=1
        )

    def parse_cell_output(self, cell_output) -> Dict[str, Any]:
        res = next(cell_output)
        content = res["boxes"]
        cells = []
        for box in content:
            cells.append({
                "box": box["coordinate"],
                "label": box["label"],
                "score": box["score"],
                "cls_id": box["cls_id"]
            })  
        return cells

    # ================= OCR =================
    def text_detection(self, img, threshold: float = 0.3):
        return self.text_det_model.predict(
            img,
            batch_size=1
        )

    def text_recognition(self, img, batch_size: int = 1):
        return self.text_rec_model.predict(
            img,
            batch_size=batch_size
        )
    def _crop_image(self, img_path: str, box: List[int]):
        img = Image.open(img_path).convert("RGB")
        img_np = np.array(img)
        x_min, y_min = int(box[0]), int(box[1])
        x_max, y_max = int(box[2]), int(box[3])
        cropped_img = img_np[y_min:y_max, x_min:x_max]
        return cropped_img
   
    def text_bbox_process(self, text_boxes: Dict) -> List[Dict]:
        polygons = text_boxes["dt_polys"]
        processed_boxes = []

        for poly in polygons:
            # poly shape: (4, 2)
            xs = poly[:, 0]
            ys = poly[:, 1]

            x_min = int(xs.min())
            y_min = int(ys.min())
            x_max = int(xs.max())
            y_max = int(ys.max())

            processed_boxes.append({
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max,
                "top_left": (x_min, y_min),
                "bottom_right": (x_max, y_max),
                "width": x_max - x_min,
                "height": y_max - y_min,
                "cx": (x_min + x_max) / 2,
                "cy": (y_min + y_max) / 2,
            })

        return processed_boxes
    def text_process(self, cropped_img, element) -> List[Dict[str, Any]]:
        text_det_output = self.text_detection(cropped_img, threshold=0.3)

        text_polygon = next(text_det_output)
        # print(text_boxes)
        text_boxes = self.text_bbox_process(text_polygon)
        rec_results = []
        for text_box in text_boxes:
            text_cropped_img = self.crop_bbox(cropped_img, text_box)
            rec_output = self.text_recognition(text_cropped_img)
            print (next(rec_output))
            rec_results.append(next(rec_output)[0])  # Assuming single result per crop

        element["ocr_results"] = rec_results
    def tabel_process(self, cropped_img, element) -> pd.DataFrame:
        cell_output = self.cell_detection(cropped_img)
        cell_result = self.parse_cell_output(cell_output)
        element["table_cells"] = cell_result
        # TODO: line detection and text recognition
    
    def crop_bbox(self, image: np.ndarray, box: Dict[str, int]) -> np.ndarray:
        return image[box["y_min"]:box["y_max"], box["x_min"]:box["x_max"]]
    # ================= Full Pipeline =================
    def full_analysis(self, img_path: str) -> Dict[str, Any]:
        # Layout Analysis -> return layout_result
        layout_output = self.layout_analysis(img_path)
        layout_result = self.parse_layout_output(layout_output)
        # loop in components layout_result type of table/text/title or v.v.
        for element in layout_result:
            box = element["content_box"]
            cropped_img = self._crop_image(img_path, box)
            # processs for each 
            if element["content_type"] == "table":

                self.tabel_process(cropped_img, element) 
            
         
            elif element["content_type"] in ["text", "title"]:
                self.text_process(cropped_img, element)
        return layout_result