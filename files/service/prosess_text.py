from .vision_ai import VisionAIService
import os 
import pandas as pd
import numpy as np


class ProcessTextService:
    def __init__(self):
        self.vision_ai_service = VisionAIService()


    def chunking_text(self, text, chunk_size=100):
        """Chunk text into smaller pieces of specified size.
        
        Args:
            text (str): The input text to be chunked.
            chunk_size (int): The size of each chunk.
        
        Returns:
            list: A list of text chunks.
        """
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    def embed_text(self, text):
        """Embed text using a placeholder embedding method.
        
        Args:
            text (str): The input text to be embedded.
        
        Returns:
            list: A placeholder list representing the embedded text.
        """
        # Placeholder for actual embedding logic
        return [ord(char) for char in text]  
    

    def _extract_text_from_image(self, image_path):
        """Extract text from an image using VisionAIService.
        
        Args:
            image_path (str): The path to the image file.
            
        Returns:
            str: The extracted text from the image.
        """
        return self.vision_ai_service.extract_text(image_path)
    def  _extract_text_from_single_pdf(self, pdf_path):
        # Placeholder for actual PDF text extraction logic
        # For example, using PyPDF2 or pdfplumber to extract text from a single PDF file
        extracted_text = "Extracted text from PDF at {}".format(pdf_path)
        return extracted_text
    def _extract_text_from_pdf(self, pdf_path, chunk_size=100):
        # if is folder
        if os.path.isdir(pdf_path):
            all_texts = []
            for filename in os.listdir(pdf_path):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_path, filename)
                    text = self._extract_text_from_single_pdf(file_path)
                    all_texts.append(text)
            combined_text = "\n".join(all_texts)
            return self.chunking_text(combined_text, chunk_size)
        





