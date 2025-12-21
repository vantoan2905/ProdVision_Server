import cv2 
import numpy as np 




class PatchUtils:
    
    @staticmethod
    def extract_patches(layout, img_path):
        img = cv2.imread(img_path)
        data = layout[0]["boxes"]
        
        patches = [{
            "patch_id": i,
            "patch_label": bbox["label"],
            "patch_positition": [int(c) for c in bbox["coordinate"]],
            "patch_score": bbox["score"],
            "patch": img[int(bbox["coordinate"][1]):int(bbox["coordinate"][3]),
                         int(bbox["coordinate"][0]):int(bbox["coordinate"][2])]
        } for i, bbox in enumerate(data)]
        
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

    @staticmethod
    def warp_polys_to_patches(text_det):
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

    @staticmethod
    def recognize_text_from_patches(warped_patches, text_rec_model, batch_size=1):
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