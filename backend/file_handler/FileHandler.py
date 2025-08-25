'''
We need these things for the class FileHandler 
    - With instance variables 
        + FileHandler class should have an instance for each file type's extractor 
        + An instance called: Extractor currentExtractor;
    
    - With the methods 
        + getFileType(file_path): --> this will return the type of that file 
        + validateFileType(file_path): --> check if the type is in allowed file or not --> return True / False
        + updateCurrentExtractor(file_path): this one would getFileType() first --> validateFileType() later
            - if the validate function return False then print a statement to notify + exit this function / return False
            - if the validate function return True, then follow this procedure 
                + use the allowed_file imported from the AllowedFile class to look for correct 
                  Extractor of the current file_path  --> then change the instance currentExtractor 
                  to that correct Extractor
        + extractText(file_path): 
            - call the updateCurrentExtractor() function first, if it return False --> then exit no need to do anything
            - if the function has done, then use the currentExtractor which has been updated above 
              --> call the method currentExtractor.extractText(file_path)
'''

import os
import importlib.util
from pathlib import Path
from AllowedFile import allowed_file
from all_file_types_handler.Extractor import Extractor

class FileHandler:
    def __init__(self):
        self.currentExtractor = None
        self._extractor_cache = {}  # Cache to avoid re-importing the same extractor
    
    def getFileType(self, file_path: str) -> str:
        """
        Extract the file extension from the file path
        Returns: file extension in lowercase (without the dot)
        """
        return Path(file_path).suffix[1:].lower()
    
    def validateFileType(self, file_path: str) -> bool:
        """
        Check if the file type is supported
        Returns: True if file type is allowed, False otherwise
        """
        file_type = self.getFileType(file_path)
        return file_type in allowed_file
    
    def _loadExtractor(self, file_type: str):
        """
        Dynamically load and instantiate the appropriate extractor class
        Returns: Instance of the extractor class
        """
        # Check cache first
        if file_type in self._extractor_cache:
            return self._extractor_cache[file_type]
        
        # and then get the file path + class name for corresponding extractor
        extractor_info = allowed_file[file_type]
        extractor_path = extractor_info["extractor_relative_path"]
        class_name = extractor_info["class_name"]
        
        try:
            # Get absolute path to the extractor module
            # module_path = os.path.abspath(extractor_path)
            base_dir = Path(__file__).parent
            module_path = base_dir / extractor_path

            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(class_name, module_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module from {module_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the class from the module
            extractor_class = getattr(module, class_name)
            
            # Create an instance of the extractor
            extractor_instance = extractor_class()
            
            # Cache the instance for future use
            self._extractor_cache[file_type] = extractor_instance
            
            return extractor_instance
            
        except Exception as e:
            raise RuntimeError(f"Failed to load extractor for {file_type}: {str(e)}")
    
    def updateCurrentExtractor(self, file_path: str) -> bool:
        """
        Update the current extractor based on file type
        Returns: True if successful, False if file type is not supported
        """
        # First validate the file type
        if not self.validateFileType(file_path):
            file_type = self.getFileType(file_path)
            print(f"Error: File type '{file_type}' is not supported. Supported types: {list(allowed_file.keys())}")
            return False
        
        try:
            # Get file type and load appropriate extractor
            file_type = self.getFileType(file_path)
            self.currentExtractor = self._loadExtractor(file_type)
            return True
            
        except Exception as e:
            print(f"Error updating extractor: {str(e)}")
            return False
    
    def extractText(self, file_path: str) -> dict:
        """
        Extract text from the file using the appropriate extractor
        Returns: Dictionary containing extracted text
        """
        # Update the current extractor first
        if not self.updateCurrentExtractor(file_path):
            return {}
        
        try:
            # Use the current extractor to extract text
            return self.currentExtractor.extractText(file_path)
            
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return {}
    
    def getSupportedFileTypes(self) -> list:
        """
        Get list of supported file types
        Returns: List of supported file extensions
        """
        return list(allowed_file.keys())


# Example usage and testing
if __name__ == "__main__":
    # Create FileHandler instance
    handler = FileHandler()
    
    # Test with different file types
    test_files = [
        "test_file/pdf/sample.pdf",
        "test_file/docx/file-sample_100kB.docx",
        "test_file/unsupported.txt"  # This should fail validation
    ]
    
    for file_path in test_files:
        print(f"\n--- Testing with: {file_path} ---")
        
        # Check file type
        file_type = handler.getFileType(file_path)
        print(f"File type: {file_type}")
        
        # Validate file type
        is_valid = handler.validateFileType(file_path)
        print(f"Is valid: {is_valid}")
        
        if is_valid:
            # Extract text
            extracted_text = handler.extractText(file_path)
            if extracted_text:
                print(f"Successfully extracted {len(extracted_text)} sections")
                # Print first few entries as sample
                for key in list(extracted_text.keys())[:3]:
                    preview = extracted_text[key][:100] + "..." if len(extracted_text[key]) > 100 else extracted_text[key]
                    print(f"  {key}: {preview}")
            else:
                print("No text extracted")
        else:
            print("File type not supported")
    
    # Show supported file types
    print(f"\nSupported file types: {handler.getSupportedFileTypes()}")