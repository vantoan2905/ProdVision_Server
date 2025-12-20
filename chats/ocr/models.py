from paddleocr import (
    LayoutDetection,
    TableCellsDetection,
    TextDetection,
    TextRecognition
)

class OCRModels:
    def __init__(self, device="gpu"):
        self.layout = LayoutDetection(
            device=device,
            model_name="PP-DocLayoutV2"
        )
        self.table = TableCellsDetection(
            device=device,
            model_name="RT-DETR-L_wired_table_cell_det"
        )
        self.text_det = TextDetection(
            device=device,
            model_name="PP-OCRv5_server_det"
        )
        self.text_rec = TextRecognition(
            device=device,
            model_name="PP-OCRv5_mobile_rec"
        )
