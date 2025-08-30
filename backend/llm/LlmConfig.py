from dotenv import load_dotenv
import os

load_dotenv()

class LlmConfig:
    """
    Configuration class for Language Model Management.
    Loads API keys and configures models and URLs for all LLM models.
    """

    # Qwen model configuration
    QWEN_BASE_URL = "https://openrouter.ai/api/v1"
    QWEN_MODEL = "qwen/qwen2.5-vl-32b-instruct:free"
    OPENROUTER_QWEN_API = os.getenv("OPENROUTER_QWEN_API")

    # OpenAI model configuration
    OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
    OPENAI_MODEL = "openai/gpt-oss-20b:free"
    OPENROUTER_OPENAI_API = os.getenv("OPENROUTER_OPENAI_API")