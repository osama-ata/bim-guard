import re
from typing import List, Dict, Any
from uuid import uuid4
from ...models.rule_models import RuleType

class RuleBuilder:
    """
    Module 3: Rule Builder
    Simulates AI extraction of rules from text.
    In a real implementation, this would call an LLM.
    """
    def extract_rules_mock(self, text: str) -> List[Dict[str, Any]]:
        """
        Mock extraction using regex patterns to find potential rules.
        """
        rules = []
        
        # Look for naming patterns
        naming_matches = re.finditer(r"naming convention.*?(?P<pattern>[A-Z0-9\-\*\.]+)", text, re.IGNORECASE)
        for match in naming_matches:
            rules.append({
                "temp_id": str(uuid4()),
                "category": "IfcElement",
                "type": RuleType.NOMENCLATURE,
                "logic": {"pattern": match.group("pattern")},
                "confidence": 0.85,
                "source_text": match.group(0)
            })

        # Look for dimension patterns (e.g. minimum width 810mm)
        dim_matches = re.finditer(r"minimum (?P<dim>width|height|run|rise) (?P<val>\d+)mm", text, re.IGNORECASE)
        for match in dim_matches:
            rules.append({
                "temp_id": str(uuid4()),
                "category": "IfcElement", # Default Class
                "type": RuleType.SPATIAL,
                "logic": {f"min_{match.group('dim').lower()}": int(match.group('val'))},
                "confidence": 0.9,
                "source_text": match.group(0)
            })

        return rules
