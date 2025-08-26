from docx import Document
import os
import tempfile

# avoid disrupting the code by import error 
try:
    from .Extractor import Extractor
except ImportError:
    from Extractor import Extractor

class DocxExtractor(Extractor):
    # Override
    def extractText(self, relative_path: str) -> dict:
        full_path = os.path.abspath(relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")

        try:
            return self._extract_via_pdf_conversion(full_path)
        except Exception as e:
            print(f"PDF conversion failed, using fallback method: {e}")
            return self._extract_direct_docx(full_path)

    def _extract_via_pdf_conversion(self, full_path: str) -> dict:
        """
        Extract text by converting DOCX to PDF first, then extracting by pages.
        This gives true page boundaries as they appear in Word.
        """
        try:
            from docx2pdf import convert
            import fitz  # PyMuPDF
        except ImportError as e:
            raise ImportError(
                f"Required libraries not installed: {e}\n"
                "Install with: pip install docx2pdf PyMuPDF"
            )

        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf_path = temp_pdf.name

        try:
            # Convert DOCX to PDF
            convert(full_path, temp_pdf_path)
            
            if not os.path.exists(temp_pdf_path):
                raise FileNotFoundError("PDF conversion failed - no output file created")

            # Extract text from PDF by pages
            extracted_text_by_page = {}
            pdf_document = fitz.open(temp_pdf_path)

            total_pages = pdf_document.page_count

            for page_num in range(total_pages):
                page = pdf_document[page_num]
                text = page.get_text()
                extracted_text_by_page[page_num + 1] = text.strip()

            pdf_document.close()
            
            # Ensure we have at least one page
            if not extracted_text_by_page:
                extracted_text_by_page[1] = ""

            return extracted_text_by_page

        finally:
            # Clean up temporary PDF file
            if os.path.exists(temp_pdf_path):
                try:
                    os.unlink(temp_pdf_path)
                except:
                    pass  # Ignore cleanup errors

    def _extract_direct_docx(self, full_path: str) -> dict:
        """
        Fallback method: Extract text directly from DOCX using character estimation.
        Used when PDF conversion is not available.
        """
        doc = Document(full_path)
        
        # Get all paragraphs with text
        all_paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                all_paragraphs.append(text)
        
        if not all_paragraphs:
            return {1: ""}
        
        # Use character-based estimation (roughly 2000 chars per page)
        chars_per_page = 2000
        extracted_text_by_page = {}
        current_page = 1
        current_content = []
        current_char_count = 0
        
        for para_text in all_paragraphs:
            para_length = len(para_text)
            
            # If adding this paragraph would exceed the page limit
            if current_char_count + para_length > chars_per_page and current_content:
                # Store current page
                extracted_text_by_page[current_page] = "\n".join(current_content)
                current_page += 1
                current_content = [para_text]
                current_char_count = para_length
            else:
                # Add to current page
                current_content.append(para_text)
                current_char_count += para_length + 1  # +1 for newline
        
        # Handle last page
        if current_content:
            extracted_text_by_page[current_page] = "\n".join(current_content)
        
        return extracted_text_by_page

# Simplified testing
if __name__ == "__main__":
    handler = DocxExtractor()
    try:
        # Update this path to your actual test file
        text_by_page = handler.extractText("test_file/docx/demo.docx")
        
        print(f"Successfully extracted {len(text_by_page)} pages")
        for page_num, content in text_by_page.items():
            print(page_num)
            print(content)
            print("=" * 120)
            
    except Exception as e:
        print(f"Extraction failed: {e}")