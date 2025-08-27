'''
    TESTNG THE FILE HANDLER STUFF
'''
# from file_handler.FileHandler import FileHandler

# file_handler = FileHandler()

# test_files = [
#     "../test_file/unsupported.txt",
#     "../test_file/docx/demo.docx",
#     "../test_file/pdf/sample.pdf",
# ]

# for file_path in test_files:
#     print(f"\n--- Testing {file_path} ---")
#     try:
#         extracted_data = file_handler.extractText(file_path)
#         print(f"Successfully extracted data from {file_path}:")
#         for page_num, content in extracted_data.items():
#             print(f"Page {page_num}:\n{content[:200]}...") # Print first 200 chars for brevity
#     except ValueError as e:
#         print(f"Error for {file_path}: {e}")
#     except FileNotFoundError as e:
#         print(f"Error for {file_path}: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred for {file_path}: {e}")


'''
    TESTING LLM STUFFS 
'''
# from llm.LlmManager import LlmManager
# from langchain_core.messages import HumanMessage

# llm_manager = LlmManager()

# # Test Qwen
# print("\n--- Testing Qwen Model ---")
# print(llm_manager.invoke("Say hi with me"))

# # Test OpenAI
# print("\n--- Testing OpenAI Model ---")
# llm_manager.setCurrentModel("Openai")
# print(llm_manager.invoke("Say hi with me"))

'''
    TESTING OS HANDLER
'''
from os_handler.OsHandler import OsHandler
# Initialize the handler
handler = OsHandler()

print("=== System Info ===")
info = handler.get_system_info()
for key, value in info.items():
    print(f"{key}: {value}")

print("\n=== Creating EasyLessonPlan Directory ===")
success, message, path = handler.makeEasyLessonDir()
print(f"Success: {success}")
print(f"Message: {message}")
print(f"Path: {path}")

# Test creating a subdirectory
if success and path:
    print("\n=== Creating Test Subdirectory ===")
    sub_success, sub_message, sub_path = handler.makeDir("Math_Lessons", path)
    print(f"Success: {sub_success}")
    print(f"Message: {sub_message}")
    print(f"Path: {sub_path}")
    
# Test copying a file
if success and path:
    print("\n=== Testing File Copy ===")
    # You can test this by creating a dummy file first or using an existing file
    # For demo purposes, let's show how it would work:
    test_file = r"C:\Users\ADMIN\Downloads\Assignment 1 Stats.pdf"  # Replace with actual file path
    copy_success, copy_message, copy_path = handler.copy_to(test_file, path)
    print(f"Copy Success: {copy_success}")
    print(f"Copy Message: {copy_message}")
    print(f"New File Path: {copy_path}")