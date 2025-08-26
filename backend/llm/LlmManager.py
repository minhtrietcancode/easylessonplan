import SupportedModels
from all_llm_models.Qwen import Qwen

class LlmManager():
    def __init__(self) -> None:
        self.Qwen = Qwen()