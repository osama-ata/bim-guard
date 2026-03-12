from abc import ABC, abstractmethod
from typing import List
from app.models.rule_models import Rule
from app.models.compliance_models import ComplianceIssue

class RuleEvaluator(ABC):
    @abstractmethod
    def evaluate(self, ifc_file, rule: Rule) -> List[ComplianceIssue]:
        """
        Evaluate a single rule against an IFC file.
        Returns a list of ComplianceIssue objects if violations are found.
        """
        pass
