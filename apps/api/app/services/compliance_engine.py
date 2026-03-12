import ifcopenshell
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from app.models.rule_models import Rule, RuleType
from app.models.compliance_models import ComplianceCheck, ComplianceIssue, ComplianceSummary
from app.services.rule_evaluators.naming import NamingEvaluator
from app.services.rule_evaluators.metadata import MetadataEvaluator
from app.services.rule_evaluators.geometric import GeometricEvaluator

class ComplianceEngine:
    def __init__(self):
        self.evaluators = {
            RuleType.NOMENCLATURE: NamingEvaluator(),
            RuleType.METADATA: MetadataEvaluator(),
            RuleType.SPATIAL: GeometricEvaluator(),
        }

    def run_check(self, ifc_path: Path, rules: List[Rule]) -> ComplianceCheck:
        ifc_file = ifcopenshell.open(str(ifc_path))
        all_issues = []
        
        for rule in rules:
            evaluator = self.evaluators.get(rule.type)
            if evaluator:
                issues = evaluator.evaluate(ifc_file, rule)
                all_issues.extend(issues)

        # Basic summary calculation
        summary = ComplianceSummary(
            critical=len([i for i in all_issues if "VIOLATION" in i.type]),
            warnings=len([i for i in all_issues if "MISSING" in i.type]),
            passed=0 # Needs actual element count logic for accuracy
        )

        from uuid import uuid4

        return ComplianceCheck(
            id=uuid4(),  # generate a unique ID for each check rather than reusing rule document
            filename=ifc_path.name,
            status="completed",
            created_at=datetime.now(),
            completed_at=datetime.now(),
            summary=summary,
            issues=all_issues
        )
