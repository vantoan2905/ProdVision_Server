import cv2
import numpy as np

class TextService:
    def warp_polys_to_patches(self, text_det):
        polys = text_det[0]["dt_polys"]
        img = text_det[0]["input_img"]

        warped = []

        for poly in polys:
            poly = np.array(poly, dtype=np.float32)

            xs, ys = poly[:,0], poly[:,1]
            x1, y1, x2, y2 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

            patch = img[y1:y2, x1:x2]

            warped.append({
                "patch": patch,
                "bbox": [x1, y1, x2, y2]
            })

        return warped

    def recognize(self, patches, text_rec_model):
        results = []

        for p in patches:
            out = text_rec_model.predict(p["patch"], batch_size=1)[0]
            results.append({
                "text": out["rec_text"],
                "score": out["rec_score"],
                "font": out["vis_font"],
                "bbox": p["bbox"]
            })

        return results
