# avoid disrupting the code by import error, importing the config
try:
    from ..LlmConfig import LlmConfig
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from backend.llm.LlmConfig import LlmConfig

# avoid disrupting the code by import error, importing the base class
try:
    from .Model import Model
except ImportError:
    from Model import Model

class Openai(Model):
    def __init__(self):
        super().__init__()
        self.base_url = LlmConfig.OPENAI_BASE_URL
        self.model_name = LlmConfig.OPENAI_MODEL
        self.api_key = LlmConfig.OPENROUTER_OPENAI_API
        self.llm_client = self.initialize_llm_client()
