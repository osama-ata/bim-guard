"""
tests/test_module3.py
----------------------
Unit tests for Module 3 — RuleGenerator (NLP/LLM path), RuleStore,
rule schema validation, and edge cases.

Run with: pytest tests/test_module3.py -v

These tests cover the CORE LLM path that test_module1.py doesn't touch:
  raw text chunk → NLP Engine → structured JSON/Regex rules

Tests marked @pytest.mark.llm call the actual LLM and may be slow/costly.
Run them selectively:  pytest tests/test_module3.py -m llm -v
Skip them:             pytest tests/test_module3.py -m "not llm" -v
"""

import os
import json
import pytest

from module3_rule_builder.rule_store     import RuleStore
from module3_rule_builder.rule_generator import RuleGenerator

TEST_DB = "tests/test_rules_m3.db"


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def store():
    s = RuleStore(TEST_DB)
    s.clear_all_rules()
    yield s
    s.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def gen(store):
    return RuleGenerator(store)


# ═══════════════════════════════════════════════════════════════════════════════
# RuleStore basic operations
# ═══════════════════════════════════════════════════════════════════════════════

def test_store_starts_empty(store):
    assert store.count() == 0

def test_store_save_and_retrieve(store):
    rule = {
        "element":  "stair",
        "property": "clear_width",
        "operator": ">=",
        "value":    860,
        "unit":     "mm",
        "source":   "OBC 9.8.2.1",
    }
    store.save_rule(rule)
    assert store.count() == 1

    rules = store.get_all_rules()
    assert len(rules) == 1

def test_store_clear(store):
    store.save_rule({"element": "stair", "property": "width",
                     "operator": ">=", "value": 860})
    store.save_rule({"element": "door", "property": "width",
                     "operator": ">=", "value": 810})
    assert store.count() == 2
    store.clear_all_rules()
    assert store.count() == 0

def test_store_handles_duplicate_rules(store):
    """Saving the same rule twice should not crash (behavior may vary)."""
    rule = {"element": "stair", "property": "width",
            "operator": ">=", "value": 860}
    store.save_rule(rule)
    store.save_rule(rule)
    assert store.count() >= 1  # at least doesn't crash


# ═══════════════════════════════════════════════════════════════════════════════
# Rule schema validation helper
# ═══════════════════════════════════════════════════════════════════════════════

REQUIRED_RULE_FIELDS = {"element", "property", "operator", "value"}
VALID_OPERATORS      = {">=", "<=", "==", "!=", ">", "<", "between",
                        "in", "not_in", "contains", "matches"}

def validate_rule_schema(rule_data):
    """Returns list of issues. Empty list = valid."""
    issues = []
    if isinstance(rule_data, str):
        try:
            rule_data = json.loads(rule_data)
        except json.JSONDecodeError:
            return ["Rule is not valid JSON"]

    missing = REQUIRED_RULE_FIELDS - set(rule_data.keys())
    if missing:
        issues.append(f"Missing fields: {missing}")

    if "operator" in rule_data:
        op = rule_data["operator"]
        if op not in VALID_OPERATORS:
            issues.append(f"Unknown operator: '{op}'")

    if "value" in rule_data:
        val = rule_data["value"]
        if val is None or val == "":
            issues.append("Value is empty or None")

    if "element" in rule_data:
        el = rule_data["element"]
        if not el or not isinstance(el, str):
            issues.append(f"Invalid element: '{el}'")

    return issues


# ═══════════════════════════════════════════════════════════════════════════════
# RuleGenerator — LLM path tests
# ═══════════════════════════════════════════════════════════════════════════════
#
# These test the core NLP pipeline: text → LLM → structured rules
# They call the real LLM, so mark them accordingly.

