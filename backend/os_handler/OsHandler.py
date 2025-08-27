import os
import platform
import shutil
from pathlib import Path

class OsHandler:
    def __init__(self):
        """Initialize the OsHandler with the appropriate base directory"""
        self.system = platform.system().lower()
        self.base_dir = self._get_base_directory()
        self.easy_lesson_dir = os.path.join(self.base_dir, "EasyLessonPlan")
    
    def _get_base_directory(self):
        """Get the appropriate base directory based on the operating system"""
        if self.system == "windows":
            # For Windows: C:\Users\{username}\
            return os.path.expanduser("~")
        elif self.system == "darwin":  # macOS
            # For macOS: /Users/{username}/
            return os.path.expanduser("~")
        else:
            # For Linux and others
            return os.path.expanduser("~")
    
    def _check_easy_lesson_exists(self):
        """Check if EasyLessonPlan directory already exists"""
        return os.path.exists(self.easy_lesson_dir) and os.path.isdir(self.easy_lesson_dir)
    
    def makeEasyLessonDir(self):
        """
        Create the main EasyLessonPlan directory if it doesn't exist
        Returns: tuple (success: bool, message: str, path: str)
        """
        try:
            if self._check_easy_lesson_exists():
                return True, "EasyLessonPlan directory already exists", self.easy_lesson_dir
            
            os.makedirs(self.easy_lesson_dir, exist_ok=True)
            
            # Verify creation
            if self._check_easy_lesson_exists():
                return True, f"EasyLessonPlan directory created successfully", self.easy_lesson_dir
            else:
                return False, "Failed to create EasyLessonPlan directory", None
                
        except PermissionError:
            return False, "Permission denied. Cannot create directory in this location", None
        except Exception as e:
            return False, f"Error creating directory: {str(e)}", None
    
    def makeDir(self, folder_name, parent_folder):
        """
        Create a directory with given folder_name inside parent_folder
        
        Args:
            folder_name (str): Name of the folder to create
            parent_folder (str): Path to the parent directory
            
        Returns: tuple (success: bool, message: str, full_path: str)
        """
        try:
            # Validate inputs
            if not folder_name or not folder_name.strip():
                return False, "Folder name cannot be empty", None
            
            if not parent_folder or not parent_folder.strip():
                return False, "Parent folder path cannot be empty", None
            
            # Check if parent folder exists
            if not os.path.exists(parent_folder):
                return False, f"Parent folder does not exist: {parent_folder}", None
            
            if not os.path.isdir(parent_folder):
                return False, f"Parent path is not a directory: {parent_folder}", None
            
            # Create full path for new directory
            new_folder_path = os.path.join(parent_folder, folder_name.strip())
            
            # Check if folder already exists
            if os.path.exists(new_folder_path):
                if os.path.isdir(new_folder_path):
                    return True, f"Directory '{folder_name}' already exists", new_folder_path
                else:
                    return False, f"A file with name '{folder_name}' already exists at this location", None
            
            # Create the directory
            os.makedirs(new_folder_path, exist_ok=True)
            
            # Verify creation
            if os.path.exists(new_folder_path) and os.path.isdir(new_folder_path):
                return True, f"Directory '{folder_name}' created successfully", new_folder_path
            else:
                return False, f"Failed to create directory '{folder_name}'", None
                
        except PermissionError:
            return False, f"Permission denied. Cannot create '{folder_name}' in '{parent_folder}'", None
        except Exception as e:
            return False, f"Error creating directory: {str(e)}", None
    
    def get_easy_lesson_path(self):
        """Get the full path to the EasyLessonPlan directory"""
        return self.easy_lesson_dir
    
    def copy_to(self, copied_file_path, aimed_folder):
        """
        Copy a file from source location to a destination folder within EasyLessonPlan structure
        
        Args:
            copied_file_path (str): Full path to the file that needs to be copied
            aimed_folder (str): Destination folder where the file should be copied to
            
        Returns: tuple (success: bool, message: str, new_file_path: str)
        """
        try:
            # Validate inputs
            if not copied_file_path or not copied_file_path.strip():
                return False, "Source file path cannot be empty", None
                
            if not aimed_folder or not aimed_folder.strip():
                return False, "Destination folder path cannot be empty", None
            
            # Clean up paths
            source_path = copied_file_path.strip()
            dest_folder = aimed_folder.strip()
            
            # Check if source file exists
            if not os.path.exists(source_path):
                return False, f"Source file does not exist: {source_path}", None
                
            if not os.path.isfile(source_path):
                return False, f"Source path is not a file: {source_path}", None
            
            # Check if destination folder exists
            if not os.path.exists(dest_folder):
                return False, f"Destination folder does not exist: {dest_folder}", None
                
            if not os.path.isdir(dest_folder):
                return False, f"Destination path is not a directory: {dest_folder}", None
            
            # Get the filename from source path
            filename = os.path.basename(source_path)
            
            # Create full destination path
            dest_file_path = os.path.join(dest_folder, filename)
            
            # Check if file already exists at destination
            if os.path.exists(dest_file_path):
                # Generate a unique filename by adding a number
                base_name, extension = os.path.splitext(filename)
                counter = 1
                
                while os.path.exists(dest_file_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    dest_file_path = os.path.join(dest_folder, new_filename)
                    counter += 1
                
                filename = os.path.basename(dest_file_path)  # Update filename for the message
            
            # Copy the file
            shutil.copy2(source_path, dest_file_path)
            
            # Verify the copy was successful
            if os.path.exists(dest_file_path) and os.path.isfile(dest_file_path):
                return True, f"File '{filename}' copied successfully to destination folder", dest_file_path
            else:
                return False, "File copy failed - destination file not found after copy", None
                
        except PermissionError:
            return False, f"Permission denied. Cannot copy file to '{aimed_folder}'", None
        except shutil.SameFileError:
            return False, "Source and destination are the same file", None
        except Exception as e:
            return False, f"Error copying file: {str(e)}", None
    
    def get_system_info(self):
        """Get system information for debugging"""
        return {
            "system": self.system,
            "base_dir": self.base_dir,
            "easy_lesson_dir": self.easy_lesson_dir,
            "exists": self._check_easy_lesson_exists()
        }


# Example usage and testing
if __name__ == "__main__":
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
        
        # # Test copying to a subdirectory
        # if sub_success and sub_path:
        #     print("\n=== Testing Copy to Subdirectory ===")
        #     copy_success2, copy_message2, copy_path2 = handler.copy_to(test_file, sub_path)
        #     print(f"Copy Success: {copy_success2}")
        #     print(f"Copy Message: {copy_message2}")
        #     print(f"New File Path: {copy_path2}")