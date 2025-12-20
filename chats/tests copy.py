from ocr.ocr_service import OCRService

img_path = "/media/tom/Code/pcb_defect/ProdVision_Server/chats/output/1507.05717v1_page-0005_res.jpg"

ocr = OCRService(device="gpu")

result = ocr.process(img_path)

print(result)
