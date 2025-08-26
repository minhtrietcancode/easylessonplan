import SupportedModels
from all_llm_models.Qwen import Qwen
from all_llm_models.OpenAI import OpenAI

class LlmManager():
    def __init__(self) -> None:
        self.supported_models = SupportedModels.supported_models
        self.Qwen = Qwen()
        self.OpenAI = OpenAI()