from models import OCRModels 
from patch_untils import PatchUtils
from table_process import TableProcessor 





class DocumentProcessor:
    def __init__(self, models: OCRModels):
        self.layout_model = models.layout_model
        self.table_model = models.table_model
        self.text_det_model = models.text_det_model
        self.text_rec_model = models.text_rec_model

    def process_document(self, img_path):
        layout_result = self.layout_model.predict(img_path, batch_size=1, layout_nms=True)
        merged_patches = PatchUtils.extract_patches(layout_result, img_path)
        document_paragraphs = []

        for patch_info in merged_patches:
            patch_img = patch_info["patch"]
            patch_idx = patch_info["patch_id"]
            patch_type = patch_info["patch_label"]
            patch_coords = patch_info["patch_positition"]
            patch_conf = patch_info["patch_score"]

            if patch_type == "table":
                table_result = TableProcessor.extract_table_text_from_patch(
                    table_patch=patch_img,
                    table_model=self.table_model,
                    text_det_model=self.text_det_model,
                    text_rec_model=self.text_rec_model
                )
                table_2d = TableProcessor.reconstruct_table_from_result(table_result)
                df = TableProcessor.table_2d_to_df(table_2d)
                recognized_text = TableProcessor.df_to_list_of_dict(df)
            else:
                det_result = self.text_det_model.predict(patch_img, batch_size=1)
                rectified_patches = PatchUtils.warp_polys_to_patches(det_result)
                recognized_text = PatchUtils.recognize_text_from_patches(rectified_patches, self.text_rec_model)

            paragraph_entry = {
                "patch_id": patch_idx,
                "patch_label": patch_type,
                "patch_position": patch_coords,
                "patch_score": patch_conf,
                "text_dict": recognized_text
            }
            document_paragraphs.append(paragraph_entry)

        return document_paragraphs