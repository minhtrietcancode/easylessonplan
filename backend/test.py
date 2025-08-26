'''
    TESTNG THE FILE HANDLER STUFF
'''
from file_handler.FileHandler import FileHandler

file_handler = FileHandler()

test_files = [
    "../test_file/unsupported.txt",
    "../test_file/docx/demo.docx",
    "../test_file/pdf/sample.pdf",
]

for file_path in test_files:
    print(f"\n--- Testing {file_path} ---")
    try:
        extracted_data = file_handler.extractText(file_path)
        print(f"Successfully extracted data from {file_path}:")
        for page_num, content in extracted_data.items():
            print(f"Page {page_num}:\n{content[:200]}...") # Print first 200 chars for brevity
    except ValueError as e:
        print(f"Error for {file_path}: {e}")
    except FileNotFoundError as e:
        print(f"Error for {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {file_path}: {e}")


'''
    TESTING LLM STUFFS 
'''
# from llm.LlmManager import LlmManager
# from langchain_core.messages import HumanMessage

# llm_manager = LlmManager()

# # Test Qwen
# print("\n--- Testing Qwen Model ---")
# try:
#     llm_manager.setCurrentModel("Qwen")
#     qwen_client = llm_manager.getCurrentModel()
#     response_qwen = qwen_client.invoke([HumanMessage(content="Hi, say hi back")])
#     print(f"Qwen response: {response_qwen.content}")
# except ValueError as e:
#     print(f"Error setting Qwen model: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred with Qwen: {e}")

# # Test OpenAI
# print("\n--- Testing OpenAI Model ---")
# try:
#     llm_manager.setCurrentModel("Openai")
#     openai_client = llm_manager.getCurrentModel()
#     response_openai = openai_client.invoke([HumanMessage(content="Hi, say hi back")])
#     print(f"OpenAI response: {response_openai.content}")
# except ValueError as e:
#     print(f"Error setting OpenAI model: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred with OpenAI: {e}")
