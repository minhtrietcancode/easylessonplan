allowed_file = {
    # pdf file 
    "pdf" : {
        "handler_relative_path" : "backend/file_handler/all_file_types_handler/pdf_extractor.py",
        "class_name" : "PdfHandler"
    },

    # docx - ms word file
    "docx" : {
        "handler_relative_path" : "backend/file_handler/all_file_types_handler/docx_extractor.py",
        "class_name" : "DocxHandler"
    }
}