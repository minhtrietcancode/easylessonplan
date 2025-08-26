import os

try:
    from .Extractor import Extractor
except ImportError:
    from Extractor import Extractor

class TxtExtractor(Extractor):
    def extractText(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return {1: content}

if __name__ == "__main__":
    handler = TxtExtractor()
    try:
        text_by_page = handler.extractText("test_file/unsupported.txt")
        print(text_by_page)
    except Exception as e:
        print(f"Extraction failed: {e}")
