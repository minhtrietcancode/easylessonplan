
import os

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_file_type(self) -> str:
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lstrip('.').lower()

    def validate_file_type(self) -> bool:
        from AllowedFile import allowed_file
        file_type = self.get_file_type()
        if file_type in allowed_file:
            return True
        else:
            print(f"Notification: File type '{file_type}' is not supported.")
            return False

    def extract_file_content(self) -> dict:
        from AllowedFile import allowed_file
        file_type = self.get_file_type()

        if not self.validate_file_type():
            return {}

        handler_info = allowed_file[file_type]
        handler_relative_path = handler_info["handler_relative_path"]
        class_name = handler_info["class_name"]

        # Dynamically import the handler module
        module_path = handler_relative_path.replace("/", ".")[:-3]  # Remove .py
        module = __import__(module_path, fromlist=[class_name])
        ExtractorClass = getattr(module, class_name)

        extractor = ExtractorClass()
        return extractor.extract_text(self.file_path)
    
'''
We need these things for the class FileHandler 
    - With instance variables 
        + FileHandler class should have an instance for each file type's extractor 
    
    - With the methods 
        + 
'''
