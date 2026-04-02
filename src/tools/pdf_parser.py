import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads a PDF from disk and extracts the text.
    Raises a FileNotFoundError if the document is missing,
    or a RuntimeError if parsing fails.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found at {file_path}")
        
    try:
        doc = fitz.open(file_path)
        
        # Extract text from each page and combine them. 
        # chr(12) is the standard form-feed character representing a page break.
        full_text = chr(12).join([page.get_text() for page in doc])
        doc.close()
        
        return full_text
        
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF {file_path}: {str(e)}")