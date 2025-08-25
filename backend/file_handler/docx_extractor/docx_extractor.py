from docx import Document
import os

class DocxHandler:
    def extract_text_from_docx(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        doc = Document(full_path)
        extracted_text_by_paragraph = {}

        for idx, para in enumerate(doc.paragraphs, start=1):
            extracted_text_by_paragraph[idx] = para.text.strip()

        return extracted_text_by_paragraph

if __name__ == "__main__":
    handler = DocxHandler()
    text_by_paragraph = handler.extract_text_from_docx("test_file/docs/sample.docx")
    print(text_by_paragraph)
