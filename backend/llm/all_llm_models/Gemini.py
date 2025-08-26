# avoid disrupting the code by import error, importing the config
try:
    from ...config import GEMINI_BASE_URL, GEMINI_MODEL, OPENROUTER_GEMINI_API
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from config import GEMINI_BASE_URL, GEMINI_MODEL, OPENROUTER_GEMINI_API

# avoid disrupting the code by import error, importing the base class
try:
    from .Model import Model
except ImportError:
    from Model import Model

class Gemini(Model):
    def __init__(self):
        super().__init__()
        self.base_url = GEMINI_BASE_URL
        self.model_name = GEMINI_MODEL
        self.api_key = OPENROUTER_GEMINI_API
