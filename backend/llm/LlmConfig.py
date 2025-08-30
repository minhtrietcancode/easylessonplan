# Updated LlmConfig.py
from dotenv import load_dotenv
import os

load_dotenv()

class LlmConfig:
    """
    Configuration class for Language Model Management.
    Loads API keys and configures models and URLs for all LLM models.
    """
    
    # Model configurations - add new models here
    MODEL_CONFIGS = {
        "Qwen": {
            "base_url": "https://openrouter.ai/api/v1",
            "model_name": "qwen/qwen2.5-vl-32b-instruct:free",
            "api_key": os.getenv("OPENROUTER_QWEN_API"),
            "class_name": "Qwen"
        },
        "OpenAI": {
            "base_url": "https://openrouter.ai/api/v1", 
            "model_name": "openai/gpt-oss-20b:free",
            "api_key": os.getenv("OPENROUTER_OPENAI_API"),
            "class_name": "OpenAI"
        },
        # Add new models here - example:
        # "Claude": {
        #     "base_url": "https://openrouter.ai/api/v1",
        #     "model_name": "anthropic/claude-3.5-sonnet",
        #     "api_key": os.getenv("OPENROUTER_CLAUDE_API"),
        #     "class_name": "Claude"
        # }
    }
    
    @classmethod
    def get_supported_models(cls):
        """Returns list of supported model names"""
        return list(cls.MODEL_CONFIGS.keys())
    
    @classmethod
    def get_model_config(cls, model_name: str):
        """Returns configuration for a specific model"""
        return cls.MODEL_CONFIGS.get(model_name)