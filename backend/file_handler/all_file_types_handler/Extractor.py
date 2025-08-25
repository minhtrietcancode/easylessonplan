from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extractText(self, relative_path: str) -> dict:
        pass
