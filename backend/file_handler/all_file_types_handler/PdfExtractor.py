from PyPDF2 import PdfReader
import os
from Extractor import Extractor

class PdfExtractor(Extractor):
    # Override
    def extractText(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        reader = PdfReader(full_path)
        extracted_text_by_page = {}

        for idx, page in enumerate(reader.pages, start=1):
            extracted_text_by_page[idx] = page.extract_text() or ""

        return extracted_text_by_page

# uncomment if need to test   
if __name__ == "__main__":
    handler = PdfExtractor()
    text_by_page = handler.extractText("test_file/pdf/sample.pdf")
    print(text_by_page)