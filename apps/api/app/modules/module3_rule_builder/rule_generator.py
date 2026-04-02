"""
module3_rule_builder/rule_generator.py
----------------------------------------
Validates, enriches, and saves rules to the RuleStore.
Acts as the gatekeeper between raw LLM output and the database.

Responsibilities:
    - Auto-correct loose entity names to IFC class names
      e.g. "stair" → "IfcStairFlight"
    - Validate required fields, operators, and rule types
    - Save valid rules, skip and log invalid ones
    - Handle both single rules and batches

Usage:
    from module3_rule_builder.rule_generator import RuleGenerator
    from module3_rule_builder.rule_store import RuleStore
    from config import DB_PATH

    store     = RuleStore(DB_PATH)
    generator = RuleGenerator(store)
    generator.save_batch(rules, source_doc="OBC_Part9_PDF")
"""

from config import OBC_TO_IFC_MAP, VALID_OPERATORS, VALID_RULE_TYPES, SOURCE_DOC_PDF


class RuleGenerator:
    """
    Validates, enriches, and saves rules to the RuleStore.
    All LLM output and manual seeds pass through here before DB insertion.
    """

    def __init__(self, rule_store):
        """
        Args:
            rule_store: RuleStore instance to write to
        """
        self.store = rule_store

    # ── PRIVATE HELPERS ───────────────────────────────────────────────────────

    def _enrich_entity_type(self, rule: dict) -> dict:
        """
        Auto-correct plain entity names to proper IFC class names.
        If the LLM returns "stair" instead of "IfcStairFlight", this fixes it.

        Args:
            rule (dict): raw rule dict

        Returns:
            dict: rule with corrected entity_type
        """
        entity = rule.get("entity_type", "")

        # Already a valid IFC class — leave it
        if str(entity).startswith("Ifc"):
            return rule

        # Try to match against the OBC → IFC map
        entity_lower = entity.lower()
        for keyword, ifc_class in OBC_TO_IFC_MAP.items():
            if keyword in entity_lower:
                rule["entity_type"] = ifc_class
                return rule

        # Could not map — leave as-is, validation will catch it
        return rule

    def _validate(self, rule: dict) -> tuple:
        """
        Validate that a rule has all required fields and valid values.

        Args:
            rule (dict): enriched rule dict

        Returns:
            tuple: (is_valid: bool, reason: str)
        """
        # Required fields
        required = ["rule_type", "entity_type", "property_name", "operator"]
        for field in required:
            if not rule.get(field):
                return False, f"Missing required field: '{field}'"

        # Valid operator
        if rule["operator"] not in VALID_OPERATORS:
            return False, f"Invalid operator: '{rule['operator']}' — must be one of {VALID_OPERATORS}"

        # Valid rule type
        if rule["rule_type"] not in VALID_RULE_TYPES:
            return False, f"Invalid rule_type: '{rule['rule_type']}' — must be one of {VALID_RULE_TYPES}"

        # Value required unless operator is 'exists'
        if rule.get("value") is None and rule["operator"] != "exists":
            return False, f"Missing 'value' for operator '{rule['operator']}'"

        # Range check must have [min, max] list
        if rule["operator"] == "between":
            val = rule.get("value")
            if not isinstance(val, list) or len(val) != 2:
                return False, "Operator 'between' requires value as [min, max] list"

        return True, "OK"

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def save_single(self, rule: dict, source_doc: str = SOURCE_DOC_PDF) -> str | None:
        """
        Validate, enrich, and save one rule to the database.

        Args:
            rule       (dict): raw rule dict from LLM or manual seed
            source_doc (str):  label for the source document

        Returns:
            str | None: rule_id if saved, None if invalid
        """
        rule["source_doc"] = source_doc
        rule = self._enrich_entity_type(rule)
        valid, reason = self._validate(rule)

        if valid:
            return self.store.save_rule(rule)
        else:
            ref = rule.get("section_ref", "?")
            desc = rule.get("description", "")[:60]
            print(f"  [SKIPPED] [{ref}] {reason} | {desc}")
            return None

    def save_batch(self, rules: list, source_doc: str = SOURCE_DOC_PDF) -> list:
        """
        Validate and save a list of rules.
        Skips invalid rules and logs the reason.

        Args:
            rules      (list[dict]): list of raw rule dicts
            source_doc (str):        label for the source document

        Returns:
            list[str]: list of saved rule_ids
        """
        saved_ids = []

        for rule in rules:
            rule_id = self.save_single(rule, source_doc)
            if rule_id:
                saved_ids.append(rule_id)

        total    = len(rules)
        saved    = len(saved_ids)
        skipped  = total - saved

        print(f"  [RuleGenerator] Saved {saved}/{total} rules "
              f"({skipped} skipped)")

        return saved_ids
