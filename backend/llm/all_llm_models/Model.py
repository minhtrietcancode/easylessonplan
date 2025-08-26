from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self):
        self.base_url = None
        self.model_name = None
        self.api_key = None
