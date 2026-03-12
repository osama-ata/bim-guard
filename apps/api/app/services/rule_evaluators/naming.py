import re
from typing import List
from .base import RuleEvaluator
from app.models.rule_models import Rule
from app.models.compliance_models import ComplianceIssue, IssueStatus

class NamingEvaluator(RuleEvaluator):
    def evaluate(self, ifc_file, rule: Rule) -> List[ComplianceIssue]:
        issues = []
        pattern = rule.logic.get("pattern")
        if not pattern:
            return issues

        try:
            regex = re.compile(pattern)
        except re.error:
            # Log error or handle invalid regex
            return issues

        # Map IFC class from string to ifcopenshell class
        target_class = rule.category # e.g. "IfcWall"
        
        elements = ifc_file.by_type(target_class)
        for element in elements:
            name = getattr(element, "Name", "") or ""
            if not regex.match(name):
                issues.append(ComplianceIssue(
                    id=f"NAME-{element.GlobalId[:6]}",
                    type="NAMING_VIOLATION",
                    element_global_id=element.GlobalId,
                    description=f"Element '{name}' does not match naming convention pattern: {pattern}",
                    status=IssueStatus.OPEN
                ))
        
        return issues
