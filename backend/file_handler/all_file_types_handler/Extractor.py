from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extract_text(self, relative_path: str) -> dict:
        pass
