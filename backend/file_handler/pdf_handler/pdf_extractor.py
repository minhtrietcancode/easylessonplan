from PyPDF2 import PdfReader
import os

class PdfHandler:
    def extract_text_from_pdf(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        reader = PdfReader(full_path)
        extracted_text_by_page = {}

        for idx, page in enumerate(reader.pages, start=1):
            extracted_text_by_page[idx] = page.extract_text() or ""

        return extracted_text_by_page
    
if __name__ == "__main__":
    handler = PdfHandler()
    text_by_page = handler.extract_text_from_pdf("test_file/pdf/module01-slides-print-5.pdf")
    print(text_by_page)