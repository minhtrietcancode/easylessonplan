from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI


class Model(ABC):
    def __init__(self):
        self.base_url = None
        self.model_name = None
        self.api_key = None

    def initialize_llm_client(self):
        """
        Initializes and returns an LLM client (ChatOpenAI) using the model's configuration.
        """
        if not all([self.base_url, self.model_name, self.api_key]):
            raise ValueError("Model attributes (base_url, model_name, api_key) must be set before initializing the LLM client.")
        
        # openrouter needs to use specific kwargs to configure base_url and api_key
        # also the api_key and base_url will be based on the model that is calling this function
        llm = ChatOpenAI(
            model_name=self.model_name,
            openai_api_base=self.base_url, # this is the openrouter base url
            openai_api_key=self.api_key, # this is the openrouter api key
            # openrouter passes the model name as part of the base_url, 
            # so the model_name param in ChatOpenAI is ignored. 
            # We pass it explicitly in the headers for clarity and potential future use.
            model_kwargs={"headers": {"HTTP-Referer": self.base_url}}, 
            temperature=0.7 # can be changed later
        )
        return llm
