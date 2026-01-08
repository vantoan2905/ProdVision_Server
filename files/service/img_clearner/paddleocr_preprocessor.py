import os
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

# import paddle
# paddle.set_device("cpu")

from paddleocr import DocPreprocessor
import cv2

class OCRPreprocessor:
    def __init__(
        self,
        use_orientation=True,
        use_unwarping=True,
        device='cpu'
    ):
        """
        use_orientation: use doc orientation classification or not
        use_unwarping: use doc unwarping or not
        device: 'cpu' or 'gpu'
        """
        self.pipeline = DocPreprocessor(
            use_doc_orientation_classify=use_orientation,
            use_doc_unwarping=use_unwarping,
            device=device
        )

    def preprocess_from_path(self, img_path):
        """
        Preprocess a document image from a file path.
        Returns the preprocessed image as a numpy array.
        """
        # Run the pipeline
        results = self.pipeline.predict(img_path)

        for res in results:
            res.save_to_img("./output/")
        return results
    
# sample usage:


# if __name__ == "__main__":
#     pre = OCRPreprocessor(use_orientation=True, use_unwarping=True, device='cpu')
#     dt =pre.preprocess_from_path(r"/media/tom/Code/pcb_defect/ProdVision_Server/generated/ocr_test_009.jpg")
#     print(dt[0]["output_img"])
#     cv2.imwrite("output.jpg", dt[0]["output_img"])



