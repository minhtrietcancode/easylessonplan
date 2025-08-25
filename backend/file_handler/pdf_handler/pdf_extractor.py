from PyPDF2 import PdfReader
import os

class PdfHandler:
    def extract_text_from_pdf(self, relative_path: str) -> str:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        reader = PdfReader(full_path)
        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        return extracted_text.strip()
    
if __name__ == "__main__":
    handler = PdfHandler()
    text = handler.extract_text_from_pdf("test_file/pdf/module01-slides-print-5.pdf")
    print(text)