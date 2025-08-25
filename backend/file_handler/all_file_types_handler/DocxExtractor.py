from docx import Document
import os
from backend.file_handler.all_file_types_handler.extractor import Extractor

class DocxExtractor(Extractor):
    def extract_text(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        doc = Document(full_path)
        extracted_text_by_paragraph = {}

        for idx, para in enumerate(doc.paragraphs, start=1):
            extracted_text_by_paragraph[idx] = para.text.strip()

        return extracted_text_by_paragraph

# # uncomment if need to test 
# if __name__ == "__main__":
#     handler = DocxExtractor()
#     text_by_paragraph = handler.extract_text("test_file/docs/sample.docx")
#     print(text_by_paragraph)
