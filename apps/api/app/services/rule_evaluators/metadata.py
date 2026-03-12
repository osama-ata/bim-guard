from typing import List
from .base import RuleEvaluator
from app.models.rule_models import Rule
from app.models.compliance_models import ComplianceIssue, IssueStatus
import ifcopenshell.util.element

class MetadataEvaluator(RuleEvaluator):
    def evaluate(self, ifc_file, rule: Rule) -> List[ComplianceIssue]:
        issues = []
        required_pset = rule.logic.get("required_pset")
        required_prop = rule.logic.get("required_property")
        expected_val = rule.logic.get("expected_value")

        if not required_pset or not required_prop:
            return issues

        target_class = rule.category
        elements = ifc_file.by_type(target_class)

        for element in elements:
            psets = ifcopenshell.util.element.get_psets(element)
            pset = psets.get(required_pset)
            
            if not pset:
                issues.append(ComplianceIssue(
                    id=f"META-P-{element.GlobalId[:6]}",
                    type="METADATA_MISSING",
                    element_global_id=element.GlobalId,
                    description=f"Missing required Property Set: {required_pset}",
                    status=IssueStatus.OPEN
                ))
                continue

            prop_val = pset.get(required_prop)
            if prop_val is None:
                issues.append(ComplianceIssue(
                    id=f"META-V-{element.GlobalId[:6]}",
                    type="METADATA_MISSING",
                    element_global_id=element.GlobalId,
                    description=f"Missing required Property: {required_prop} in {required_pset}",
                    status=IssueStatus.OPEN
                ))
            elif expected_val is not None and prop_val != expected_val:
                issues.append(ComplianceIssue(
                    id=f"META-E-{element.GlobalId[:6]}",
                    type="METADATA_VALUE_MISMATCH",
                    element_global_id=element.GlobalId,
                    description=f"Property {required_prop} value '{prop_val}' does not match expected: {expected_val}",
                    status=IssueStatus.OPEN
                ))

        return issues
