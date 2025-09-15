# Updated Model.py - Base class remains mostly the same
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI

class Model(ABC):
    def __init__(self, config=None):
        if config:
            self.base_url = config["base_url"]
            self.model_name = config["model_name"] 
            self.api_key = config["api_key"]
        else:
            self.base_url = None
            self.model_name = None
            self.api_key = None

    def initialize_llm_client(self):
        """
        Initializes and returns an LLM client (ChatOpenAI) using the model's configuration.
        """
        if not all([self.base_url, self.model_name, self.api_key]):
            raise ValueError("Model attributes (base_url, model_name, api_key) must be set before initializing the LLM client.")
        
        llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_base=self.base_url,
            openai_api_key=self.api_key,
            temperature=0.7
        )
        return llm