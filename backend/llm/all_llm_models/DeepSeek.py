from ..LlmConfig import LlmConfig
from .Model import Model

class DeepSeek(Model):
    def __init__(self):
        config = LlmConfig.get_model_config("DeepSeek")
        super().__init__(config)
        self.llm_client = self.initialize_llm_client()