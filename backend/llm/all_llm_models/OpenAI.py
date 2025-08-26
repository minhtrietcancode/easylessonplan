# avoid disrupting the code by import error, importing the config
try:
    from ...config import OPENAI_BASE_URL, OPENAI_MODEL, OPENROUTER_OPENAI_API
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from config import OPENAI_BASE_URL, OPENAI_MODEL, OPENROUTER_OPENAI_API

# avoid disrupting the code by import error, importing the base class
try:
    from .Model import Model
except ImportError:
    from Model import Model

class Openai(Model):
    def __init__(self):
        super().__init__()
        self.base_url = OPENAI_BASE_URL
        self.model_name = OPENAI_MODEL
        self.api_key = OPENROUTER_OPENAI_API
