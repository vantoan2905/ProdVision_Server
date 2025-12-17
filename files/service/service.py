from files.service.vision_ai import VisionAIPipeline
from files.service.pdf_file import VisionPDFPipeline
from sentence_transformers import SentenceTransformer

class Service:
    def __init__(self):
        self.vision_ai_pipeline = VisionAIPipeline(languages=['en'], gpu=True)
        self.vision_pdf_pipeline = VisionPDFPipeline()

        self.embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


    # --- Image Processing ---
    def process_image(self, image, file_name="image.jpg", generate_lines=True):
        return self.vision_ai_pipeline._process_single_image(image, generate_lines, file_name)

    # --- PDF Processing ---
    def process_pdf(self, pdf_path):
        return self.vision_pdf_pipeline.process_pdf(pdf_path)

    def split_text_pdf(self, text):
        return self.vision_pdf_pipeline.split_text(text)

    def make_meta_data_pdf(self, text):
        return self.vision_pdf_pipeline.make_meta_data(text)

    # --- Text Splitting ---
    def chunk_text(self, text, max_chars=500, overlap=50):

        if not isinstance(text, str):
            raise ValueError("text mush be string.")

        text = text.strip()
        chunks = []

        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + max_chars
            chunk = text[start:end]

            chunks.append(chunk)

            start = end - overlap
            if start < 0:
                start = 0

        return chunks


    def split_text(self, text):
        document_chunks = self.chunk_text(text=text)
        return document_chunks


    # --- Text Embedding ---
    def vectorize_texts(self, texts):
        return self.embed_model.encode(texts).tolist()
