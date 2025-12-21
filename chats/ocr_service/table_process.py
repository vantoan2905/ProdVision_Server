import numpy as np
import pandas as pd
# %%
class TableProcessor:

    @staticmethod
    def poly_to_bbox(poly):
        poly = np.array(poly)
        x_min = np.min(poly[:, 0])
        y_min = np.min(poly[:, 1])
        x_max = np.max(poly[:, 0])
        y_max = np.max(poly[:, 1])
        return x_min, y_min, x_max, y_max

    @staticmethod
    def extract_table_text_from_patch(table_patch, table_model, text_det_model, text_rec_model):
        result = []
        cells = table_model.predict(table_patch)

        for cell in cells[0]["boxes"]:
            x_min, y_min, x_max, y_max = map(int, cell["coordinate"])
            patch = table_patch[y_min:y_max, x_min:x_max]

            line_text_det = text_det_model.predict(patch)
            polys = line_text_det[0]["dt_polys"]
            line_img = line_text_det[0]["input_img"]

            for poly in polys:
                bbox = TableProcessor.poly_to_bbox(poly)
                x_min_l, y_min_l, x_max_l, y_max_l = map(int, bbox)
                line_patch = line_img[y_min_l:y_max_l, x_min_l:x_max_l]
                text_info = text_rec_model.predict(line_patch)[0]
                result.append({
                    "cell_bbox": [x_min, y_min, x_max, y_max],
                    "text": text_info["rec_text"],
                    "score": text_info["rec_score"],
                    "front": text_info["vis_font"]
                })

        return result

    @staticmethod
    def reconstruct_table_from_result(result, y_threshold=5):
        cells = [(tuple(item["cell_bbox"]), item["text"]) for item in result]
        cells.sort(key=lambda x: (x[0][1], x[0][0]))

        table = []
        current_row = []
        current_y_min = None

        for bbox, text in cells:
            x_min, y_min, x_max, y_max = bbox
            if current_y_min is None:
                current_y_min = y_min
            if y_min - current_y_min > y_threshold:
                table.append(current_row)
                current_row = []
                current_y_min = y_min
            current_row.append((x_min, text))
        if current_row:
            table.append(current_row)

        table_2d = []
        for row in table:
            row_sorted = [text for x, text in sorted(row, key=lambda x: x[0])]
            table_2d.append(row_sorted)
        return table_2d

    @staticmethod
    def table_2d_to_df(table_2d):
        max_cols = max(len(row) for row in table_2d)
        normalized_table = [row + [""]*(max_cols - len(row)) for row in table_2d]
        return pd.DataFrame(normalized_table)

    @staticmethod
    def df_to_list_of_dict(df):
        return df.to_dict(orient="records")
