from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID

class RuleType(str, Enum):
    METADATA = "METADATA"
    SPATIAL = "SPATIAL"
    NOMENCLATURE = "NOMENCLATURE"

class Rule(BaseModel):
    id: UUID
    document_id: UUID
    category: str
    type: RuleType
    logic: Dict[str, Any]
    confidence: float
    source_text: Optional[str] = None
    is_approved: bool = False

class RuleSet(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    version: str = "1.0"
    categories: List[str]
    rule_count: int
    target_classes: List[str]
