from openai import OpenAI

# Import your model classes
from OpenAI import OpenAI as OpenAILLM
from Qwen import Qwen

def test_openai_api():
    print("Testing OpenAI API...")
    openai_llm = OpenAILLM() # Renamed to avoid conflict with imported OpenAI client
    client = OpenAI(
        base_url=openai_llm.base_url,
        api_key=openai_llm.api_key,
    )

    try:
        completion = client.chat.completions.create(
            model=openai_llm.model_name,
            messages=[
                {
                    "role": "user",
                    "content": "What is the capital of Japan?"
                }
            ]
        )
        print("OpenAI API Response:")
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error testing OpenAI API: {e}")

def test_qwen_api():
    print("Testing Qwen API...")
    qwen_model = Qwen()
    client = OpenAI(
        base_url=qwen_model.base_url,
        api_key=qwen_model.api_key,
    )

    try:
        completion = client.chat.completions.create(
            model=qwen_model.model_name,
            messages=[
                {
                    "role": "user",
                    "content": "What is the capital of Germany?"
                }
            ]
        )
        print("Qwen API Response:")
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error testing Qwen API: {e}")

if __name__ == "__main__":
    test_openai_api()
    test_qwen_api()
