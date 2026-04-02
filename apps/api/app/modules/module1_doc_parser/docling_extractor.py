"""
module1_doc_parser/docling_extractor.py
-----------------------------------------
Step 1 — PDF extraction using Docling (IBM, MIT license).
Extracts both prose text and tables in one call.

Install: pip install docling
First run downloads vision models (~2 min, one-time only).

Usage:
    from module1_doc_parser.docling_extractor import DoclingExtractor
    extractor = DoclingExtractor()
    text, tables = extractor.extract("data/input_docs/OBC_Part9.pdf")
"""

from pathlib import Path


class DoclingExtractor:
    """
    Wraps Docling DocumentConverter to extract prose text
    and tables from an OBC PDF in a single call.
    """

    def __init__(self):
        try:
            from docling.document_converter import DocumentConverter
            self.converter = DocumentConverter()
            print("[DoclingExtractor] Ready")
        except ImportError:
            raise ImportError(
                "Docling not installed. Run: pip install docling"
            )

    def extract(self, pdf_path: str) -> tuple:
        """
        Extract text and tables from a PDF.

        Args:
            pdf_path (str): path to the OBC PDF

        Returns:
            text   (str):        full markdown text in reading order
            tables (list[dict]): each table as a dict with a DataFrame
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        print(f"[DoclingExtractor] Converting: {pdf_path.name}")

        result = self.converter.convert(str(pdf_path))

        # Full prose text as clean markdown
        text = result.document.export_to_markdown()

        # Tables as DataFrames — critical OBC tables come out clean
        tables = []
        for i, table in enumerate(result.document.tables):
            df = table.export_to_dataframe()
            tables.append({
                "table_index": i,
                "dataframe":   df,
                "row_count":   len(df),
                "col_count":   len(df.columns),
            })

        print(f"[DoclingExtractor] Done — {len(text):,} chars, {len(tables)} tables")
        return text, tables
