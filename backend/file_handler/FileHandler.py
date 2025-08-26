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
    
    '''
        
    '''
