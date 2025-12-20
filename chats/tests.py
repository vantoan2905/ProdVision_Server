from paddleocr import LayoutDetection, TableCellsDetection, TextDetection, TextRecognition
import cv2
import numpy as np
import pandas as pd

class OCRService():
    def __init__(self):
        self.layout_model = LayoutDetection(device="gpu", model_name="PP-DocLayoutV2")
        self.table_model = TableCellsDetection(device="gpu", model_name="RT-DETR-L_wired_table_cell_det")
        self.text_det_model = TextDetection(device="gpu",model_name="PP-OCRv5_server_det")
        self.text_rec_model = TextRecognition(device="gpu", model_name="PP-OCRv5_mobile_rec")


        
    def extract_patches(self, layout, img_path):

        img = cv2.imread(img_path)
        data = layout[0]["boxes"]

        # Tạo tất cả patch
        patches = [{
            "patch_id": i,
            "patch_label": bbox["label"],
            "patch_positition": [int(c) for c in bbox["coordinate"]],
            "patch_score": bbox["score"],
            "patch": img[int(bbox["coordinate"][1]):int(bbox["coordinate"][3]),
                        int(bbox["coordinate"][0]):int(bbox["coordinate"][2])]
        } for i, bbox in enumerate(data)]

        # Hàm merge các patch text liên tiếp
        def merge_text_patches(patch_group):
            xs = [x for p in patch_group for x in (p["patch_positition"][0], p["patch_positition"][2])]
            ys = [y for p in patch_group for y in (p["patch_positition"][1], p["patch_positition"][3])]
            scores = [p["patch_score"] for p in patch_group]

            new_position = [min(xs), min(ys), max(xs), max(ys)]
            x1, y1, x2, y2 = map(int, new_position)
            merged_patch = img[y1:y2, x1:x2]

            return {
                "patch_id": patch_group[0]["patch_id"],
                "patch_label": "text",
                "patch_positition": new_position,
                "patch_score": max(scores),
                "patch": merged_patch
            }

        # Merge patch text liên tiếp
        finally_patches = []
        temp_patches = []

        for patch in patches:
            if patch["patch_label"] == "text":
                temp_patches.append(patch)
            else:
                if temp_patches:
                    finally_patches.append(merge_text_patches(temp_patches))
                    temp_patches = []
                finally_patches.append(patch)

        if temp_patches:
            finally_patches.append(merge_text_patches(temp_patches))

        return finally_patches
    

    def warp_polys_to_patches(self, text_det):
        """
        Từ kết quả text detection, sort polygon theo trục y, warp từng polygon thành patch chữ nhật.
        
        Args:
            text_det: output của text_det_model.predict, dạng list/dict như text_det[0]
        
        Returns:
            warped_patches: list các dict, mỗi dict gồm:
                - 'patch': patch ảnh đã warp
                - 'bboxes': bbox trong patch
                - 'poly': polygon sau warp (int)
        """
        list_poly = text_det[0]["dt_polys"]
        img_input = text_det[0]["input_img"]

        centers_y = np.array([np.mean(np.array(poly)[:,1]) for poly in list_poly])
        sorted_idx = np.argsort(centers_y)
        list_poly_sorted = [list_poly[i] for i in sorted_idx]

        warped_patches = []

        for poly in list_poly_sorted:
            poly = np.array(poly, dtype=np.float32)

            if len(poly) > 4:
                hull = cv2.convexHull(poly).squeeze()
                src_pts = hull[:4] if hull.shape[0] >= 4 else hull
            else:
                src_pts = poly

            while src_pts.shape[0] < 4:
                src_pts = np.vstack([src_pts, src_pts[-1]])

            min_x, min_y = src_pts.min(axis=0)
            max_x, max_y = src_pts.max(axis=0)
            width = int(max_x - min_x)
            height = int(max_y - min_y)
            dst_pts = np.array([[0,0],[width-1,0],[width-1,height-1],[0,height-1]], dtype=np.float32)

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img_input, M, (width, height))

            poly_warped = cv2.perspectiveTransform(src_pts.reshape(-1,1,2), M).reshape(-1,2)
            min_x_w, min_y_w = poly_warped.min(axis=0)
            max_x_w, max_y_w = poly_warped.max(axis=0)
            bbox = [int(min_x_w), int(min_y_w), int(max_x_w), int(max_y_w)]

            warped_patches.append({
                "patch": warped,
                "bboxes": bbox,
                "poly": poly_warped.astype(int)
            })

        return warped_patches
    def recognize_text_from_patches(self, warped_patches, text_rec_model, batch_size=1):
        """
        Duyệt qua danh sách patch, predict text và trả về list dict gồm text, bbox, score, font.

        Args:
            warped_patches: list các dict, mỗi dict gồm 'patch', 'bboxes', 'poly'
            text_rec_model: model nhận dạng text
            batch_size: batch size khi predict

        Returns:
            text_patch: list dict, mỗi dict gồm 'text', 'bbox', 'score', 'front'
        """
        text_patch = []

        for patch_dict in warped_patches:
            img = patch_dict['patch']
            text_lines = text_rec_model.predict(img, batch_size=batch_size)

            result = {
                "text": text_lines[0]["rec_text"],
                "bbox": patch_dict['bboxes'],
                "score": text_lines[0]["rec_score"],
                "front": text_lines[0]["vis_font"]
            }

            text_patch.append(result)

        return text_patch
        
    def detect_cells(self, img, table_det_model):
        result = table_det_model.predict(img, batch_size=1)
        cells = []

        bboxes = result[0]["boxes"]

        for poly in bboxes:
            x1, y1, x2, y2 = map(int, poly["coordinate"])

            cells.append({
                "bbox": [x1, y1, x2, y2],
                "label": poly.get("label", "cell"),
                "score": poly.get("score", 1.0)
            })

        return cells


    def expand_bbox(self,bbox, img_shape, overlap_ratio=0.1):
        x1, y1, x2, y2 = bbox
        h, w = img_shape[:2]

        bw = x2 - x1
        bh = y2 - y1

        dx = int(bw * overlap_ratio)
        dy = int(bh * overlap_ratio)

        nx1 = max(0, x1 - dx)
        ny1 = max(0, y1 - dy)
        nx2 = min(w, x2 + dx)
        ny2 = min(h, y2 + dy)

        return nx1, ny1, nx2, ny2


    def recog_and_sort_cells(
        self,
        img,
        cells,
        text_det_model,
        text_rec_model,
        y_thresh_ratio=0.5
    ):
        cells_ = []

        for cell in cells:
            x1, y1, x2, y2 = self.expand_bbox(
                cell["bbox"],
                img.shape,
                overlap_ratio=0.15
            )

            patch = img[y1:y2, x1:x2]
            if patch.size == 0:
                continue

            text_det = text_det_model.predict(patch, batch_size=1)
            polys = text_det[0].get("dt_polys", [])
            for poly in polys:

                # poly: [[x,y], [x,y], ...]
                xs = [p[0] for p in poly]
                ys = [p[1] for p in poly]

                px1, py1 = max(0, min(xs)), max(0, min(ys))
                px2, py2 = min(patch.shape[1], max(xs)), min(patch.shape[0], max(ys))

                if px2 <= px1 or py2 <= py1:
                    text = ""
                    score = 0.0
                    font = None
                else:
                    img_patch = patch[py1:py2, px1:px2]

                    text_dict = text_rec_model.predict(img_patch)
                    text = text_dict[0].get("rec_text", "")
                    score = text_dict[0].get("rec_score", 0.0)
                    font = text_dict[0].get("vis_font", None)

                cells_.append({
                    "bbox": cell["bbox"],
                    "text": text,
                    "score": score,
                    "font": font,
                    "cx": (x1 + x2) / 2,
                    "cy": (y1 + y2) / 2,
                    "h": y2 - y1
                })

        if not cells_:
            return []

        # sort theo trục y
        cells_.sort(key=lambda x: x["cy"])

        rows = []
        current_row = []
        y_thresh = np.mean([c["h"] for c in cells_]) * y_thresh_ratio

        for cell in cells_:
            if not current_row:
                current_row.append(cell)
            elif abs(cell["cy"] - current_row[-1]["cy"]) <= y_thresh:
                current_row.append(cell)
            else:
                rows.append(current_row)
                current_row = [cell]

        if current_row:
            rows.append(current_row)

        # sort từng row theo x
        for row in rows:
            row.sort(key=lambda x: x["cx"])

        return rows


    def extract_table_fast(self,img, table_det_model, text_det_model, text_rec_model):
        cells = self.detect_cells(img, table_det_model)
        rows = self.recog_and_sort_cells(
            img,
            cells,
            text_det_model,
            text_rec_model
        )

        table = []
        for row in rows:
            table.append([cell["text"] for cell in row])

        return pd.DataFrame(table)


    def df_to_json(self, df, orient="records", indent=2):
        """
        orient:
            - records  : [{col: val, ...}, ...]
            - split    : {index, columns, data}
            - table    : Table Schema
            - values   : [[...], [...]]
        """
        return df.to_json(
            orient=orient,
            force_ascii=False,
            indent=indent
        )
    def process_document(
        self,
        img_path,
        layout_model,
        text_det_model,
        text_rec_model,
        table_model
    ):

        # 1. Layout detection
        layout_result = layout_model.predict(
            img_path,
            batch_size=1,
            layout_nms=True
        )

        # 2. Merge layout patches
        merged_patches = self.extract_patches(layout_result, img_path)

        document_paragraphs = []

        for patch_info in merged_patches:
            patch_img = patch_info["patch"]
            patch_idx = patch_info["patch_id"]
            patch_type = patch_info["patch_label"]
            patch_coords = patch_info["patch_positition"]
            patch_conf = patch_info["patch_score"]

            # 3. Process by patch type
            if patch_type == "table":
                table_result = self.extract_table_fast(
                    img=patch_img,
                    table_det_model=table_model,
                    text_det_model = text_det_model,
                    text_rec_model=text_rec_model
                )

                recognized_text = self.df_to_json(table_result)
            else:
                det_result = text_det_model.predict(
                    patch_img,
                    batch_size=1
                )

                rectified_patches = self.warp_polys_to_patches(
                    det_result
                )

                recognized_text = self.recognize_text_from_patches(
                    rectified_patches,
                    text_rec_model
                )

            paragraph_entry = {
                "patch_id": patch_idx,
                "patch_label": patch_type,
                "patch_position": patch_coords,
                "patch_score": patch_conf,
                "text_dict": recognized_text
            }

            document_paragraphs.append(paragraph_entry)

        return document_paragraphs
    




img_path = "/media/tom/Code/pcb_defect/ProdVision_Server/media/data_test/1507.05717v1_page-0005.jpg"

document_paragraphs = process_document(
    img_path=img_path,
    layout_model=layout_model,
    text_det_model=text_det_model,
    text_rec_model=text_rec_model,
    table_model=table_model
)
