from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
from uuid import UUID

class IssueStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"

class ComplianceIssue(BaseModel):
    id: str
    type: str
    element_id: str = Field(..., alias="element_global_id")
    description: str
    viewpoint: Optional[Dict[str, List[float]]] = None
    status: IssueStatus = IssueStatus.OPEN

    model_config = {
        "populate_by_name": True,
    }

class ComplianceSummary(BaseModel):
    critical: int = 0
    warnings: int = 0
    passed: int = 0

class ComplianceCheck(BaseModel):
    id: UUID
    filename: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    summary: Optional[ComplianceSummary] = None
    issues: Optional[List[ComplianceIssue]] = None
    error: Optional[str] = None
