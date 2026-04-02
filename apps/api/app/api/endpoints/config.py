"""
config.py
---------
Single source of truth for all BIMGuard paths and settings.
Every module imports from here — no hardcoded paths anywhere else.

Usage:
    from config import DB_PATH, OPENAI_API_KEY, OBC_SECTION_NAMES
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# ── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
INPUT_DIR   = DATA_DIR / "input_docs"    # uploaded OBC PDFs go here
IFC_DIR     = DATA_DIR / "ifc_models"    # uploaded IFC files go here
REPORTS_DIR = DATA_DIR / "reports"       # BCF / CSV / PDF outputs

# Database paths
DB_PATH         = DATA_DIR / "rules.db"
COMPLIANCE_DB   = DATA_DIR / "compliance.db"

# Ensure data directories exist on import
for _dir in [DATA_DIR, INPUT_DIR, IFC_DIR, REPORTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── API KEYS ─────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── SOURCE DOCUMENT LABELS ───────────────────────────────────────────────────
SOURCE_DOC_PDF    = "OBC_Part9_PDF"
SOURCE_DOC_TABLE  = "OBC_Table_Direct"
SOURCE_DOC_SEED   = "OBC_Part9_Seed"

# ── OBC SECTION DEFINITIONS ──────────────────────────────────────────────────
OBC_SECTION_HEADINGS = [
    "1", "2", "3", "4", "5", "6",
    "7", "8", "9", "10", "11", "12", "13"
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

# ── KEYWORD FILTER SETTINGS ───────────────────────────────────────────────────
CONFIDENCE_HIGH   = 10   # score >= 10  → HIGH
CONFIDENCE_MEDIUM = 1    # score >= 1   → MEDIUM
CONFIDENCE_LOW    = 0    # score == 0   → LOW_CONFIDENCE (flagged, still sent)

# ── IFC ENTITY MAP ────────────────────────────────────────────────────────────
OBC_TO_IFC_MAP = {
    "stair":     "IfcStairFlight",
    "step":      "IfcStairFlight",
    "door":      "IfcDoor",
    "window":    "IfcWindow",
    "landing":   "IfcSlab",
    "ramp":      "IfcRamp",
    "guard":     "IfcRailing",
    "handrail":  "IfcRailing",
    "railing":   "IfcRailing",
    "room":      "IfcSpace",
    "space":     "IfcSpace",
    "wall":      "IfcWall",
    "garage":    "IfcZone",
    "floor":     "IfcSlab",
    "balcony":   "IfcSlab",
    "column":    "IfcColumn",
    "foundation":"IfcFooting",
    "occupancy": "IfcSpace",
}

# ── RULE VALIDATION ───────────────────────────────────────────────────────────
VALID_OPERATORS  = {">=", "<=", "==", "!=", "between", "regex_match", "exists"}
VALID_RULE_TYPES = {"json_check", "range_check", "regex", "shacl", "exists_check"}
