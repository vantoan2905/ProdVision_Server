from typing import List, Dict
import cv2
import numpy as np
from paddleocr import DocImgOrientationClassification




class DefectDetectionService:
    def __init__(self, languages: List[str] = ['en'], gpu: bool = True):
        self.languages = languages
        self.gpu = gpu

        self.blur_thresh = 120.0
        self.skew_thresh = 2.0
        self.orien_model = DocImgOrientationClassification(model_name="PP-LCNet_x1_0_doc_ori")
    # ------------------------
    # Orientation calssification
    # ------------------------

    def ocr_orientation_classification(self, img: np.ndarray) -> Dict:
        return self.orien_model.ocr_orientation_classification.predict(img)

    # =========================
    # SAT / NOISE CHECK
    # =========================
    def sat_noise_check(self, img, threshold=5, img_type="camera", lighting=None):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshold = max(1, min(int(threshold), 10))

        white_ratio = np.mean(gray >= 255 - threshold)
        black_ratio = np.mean(gray <= threshold)

        if lighting and (lighting["is_bad_dark"] or lighting["is_bad_light"]):
            is_noisy = False
            is_fixed = False
        elif img_type == "camera" and white_ratio + black_ratio > 0.3:
            is_noisy = False
            is_fixed = False
        else:
            if img_type == "camera":
                is_noisy = white_ratio > 0.02 or black_ratio > 0.04
            elif img_type == "scanner":
                is_noisy = white_ratio > 0.08 or black_ratio > 0.05
            elif img_type == "print":
                is_noisy = white_ratio > 0.95 or black_ratio > 0.05
            else:
                raise ValueError(f"Unknown img_type: {img_type}")

            is_fixed = is_noisy  

        return {
            "is_noisy": is_noisy,
            "white_ratio": float(white_ratio),
            "black_ratio": float(black_ratio),
            "is_fixed": is_fixed
        }


    # =========================
    # BLUR CHECK
    # =========================
    def blur_check(self, img: np.ndarray, lighting=None) -> Dict:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if lighting and lighting["is_bad_dark"]:
            return {
                "is_blurry": False,
                "blur_score": 0.0,
                "is_fixed": False
            }

        lap = cv2.Laplacian(gray, cv2.CV_64F)
        blur_score = lap.var()
        is_blurry = blur_score < self.blur_thresh

        return {
            "is_blurry": is_blurry,
            "blur_score": float(blur_score),
            "is_fixed": is_blurry  
        }


    # =========================
    # FLIP CHECK
    # =========================
    def flip_check(self, img: np.ndarray) -> Dict:
        h = img.shape[0]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        top = gray[:h // 2]
        bottom = gray[h // 2:]

        top_energy = cv2.Laplacian(top, cv2.CV_64F).var()
        bottom_energy = cv2.Laplacian(bottom, cv2.CV_64F).var()

        if top_energy < 5 and bottom_energy < 5:
            flipped = False
        else:
            flipped = bottom_energy > top_energy * 1.5

        return {
            "is_flipped": flipped,
            "top_energy": float(top_energy),
            "bottom_energy": float(bottom_energy),
            "is_fixed": flipped  
        }


    # =========================
    # SKEW CHECK
    # =========================
    def skew_check(self, img: np.ndarray) -> Dict:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        if lines is None or len(lines) < 5:
            return {
                "is_skewed": False,
                "skew_angle": 0.0,
                "is_fixed": False
            }

        angles = [(theta - np.pi / 2) * 180 / np.pi for rho, theta in lines[:, 0]]
        median_angle = float(np.median(angles))
        is_skewed = abs(median_angle) > self.skew_thresh

        return {
            "is_skewed": is_skewed,
            "skew_angle": median_angle,
            "is_fixed": is_skewed
        }


    # =========================
    # LIGHTING CHECK
    # =========================
    def lighting_check(self, img: np.ndarray, grid_size=3, img_type="camera") -> Dict:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        grid_size = max(1, min(grid_size, min(h, w)))
        cell_h, cell_w = h // grid_size, w // grid_size

        light_ratios = []
        dark_ratios = []

        for i in range(grid_size):
            for j in range(grid_size):
                y1 = i * cell_h
                y2 = h if i == grid_size - 1 else (i + 1) * cell_h
                x1 = j * cell_w
                x2 = w if j == grid_size - 1 else (j + 1) * cell_w

                cell = gray[y1:y2, x1:x2]
                light_ratios.append(np.mean(cell >= 250))
                dark_ratios.append(np.mean(cell <= 5))

        light_score = float(np.percentile(light_ratios, 90))
        dark_score = float(np.percentile(dark_ratios, 90))

        if img_type == "camera":
            light_thresh, dark_thresh = 0.02, 0.02
        elif img_type == "scanner":
            light_thresh, dark_thresh = 0.95, 0.1
        else:
            light_thresh, dark_thresh = 0.02, 0.02

        is_bad_light = light_score > light_thresh
        is_bad_dark = dark_score > dark_thresh

        return {
            "is_bad_light": is_bad_light,
            "is_bad_dark": is_bad_dark,
            "light_clipped_ratio": light_score,
            "dark_clipped_ratio": dark_score,
            "is_fixed": False  
        }


    # =========================
    # GLOBAL CHECK
    # =========================
    def check_defects(self, image: np.ndarray) -> Dict:
        ocr_orientation = self.ocr_orientation_classification(image)
        orientaion = ocr_orientation[0]["label_names"]
        
        lighting = self.lighting_check(image, img_type="scanner")

        report = {
            "orientation": orientaion,
            "lighting": lighting,
            "blur": self.blur_check(image, lighting),
            "sat_noise": self.sat_noise_check(
                image, threshold=5, img_type="print", lighting=lighting
            ),
            "flip": self.flip_check(image),
            "skew": self.skew_check(image),
        }

        defects = []
        fixable = []

        for name, result in report.items():
            if any(k.startswith("is_") and v for k, v in result.items()):
                defects.append(name)
                if result.get("is_fixed"):
                    fixable.append(name)

        report["defects"] = defects
        report["fixable_defects"] = fixable
        report["has_defect"] = len(defects) > 0

        return report
