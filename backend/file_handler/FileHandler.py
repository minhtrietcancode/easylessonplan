#######################################################################################################################
                                        # IMPORTING STATEMENTS 
#######################################################################################################################
# some package for directory management 
import os
import importlib.util
from pathlib import Path

# configured allowed file + metadata 
import AllowedFile

# all of the classes that handle + extract data for different file types
from all_file_types_handler.PdfExtractor import PdfExtractor
from all_file_types_handler.DocxExtractor import DocxExtractor

#######################################################################################################################
                                        # CLASS FOR FILE HANDLER 
#######################################################################################################################
class FileHandler:
    def __init__(self):
        # initialize the allowed_file 
        self.allowed_file = AllowedFile.allowed_file

        # get an instance of each Extractor classes 
        self.PdfExtractor = PdfExtractor()
        self.DocxExtractor = DocxExtractor()
    

    """
        Extract the file extension from the file path
        Returns: file extension in lowercase (without the dot)
    """
    def getFileType(self, file_path: str) -> str:     
        return Path(file_path).suffix[1:].lower()
    

    """
        Check if the file type is supported
        Returns: True if file type is allowed, False otherwise
    """
    def validateFileType(self, file_path: str) -> bool:
        file_type = self.getFileType(file_path)
        return file_type in self.allowed_file
    

    """
        Extracts text from a file based on its type.
        Raises: ValueError if the file type is unsupported.
        Returns: A dictionary where keys are page numbers and values are extracted text.
    """
    def extractText(self, file_path: str) -> dict:
        # we need to get the file type first
        file_type = self.getFileType(file_path)

        # then check if the file type is supported or not
        if not self.validateFileType(file_path):
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # and then use the defined dictionary to get the correct extractor instance of this class
        extractor_class_name = self.allowed_file[file_type]["class_name"]
        extractor_instance = getattr(self, extractor_class_name)

        # after getting correct extractor instance --> use that to extract and return extracted data 
        return extractor_instance.extractText(file_path)
    

    
if __name__ == "__main__":
    file_handler = FileHandler()

    test_files = [
        "test_file/unsupported.txt",
        "test_file/docx/demo.docx",
        "test_file/pdf/sample.pdf",
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
    

    