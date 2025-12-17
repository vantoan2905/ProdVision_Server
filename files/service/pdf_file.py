from pypdf import PdfReader
import uuid
from pathlib import Path
from typing import Dict, List

class VisionPDFPipeline:
    SUPPORTED_EXTENSIONS = {'.pdf'}

    def __init__(self):
        pass

    def process_pdf(self, pdf_path: str) -> Dict:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if pdf_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {pdf_path.suffix}")

        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        page_results: List[Dict] = []
        total_words = 0

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""  # một số trang trống trả về None
            words = text.split()
            total_words += len(words)
            page_results.append({
                "page_number": i + 1,
                "text": text,
                "word_count": len(words)
            })

        full_text = "\n".join(p['text'] for p in page_results)

        return {
            "id": str(uuid.uuid4()),
            "file_path": str(pdf_path),
            "file_name": pdf_path.name,
            "text": full_text,
            "pages": total_pages,
            "total_words": total_words,
            "page_results": page_results
        }

# # --- ví dụ sử dụng ---
# if __name__ == "__main__":
#     pipeline = VisionPDFPipeline()
#     result = pipeline.process_pdf("example.pdf")
#     print(f"PDF có {result['pages']} trang, tổng số từ: {result['total_words']}")
#     # print(result['page_results'])  # nếu muốn xem chi tiết từng trang