# ── Golden test cases: (input text, expected rule properties) ──
GOLDEN_CASES = [
    {
        "id": "stair_width",
        "text": "Every exit stair shall have a clear width of not less than 860 mm.",
        "expect": {
            "element":  "stair",
            "property": "clear_width",
            "operator": ">=",
            "value":    860,
            "unit":     "mm",
        },
    },
    {
        "id": "riser_height_range",
        "text": "The riser height shall be not less than 125 mm and not more than 200 mm.",
        "expect": {
            "element":  "stair",
            "property": "riser_height",
            "value_min": 125,
            "value_max": 200,
            "unit":      "mm",
        },
    },
    {
        "id": "guard_height",
        "text": "Guards shall be not less than 900 mm in height measured vertically.",
        "expect": {
            "element":  "guard",
            "property": "height",
            "operator": ">=",
            "value":    900,
            "unit":     "mm",
        },
    },
    {
        "id": "door_width",
        "text": "Every doorway in a means of egress shall have a clear width of not less than 810 mm.",
        "expect": {
            "element":  "door",
            "property": "clear_width",
            "operator": ">=",
            "value":    810,
            "unit":     "mm",
        },
    },
    {
        "id": "window_egress",
        "text": "Each window providing emergency egress shall have an unobstructed opening of not less than 0.35 m2.",
        "expect": {
            "element":  "window",
            "property": "opening_area",
            "operator": ">=",
            "value":    0.35,
            "unit":     "m2",
        },
    },
]


@pytest.mark.llm
class TestRuleGeneratorLLM:
    """
    Tests that call the actual LLM to generate rules.
    Run with:  pytest tests/test_module3.py -m llm -v
    """

    @pytest.mark.parametrize("case", GOLDEN_CASES, ids=[c["id"] for c in GOLDEN_CASES])
    def test_golden_case_produces_valid_rule(self, gen, store, case):
        """LLM should produce at least one structurally valid rule."""
        rules = gen.generate_rules(case["text"])

        assert len(rules) >= 1, \
            f"[{case['id']}] No rules generated from: {case['text'][:60]}..."

        # Validate schema of every generated rule
        for rule in rules:
            rule_data = rule if isinstance(rule, dict) else json.loads(rule)
            issues    = validate_rule_schema(rule_data)
            assert not issues, \
                f"[{case['id']}] Schema issues: {issues} — rule: {rule_data}"

    @pytest.mark.parametrize("case", GOLDEN_CASES, ids=[c["id"] for c in GOLDEN_CASES])
    def test_golden_case_correct_element(self, gen, store, case):
        """Generated rule should reference the correct building element."""
        rules     = gen.generate_rules(case["text"])
        rule_data = rules[0] if isinstance(rules[0], dict) else json.loads(rules[0])

        expected_el = case["expect"]["element"].lower()
        actual_el   = rule_data.get("element", "").lower()

        assert expected_el in actual_el or actual_el in expected_el, \
            f"[{case['id']}] Expected element '{expected_el}', got '{actual_el}'"

    @pytest.mark.parametrize("case", GOLDEN_CASES, ids=[c["id"] for c in GOLDEN_CASES])
    def test_golden_case_correct_value(self, gen, store, case):
        """Generated rule should capture the correct numeric threshold."""
        rules     = gen.generate_rules(case["text"])
        rule_data = rules[0] if isinstance(rules[0], dict) else json.loads(rules[0])

        if "value" in case["expect"]:
            expected_val = case["expect"]["value"]
            actual_val   = rule_data.get("value")
            # Allow numeric comparison with tolerance
            try:
                assert abs(float(actual_val) - float(expected_val)) < 0.01, \
                    f"[{case['id']}] Expected value {expected_val}, got {actual_val}"
            except (TypeError, ValueError):
                pytest.fail(
                    f"[{case['id']}] Could not compare values: "
                    f"expected={expected_val}, actual={actual_val}"
                )

    def test_llm_handles_ambiguous_text(self, gen, store):
        """Vague requirements should either produce a flagged rule or no rule."""
        vague_text = "Adequate ventilation shall be provided in all occupied spaces."
        rules = gen.generate_rules(vague_text)
        # Either: no rule (acceptable) or a rule flagged as needing review
        if rules:
            rule_data = rules[0] if isinstance(rules[0], dict) else json.loads(rules[0])
            # Should NOT have invented a specific numeric threshold
            val = rule_data.get("value")
            if val is not None:
                # If it did produce a value, it should be flagged
                assert rule_data.get("needs_review") or rule_data.get("confidence") == "low", \
                    f"LLM invented threshold '{val}' for vague requirement without flagging"

    def test_llm_handles_multiple_requirements_in_one_chunk(self, gen, store):
        """A text chunk with 2 requirements should produce ~2 rules."""
        multi_text = (
            "The riser height shall not be more than 200 mm. "
            "The tread run shall not be less than 255 mm."
        )
        rules = gen.generate_rules(multi_text)
        assert len(rules) >= 2, \
            f"Expected ≥2 rules from 2 requirements, got {len(rules)}"

    def test_llm_empty_input(self, gen, store):
        """Empty string should return no rules, not crash."""
        rules = gen.generate_rules("")
        assert rules == [] or rules is None


