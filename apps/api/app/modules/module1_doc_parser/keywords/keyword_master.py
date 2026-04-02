"""
module1_doc_parser/keywords/keyword_master.py
-----------------------------------------------
Master keyword list for BIMGuard OBC compliance rule detection.
193 keywords across 12 groups with weighted scoring.

Sources:
    - CODE-ACCORD (Nature 2025)   — deontic, permissive, exemption language
    - SPaR.txt (ACL 2021)         — multi-word expressions in building regulations
    - ScienceDirect (2024)        — OBC-specific terms
    - ontario.ca (real OBC text)  — actual OBC phrasing patterns
"""

# ── GROUP 1: OBLIGATION / MANDATE  (weight 3) ─────────────────────────────────
OBLIGATION_KEYWORDS = [
    "shall", "shall not", "must", "must not", "should", "should not",
    "required", "is required", "are required", "requirement",
]

# ── GROUP 2: COMPLIANCE / CONFORMANCE  (weight 2) ────────────────────────────
COMPLIANCE_KEYWORDS = [
    "comply", "complies", "compliance", "conform", "conforms", "conforming",
    "meet", "meets", "meeting",
]

# ── GROUP 3: THRESHOLD / LIMIT  (weight 5) ───────────────────────────────────
THRESHOLD_KEYWORDS = [
    "minimum", "maximum", "min", "max",
    "not less than", "not more than", "no less than", "no more than",
    "at least", "at most", "exceed", "exceeds", "shall not exceed",
    "does not exceed", "less than", "greater than", "between", "within",
]

# ── GROUP 4: CONDITIONAL  (weight 1) ─────────────────────────────────────────
CONDITIONAL_KEYWORDS = [
    "if", "where", "when", "unless", "except",
    "provided that", "in the case of", "subject to",
]

# ── GROUP 5: UNITS  (weight 5) ────────────────────────────────────────────────
UNIT_KEYWORDS = [
    "mm", "m2", "metres", "meters", "degrees",
    "percent", "%", "ratio", "kpa", "mpa",
]

# ── GROUP 6: ELEMENT PROPERTIES  (weight 4) ───────────────────────────────────
PROPERTY_KEYWORDS = [
    "width", "height", "depth", "length", "area", "clearance", "clear",
    "opening", "slope", "rise", "run", "tread", "riser", "nosing",
    "rating", "separation", "distance", "travel distance", "egress",
    "load", "capacity", "thickness", "dimension", "size",
]

# ── GROUP 7: BUILDING ELEMENT NAMES  (weight 3) ───────────────────────────────
ELEMENT_KEYWORDS = [
    "stair", "stairs", "stairway", "flight", "landing", "winder",
    "ramp", "door", "window", "guard", "handrail", "railing",
    "wall", "floor", "ceiling", "roof", "balcony", "garage",
    "corridor", "exit", "room", "space", "dwelling", "suite",
    "storey", "basement", "mezzanine",
    "occupancy", "assembly", "foundation", "column",
]

# ── GROUP 8: FIRE / SAFETY  (weight 4) ────────────────────────────────────────
FIRE_SAFETY_KEYWORDS = [
    "fire", "fire rating", "fire separation", "fire resistance",
    "smoke", "smoke alarm", "sprinkler", "protected",
    "noncombustible", "combustible", "flame spread",
]

# ── GROUP 9: BIGRAMS AND KEY PHRASES  (weight 6 — highest) ───────────────────
BIGRAM_PHRASES = sorted([
    "shall be", "shall have", "shall not be", "must be", "must not be",
    "should be", "should not be", "is not permitted", "are not permitted", "is permitted",
    "not less than", "not more than", "no less than", "no more than",
    "shall not exceed", "does not exceed", "at least one", "at minimum", "at maximum",
    "comply with", "conform to", "in accordance with", "as required by",
    "meet the requirements", "subject to the requirements",
    "provided that", "in the case of", "where required", "where applicable",
    "if located", "if used", "except where", "unless otherwise",
    "clear width", "clear height", "clear opening", "floor area",
    "ceiling height", "travel distance", "fire rating", "fire separation",
    "limiting distance", "headroom clearance",
    "fire-resistance rating", "floor assembly", "exterior wall",
    "unobstructed path", "path of travel", "ground level", "floor level",
    "occupant load", "means of egress",
], key=len, reverse=True)

# ── GROUP 10: PERMISSIVE / EXEMPTION  (weight 4) — NEW ───────────────────────
PERMISSIVE_KEYWORDS = [
    "may", "may be used", "may be required", "may be considered",
    "may terminate", "is permitted to", "shall be permitted",
    "need not", "need not be", "is exempt", "is exempted", "does not apply",
]

# ── GROUP 11: DEEMED / ACCEPTABLE COMPLIANCE  (weight 5) — NEW ───────────────
DEEMED_KEYWORDS = [
    "deemed to comply", "is deemed", "deemed acceptable",
    "acceptable solution", "alternative solution", "compliance alternative",
]

# ── GROUP 12: HARD PROHIBITION  (weight 5) — NEW ─────────────────────────────
PROHIBITION_KEYWORDS = [
    "prohibited", "is prohibited", "prohibit", "not allowed", "not acceptable",
]

# ── MASTER FLAT LISTS ─────────────────────────────────────────────────────────
ALL_SINGLE_KEYWORDS = (
    OBLIGATION_KEYWORDS   + COMPLIANCE_KEYWORDS  + THRESHOLD_KEYWORDS  +
    CONDITIONAL_KEYWORDS  + UNIT_KEYWORDS         + PROPERTY_KEYWORDS   +
    ELEMENT_KEYWORDS      + FIRE_SAFETY_KEYWORDS  +
    PERMISSIVE_KEYWORDS   + DEEMED_KEYWORDS        + PROHIBITION_KEYWORDS
)

ALL_KEYWORDS = ALL_SINGLE_KEYWORDS + BIGRAM_PHRASES

# ── WEIGHT MAP ────────────────────────────────────────────────────────────────
KEYWORD_WEIGHTS: dict = {}
for _kw in OBLIGATION_KEYWORDS:   KEYWORD_WEIGHTS[_kw] = 3
for _kw in COMPLIANCE_KEYWORDS:   KEYWORD_WEIGHTS[_kw] = 2
for _kw in THRESHOLD_KEYWORDS:    KEYWORD_WEIGHTS[_kw] = 5
for _kw in CONDITIONAL_KEYWORDS:  KEYWORD_WEIGHTS[_kw] = 1
for _kw in UNIT_KEYWORDS:         KEYWORD_WEIGHTS[_kw] = 5
for _kw in PROPERTY_KEYWORDS:     KEYWORD_WEIGHTS[_kw] = 4
for _kw in ELEMENT_KEYWORDS:      KEYWORD_WEIGHTS[_kw] = 3
for _kw in FIRE_SAFETY_KEYWORDS:  KEYWORD_WEIGHTS[_kw] = 4
for _kw in BIGRAM_PHRASES:        KEYWORD_WEIGHTS[_kw] = 6
for _kw in PERMISSIVE_KEYWORDS:   KEYWORD_WEIGHTS[_kw] = 4
for _kw in DEEMED_KEYWORDS:       KEYWORD_WEIGHTS[_kw] = 5
for _kw in PROHIBITION_KEYWORDS:  KEYWORD_WEIGHTS[_kw] = 5
