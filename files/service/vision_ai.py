import easyocr
import cv2
import numpy as np
import os
import uuid
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
import tqdm


class VisionAIPipeline:
    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}

    def __init__(self, languages: Optional[List[str]] = None, gpu: bool = True):
        self.languages = languages or ['en']
        try:
            self.reader = easyocr.Reader(self.languages, gpu=gpu)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EasyOCR reader: {e}")

    # --- Folder processing ---
    def process_folder(self, folder_path: str, generate_lines: bool = True) -> List[Dict]:
        folder_path = Path(folder_path)
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        image_files = [f for f in folder_path.iterdir() if f.suffix.lower() in self.SUPPORTED_EXTENSIONS]
        results = []
        for file_path in tqdm.tqdm(image_files, desc="Processing images"):
            try:
                results.append(self._process_single_image(file_path, generate_lines, file_path.name))
            except Exception:
                continue
        return results

    # --- Single image processing ---
    def process_single_image(self, image: Union[str, Path, np.ndarray], generate_lines: bool = True, file_name: str = "") -> Dict:
        return self._process_single_image(image, generate_lines, file_name)

    def _process_single_image(self, image: Union[str, Path, np.ndarray], generate_lines: bool, file_name: str) -> Dict:
        ocr_items = self._read_image(image)
        full_text_data, line_texts = self._ocr_to_full_text(ocr_items, return_lines=generate_lines)
        return {
            "id": str(uuid.uuid4()),
            "file_path": str(image),
            "file_name": file_name,
            "text": full_text_data["text"],
            "lines": line_texts,
            "word_count": len(full_text_data["text"].split()),
            "embedding": [],
            "metadata": full_text_data["metadata"]
        }

    # --- Image reading & OCR ---
    def _read_image(self, image: Union[str, Path, np.ndarray]) -> List[Tuple]:
        if isinstance(image, (str, Path)) and os.path.isfile(image):
            img = cv2.imread(str(image))
            if img is None:
                raise ValueError(f"Could not read image: {image}")
            image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return self.reader.readtext(image_rgb)
        elif isinstance(image, np.ndarray):
            return self.reader.readtext(image)
        else:
            raise ValueError(f"Invalid image input: {image}")

    # --- OCR post-processing ---
    def _ocr_to_full_text(self, ocr_items: List[Tuple], line_threshold: int = 10, return_lines: bool = True) -> Tuple[Dict, List[str]]:
        if not ocr_items:
            empty_metadata = {"avg_bbox": None, "avg_confidence": None, "total_words": 0, "total_lines": 0}
            return {"text": "", "metadata": empty_metadata}, []

        ocr_items.sort(key=lambda x: x[0][0][1])
        lines = self._group_into_lines(ocr_items, line_threshold)
        for line in lines:
            line.sort(key=lambda x: x[0][0][0])

        full_text = " ".join(text for line in lines for _, text, _ in line)
        line_texts = [" ".join(text for _, text, _ in line) for line in lines] if return_lines else []
        metadata = self._calculate_metadata(lines, ocr_items)
        return {"text": full_text, "metadata": metadata}, line_texts

    def _group_into_lines(self, ocr_items: List[Tuple], line_threshold: int) -> List[List[Tuple]]:
        lines = []
        current_line = []
        current_y = None
        for bbox, text, conf in ocr_items:
            y_top = bbox[0][1]
            if current_y is None or abs(y_top - current_y) < line_threshold:
                current_line.append((bbox, text, conf))
                current_y = y_top
            else:
                lines.append(current_line)
                current_line = [(bbox, text, conf)]
                current_y = y_top
        if current_line:
            lines.append(current_line)
        return lines

    def _calculate_metadata(self, lines: List[List[Tuple]], ocr_items: List[Tuple]) -> Dict:
        all_bboxes = [bbox for line in lines for bbox, _, _ in line]
        all_confidences = [conf for line in lines for _, _, conf in line]
        return {
            "avg_bbox": np.mean(np.array(all_bboxes), axis=0).tolist() if all_bboxes else None,
            "avg_confidence": float(np.mean(all_confidences)) if all_confidences else None,
            "min_confidence": float(min(all_confidences)) if all_confidences else None,
            "max_confidence": float(max(all_confidences)) if all_confidences else None,
            "total_words": len(ocr_items),
            "total_lines": len(lines)
        }
