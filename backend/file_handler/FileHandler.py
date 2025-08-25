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
