# avoid disrupting the code by import error, importing the config
try:
    from ...config import QWEN_BASE_URL, QWEN_MODEL, OPENROUTER_QWEN_API
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from config import QWEN_BASE_URL, QWEN_MODEL, OPENROUTER_QWEN_API

# avoid disrupting the code by import error, importing the base class
try:
    from .Model import Model
except ImportError:
    from Model import Model

class Qwen(Model):
    def __init__(self):
        super().__init__()
        self.base_url = QWEN_BASE_URL
        self.model_name = QWEN_MODEL
        self.api_key = OPENROUTER_QWEN_API
