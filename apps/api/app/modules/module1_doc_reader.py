import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional

class DocReader:
    """
    Module 1: Document Reader
    Extracts text from PDF documents (BEPs, Building Codes).
    """
    def extract_text(self, file_path: Path) -> str:
        """
        Extract full text from a PDF file.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        full_text = ""
        try:
            doc = fitz.open(str(file_path))
            for page in doc:
                full_text += page.get_text()
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {str(e)}")

        return full_text
