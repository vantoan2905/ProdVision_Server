from paddleocr import LayoutDetection, TableCellsDetection, TextDetection, TextRecognition

# --- Lazy init các model OCR (singleton đơn giản) ---
_layout_model = None
_table_model = None
_text_det_model = None
_text_rec_model = None

def get_layout_model():
    global _layout_model
    if _layout_model is None:
        _layout_model = LayoutDetection(model_name="PP-DocLayoutV2")
    return _layout_model

def get_table_model():
    global _table_model
    if _table_model is None:
        _table_model = TableCellsDetection(model_name="RT-DETR-L_wired_table_cell_det")
    return _table_model

def get_text_det_model():
    global _text_det_model
    if _text_det_model is None:
        _text_det_model = TextDetection(model_name="PP-OCRv5_server_det")
    return _text_det_model

def get_text_rec_model():
    global _text_rec_model
    if _text_rec_model is None:
        _text_rec_model = TextRecognition(model_name="PP-OCRv5_server_rec")
    return _text_rec_model

# --- Pipeline OCR ---
def ocr_pipeline(img_path):
    layout_model = get_layout_model()
    table_model = get_table_model()
    text_det_model = get_text_det_model()
    text_rec_model = get_text_rec_model()

    # 1. Layout
    layout = layout_model.predict(img_path, batch_size=1, layout_nms=True)

    # 2. Table cells (nếu cần)
    tables = table_model.predict(img_path, threshold=0.3, batch_size=1)

    # 3. Text detection
    text_det = text_det_model.predict(img_path, batch_size=1)

    # 4. Text recognition
    text_lines = text_rec_model.predict(text_det, batch_size=1)

    # Flatten text
    lines = []
    for page in text_lines:
        for item in page:
            lines.append(item[0])  # text

    return "\n".join(lines)

# --- Test ---
if __name__ == "__main__":
    img_path = "/media/tom/Code/pcb_defect/ProdVision_Server/image copy.png"  # đổi thành ảnh của bạn
    extracted_text = ocr_pipeline(img_path)
    print("=== OCR Extracted Text ===")
    print(extracted_text)