# ═══════════════════════════════════════════════════════════════════════════════
# RuleGenerator — Non-LLM / deterministic tests
# ═══════════════════════════════════════════════════════════════════════════════
#
# These test regex/SHACL generation paths if your RuleGenerator has them.

class TestRuleGeneratorDeterministic:

    def test_generate_regex_from_text(self, gen):
        """If RuleGenerator has a regex builder, test it here."""
        if not hasattr(gen, "generate_regex_from_text"):
            pytest.skip("No regex generation method")
        pattern = gen.generate_regex_from_text("clear width", ">=", "860", "mm")
        assert pattern is not None
        assert "860" in pattern

    def test_build_shacl_shapes(self, gen):
        """If RuleGenerator has SHACL output, test it here."""
        if not hasattr(gen, "build_shacl_shapes"):
            pytest.skip("No SHACL generation method")
        rule = {"element": "stair", "property": "clear_width",
                "operator": ">=", "value": 860, "unit": "mm"}
        shapes = gen.build_shacl_shapes([rule])
        assert shapes is not None

    def test_rules_saved_to_store(self, gen, store):
        """After generation, rules should be persisted in the store."""
        if not hasattr(gen, "generate_and_save"):
            pytest.skip("No generate_and_save method")
        gen.generate_and_save("Every stair shall have a width of 860 mm.")
        assert store.count() >= 1


# ═══════════════════════════════════════════════════════════════════════════════
# Snapshot regression for Module 3
# ═══════════════════════════════════════════════════════════════════════════════

SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "snapshots")

@pytest.mark.llm
class TestModule3Snapshots:

    def _snapshot_path(self, name):
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
        return os.path.join(SNAPSHOTS_DIR, f"m3_{name}.json")

    def test_stair_width_rule_snapshot(self, gen, store):
        text  = "Every exit stair shall have a clear width of not less than 860 mm."
        rules = gen.generate_rules(text)

        snap_file = self._snapshot_path("stair_width")
        current   = [r if isinstance(r, dict) else json.loads(r) for r in rules]

        if not os.path.exists(snap_file):
            with open(snap_file, "w") as f:
                json.dump(current, f, indent=2)
            pytest.skip("Snapshot created — re-run to verify")

        with open(snap_file) as f:
            expected = json.load(f)

        assert len(current) == len(expected), \
            f"Rule count changed: {len(expected)} → {len(current)}"

        for got, exp in zip(current, expected):
            assert got.get("element")  == exp.get("element"),  "Element changed"
            assert got.get("operator") == exp.get("operator"), "Operator changed"
            # Allow small numeric drift
            if "value" in exp:
                assert abs(float(got.get("value", 0)) - float(exp["value"])) < 1, \
                    f"Value drifted: {exp['value']} → {got.get('value')}"
