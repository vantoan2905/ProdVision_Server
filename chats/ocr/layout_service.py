import cv2

class LayoutService:
    def extract_patches(self, layout_result, img_path):
        img = cv2.imread(img_path)
        boxes = layout_result[0]["boxes"]

        patches = []

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box["coordinate"])

            patches.append({
                "patch_id": i,
                "patch_label": box["label"],
                "patch_position": [x1, y1, x2, y2],
                "patch_score": box["score"],
                "patch": img[y1:y2, x1:x2]
            })

        return patches
