from ..LlmConfig import LlmConfig
from .Model import Model

class OpenAI(Model):
    def __init__(self):
        config = LlmConfig.get_model_config("OpenAI")
        super().__init__(config)
        self.llm_client = self.initialize_llm_client()