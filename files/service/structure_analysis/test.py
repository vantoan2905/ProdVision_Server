# from paddlex import create_model

# model_name = "PP-DocLayout_plus-L"
# model = create_model(model_name=model_name,
#                      device='gpu')
# output = model.predict("/media/tom/Code/pcb_defect/ProdVision_Server/media/data_test/1507.05717v1_page-0007.jpg", batch_size=1, layout_nms=True)

# # for res in output:
# #     print(res)
# res = next(output)

# print(res["boxes"][0])



# from paddlex import create_model
# model = create_model(model_name="RT-DETR-L_wired_table_cell_det", device ='gpu')
# output = model.predict("/media/tom/Code/pcb_defect/ProdVision_Server/media/data_test/image.png",  threshold=0.3, batch_size=1)
# res = next(output)
# print(res.keys())

# from paddlex import create_model

# from structure_analysis import StructureAnalyzer

# layout_model = create_model(model_name="PP-DocLayout_plus-L", device="gpu")
# cell_det_model = create_model(model_name="RT-DETR-L_wired_table_cell_det", device="gpu")
# text_det_model = create_model(model_name="PP-OCRv5_server_det", device="gpu")
# text_rec_model = create_model(model_name="PP-OCRv5_server_rec", device="gpu")

# analyzer = StructureAnalyzer(
#     layout_model=layout_model,
#     cell_det_model=cell_det_model,
#     text_det_model=text_det_model,
#     text_rec_model=text_rec_model
# )

# layout_output = analyzer.full_analysis(img_path="/media/tom/Code/pcb_defect/ProdVision_Server/media/data_test/1507.05717v1_page-0007.jpg")
# # print(layout_output)


# from pypdf import PdfReader

# def extract_text_from_pdf(pdf_path):
#     """
#     Extracts all text from a PDF file.

#     Args:
#         pdf_path (str): The path to the PDF file.

#     Returns:
#         str: The extracted text content.
#     """
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() + "\n"
#     return text

# # Usage: Replace "your_file.pdf" with the path to your file
# file_content = extract_text_from_pdf("/media/tom/Code/pcb_defect/ProdVision_Server/media/data_test/2022.acl-long.180.pdf")
# print(file_content)
