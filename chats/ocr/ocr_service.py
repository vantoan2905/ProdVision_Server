from chats.ocr.models import OCRModels
from chats.ocr.layout_service import LayoutService 
from chats.ocr.table_service import TableService
from chats.ocr.text_service import TextService



class OCRService:
    def __init__(self, device="gpu"):
        self.models = OCRModels(device=device)

        self.layout_service = LayoutService()
        self.table_service = TableService()
        self.text_service = TextService()

    def process(self, img_path):
        layout = self.models.layout.predict(
            img_path,
            batch_size=1,
            layout_nms=True
        )

        patches = self.layout_service.extract_patches(layout, img_path)

        results = []

        for p in patches:
            if p["patch_label"] == "table":
                cells = self.table_service.detect_cells(
                    p["patch"],
                    self.models.table
                )

                table = self.table_service.extract_table(
                    p["patch"],
                    cells,
                    self.models.text_det,
                    self.models.text_rec
                )

                results.append(table)

            else:
                det = self.models.text_det.predict(
                    p["patch"],
                    batch_size=1
                )

                warped = self.text_service.warp_polys_to_patches(det)

                text = self.text_service.recognize(
                    warped,
                    self.models.text_rec
                )

                results.append(text)

        return results
