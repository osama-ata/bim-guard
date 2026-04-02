"""
module1_doc_parser/section_chunker.py
---------------------------------------
Step 3 — Splits Docling markdown text into 13 OBC section chunks.
Detects Docling markdown headings (# 4 Stairs) first,
falls back to plain text heading detection.

Usage:
    from module1_doc_parser.section_chunker import SectionChunker
    chunker = SectionChunker()
    chunks  = chunker.chunk(docling_text)
"""

import re

OBC_SECTION_HEADINGS = [
    "1","2","3","4","5","6","7","8","9","10","11","12","13"
]

OBC_SECTION_NAMES = {
    "1":  "Building Basics",
    "2":  "Means of Egress and Exit Paths",
    "3":  "Doors (Detailed)",
    "4":  "Stairs (Detailed - Part 9)",
    "5":  "Ramps",
    "6":  "Guards and Handrails",
    "7":  "Windows and Glazing",
    "8":  "Washrooms and Basic Accessibility",
    "9":  "Plumbing Fixture Counts",
    "10": "Fire Protection",
    "11": "Garage and Carport",
    "12": "Spatial Separation to Property Line",
    "13": "Model QA",
}

MD_HEADING  = re.compile(r"^#{1,3}\s+(1[0-3]|[1-9])\s+.+")
TXT_HEADING = re.compile(r"^(1[0-3]|[1-9])[\s\.].+")


class SectionChunker:

    def _detect_section(self, line: str):
        s = line.strip()
        if MD_HEADING.match(s):
            m = re.search(r"(1[0-3]|[1-9])", s)
            return m.group(1) if m else None
        if TXT_HEADING.match(s):
            m = re.match(r"^(1[0-3]|[1-9])", s)
            if m:
                candidate = m.group(1)
                if s[len(candidate):len(candidate)+1] == " ":
                    return candidate
        return None

    def chunk(self, full_text: str) -> list:
        lines         = full_text.split("\n")
        chunks        = []
        current_num   = None
        current_lines = []

        for line in lines:
            num = self._detect_section(line)
            if num and num in OBC_SECTION_HEADINGS:
                if current_num and current_lines:
                    text = "\n".join(current_lines).strip()
                    chunks.append({
                        "section_number": current_num,
                        "section_name":   OBC_SECTION_NAMES.get(current_num, "Unknown"),
                        "text":           text,
                        "char_count":     len(text),
                    })
                current_num   = num
                current_lines = [line.strip()]
            elif current_num:
                current_lines.append(line.strip())

        if current_num and current_lines:
            text = "\n".join(current_lines).strip()
            chunks.append({
                "section_number": current_num,
                "section_name":   OBC_SECTION_NAMES.get(current_num, "Unknown"),
                "text":           text,
                "char_count":     len(text),
            })

        print(f"[SectionChunker] {len(chunks)} sections detected")
        for c in chunks:
            print(f"  {c['section_number']:<4} {c['section_name']:<40} {c['char_count']:>8,} chars")

        return chunks
