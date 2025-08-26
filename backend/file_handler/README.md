# `file_handler/` Directory Documentation

This directory is responsible for handling various file types, extracting their content, and providing a unified interface for file processing. It's designed to be extensible, allowing easy addition of new file type extractors.

## Directory Structure

```
file_handler/
├── __init__.py               # Marks 'file_handler' as a Python package
├── AllowedFile.py            # Defines supported file types and their corresponding extractor class names
├── FileHandler.py            # Main entry point for file processing
├── document.md               # This documentation file
└── all_file_types_handler/   # Subpackage for specific file type extractors
    ├── __init__.py           # Marks 'all_file_types_handler' as a Python package
    ├── Extractor.py          # Abstract base class for all file extractors
    ├── DocxExtractor.py      # Handles text extraction from DOCX files
    └── PdfExtractor.py       # Handles text extraction from PDF files
```

## Workflow and Component Responsibilities

The core idea is to provide a flexible system where new file types can be added without modifying the central `FileHandler` logic.

### 1. `AllowedFile.py`

*   **Purpose**: This file defines a dictionary, `allowed_file`, which acts as a configuration for supported file types.
*   **Content**: Each key in the dictionary is a file extension (e.g., "pdf", "docx"), and its value is another dictionary containing metadata, specifically `"class_name"` which points to the name of the Python class responsible for extracting text from that file type.
*   **Role in Workflow**: `FileHandler.py` consults this dictionary to determine if a file type is supported and to dynamically get the correct extractor instance.

### 2. `all_file_types_handler/Extractor.py`

*   **Purpose**: This file defines an abstract base class (`Extractor`) that all specific file type extractors must inherit from.
*   **Content**: It uses Python's `abc` module to define an `abstractmethod` called `extractText(self, relative_path: str) -> dict`.
*   **Role in Workflow**: Enforces a consistent interface for all extractors, ensuring that any new extractor will have an `extractText` method that takes a file path and returns a dictionary of extracted text by page.

### 3. `all_file_types_handler/PdfExtractor.py` and `all_file_types_handler/DocxExtractor.py`

*   **Purpose**: These are concrete implementations of the `Extractor` abstract base class, each specialized for a particular file type.
*   **Content**:
    *   `PdfExtractor.py`: Uses `PyPDF2` to read and extract text content from PDF files, returning a dictionary where keys are page numbers (1-based) and values are the extracted text for that page.
    *   `DocxExtractor.py`: Uses `python-docx` and `docx2pdf` (with `PyMuPDF` for PDF conversion) to extract text from DOCX files. It prioritizes converting DOCX to PDF for accurate page-based extraction, falling back to a direct DOCX parsing with character-based page estimation if PDF conversion fails.
*   **Role in Workflow**: They provide the actual logic for parsing and extracting content from their respective file formats. They handle file-specific libraries and data structures. Both include conditional import logic to allow them to be run directly for testing or imported as part of the package.

### 4. `FileHandler.py`

*   **Purpose**: This is the central orchestration point for file handling. It provides a high-level API for determining file types, validating them, and delegating text extraction to the appropriate specialized extractor.
*   **Content**:
    *   `__init__`: Initializes instances of all supported `Extractor` classes (e.g., `self.PdfExtractor`, `self.DocxExtractor`). It also loads the `allowed_file` dictionary from `AllowedFile.py`.
    *   `getFileType(self, file_path: str) -> str`: Extracts the file extension from a given path.
    *   `validateFileType(self, file_path: str) -> bool`: Checks if a file's type is listed in `allowed_file`.
    *   `extractText(self, file_path: str) -> dict`: This is the main function users will call. It performs the following steps:
        1.  Calls `getFileType` to identify the file extension.
        2.  Calls `validateFileType` to ensure the file is supported, raising a `ValueError` if not.
        3.  Uses the `allowed_file` dictionary to find the `class_name` of the correct extractor.
        4.  Dynamically retrieves the instance of the corresponding extractor (e.g., `self.PdfExtractor`).
        5.  Calls the `extractText` method on that specific extractor instance and returns its result.
*   **Role in Workflow**: `FileHandler.py` acts as a facade, hiding the complexity of different file types and their extractors. It ensures that the correct extractor is used for each file. It also includes conditional import logic for `AllowedFile` to enable both direct execution and package import.

### How Everything Orchestrates Together

1.  A user calls `FileHandler().extractText("path/to/document.pdf")`.
2.  `FileHandler` determines the file type ("pdf").
3.  It validates "pdf" against the `allowed_file` dictionary from `AllowedFile.py`.
4.  It retrieves "PdfExtractor" as the `class_name` for "pdf" files.
5.  It gets the `self.PdfExtractor` instance.
6.  It calls `self.PdfExtractor.extractText("path/to/document.pdf")`.
7.  `PdfExtractor` (which adheres to the `Extractor` interface) then uses `PyPDF2` to read the PDF and return the extracted text by page.
8.  This extracted text is then returned back through `FileHandler.extractText` to the original caller.

This modular design ensures clear separation of concerns, making the system easy to understand, maintain, and extend with new file types in the future.
