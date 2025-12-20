import numpy as np
import pandas as pd

class TableService:
    def detect_cells(self, img, table_model):
        result = table_model.predict(img, batch_size=1)
        cells = []

        for b in result[0]["boxes"]:
            cells.append({
                "bbox": list(map(int, b["coordinate"])),
                "score": b.get("score", 1.0)
            })

        return cells

    def extract_table(self, img, cells, text_det, text_rec):
        table = []

        for cell in cells:
            x1, y1, x2, y2 = cell["bbox"]
            patch = img[y1:y2, x1:x2]

            det = text_det.predict(patch, batch_size=1)
            polys = det[0]["dt_polys"]
            for poly in polys:

                xs = [p[0] for p in poly]
                ys = [p[1] for p in poly]

                patch = patch[min(ys):max(ys), min(xs):max(xs)]
                text = text_rec.predict(patch)[0]["rec_text"]
                table.append(text)

        return pd.DataFrame([table])
