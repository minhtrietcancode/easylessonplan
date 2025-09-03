# Updated OpenAI.py - Simplified using config  
try:
    from ..LlmConfig import LlmConfig
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from backend.llm.LlmConfig import LlmConfig

try:
    from .Model import Model
except ImportError:
    from Model import Model

class DeepSeek(Model):
    def __init__(self):
        config = LlmConfig.get_model_config("DeepSeek")
        super().__init__(config)
        self.llm_client = self.initialize_llm_client()