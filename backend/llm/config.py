from dotenv import load_dotenv
import os

load_dotenv()

#################################################################################
        # LOAD ALL API KEY + CONFIGURE MODEL AND URL FOR ALL LLM MODELS
#################################################################################
'''
Firstly with the free Qwen model
'''
QWEN_BASE_URL = "https://openrouter.ai/api/v1"
QWEN_MODEL = "qwen/qwen2.5-vl-32b-instruct:free"
OPENROUTER_QWEN_API = os.getenv("OPENROUTER_QWEN_API")

'''
Secondly would be free OpenAI model
'''
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_MODEL = "openai/gpt-oss-20b:free"
OPENROUTER_OPENAI_API = os.getenv("OPENROUTER_OPENAI_API")