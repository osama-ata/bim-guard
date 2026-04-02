"""
tests/test_integration.py
--------------------------
End-to-end integration tests: PDF → Module 1 → Module 3 → validated rules.

Run with: pytest tests/test_integration.py -v -m integration
These tests require:
  1. Real PDF fixtures in tests/fixtures/
  2. LLM access for Module 3

SETUP:
  Place your test PDFs in tests/fixtures/ and update INTEGRATION_CASES below.
"""

import os
import json
import time
import pytest

from module1_doc_parser.section_chunker    import SectionChunker
from module1_doc_parser.keyword_filter     import KeywordFilter
from module1_doc_parser.table_rule_builder import TableRuleBuilder
from module3_rule_builder.rule_store       import RuleStore
from module3_rule_builder.rule_generator   import RuleGenerator

TEST_DB      = "tests/test_rules_integration.db"
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
RESULTS_DIR  = os.path.join(os.path.dirname(__file__), "integration_results")


# ═══════════════════════════════════════════════════════════════════════════════
# Integration test cases — CUSTOMIZE THESE FOR YOUR PDFS
# ═══════════════════════════════════════════════════════════════════════════════
#
# Each case maps a fixture PDF to what you expect the pipeline to produce.
# This is your "golden dataset."

INTEGRATION_CASES = [
    {
        "id":   "obc_stairs",
        "pdf":  "sample_obc_stairs.pdf",
        "description": "OBC Part 9 — Stairs section",
        # Module 1 expectations
        "expect_sections": ["4"],         # section numbers that should appear
        "expect_terms":    ["stair", "shall", "860", "mm"],
        "min_chunks":      1,
        # Module 3 expectations
        "expect_rules_min":    1,
        "expect_elements":     ["stair"],
        "expect_values":       [860],     # numeric thresholds that should appear
    },
    # ── Add more cases as you add fixture PDFs ──
    # {
    #     "id":   "obc_fire_safety",
    #     "pdf":  "sample_obc_fire.pdf",
    #     "expect_sections": ["3"],
    #     "expect_terms":    ["fire", "rating", "hour"],
    #     "min_chunks":      1,
    #     "expect_rules_min":    2,
    #     "expect_elements":     ["wall", "door"],
    #     "expect_values":       [45, 60],
    # },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def pipeline():
    """Set up the full Module 1 → Module 3 pipeline."""
    store   = RuleStore(TEST_DB)
    store.clear_all_rules()
    chunker = SectionChunker()
    kf      = KeywordFilter()
    gen     = RuleGenerator(store)
    builder = TableRuleBuilder(store)

    yield {
        "store":   store,
        "chunker": chunker,
        "kf":      kf,
        "gen":     gen,
        "builder": builder,
    }

    store.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


@pytest.fixture
def docling_extractor():
    try:
        from module1_doc_parser.docling_extractor import DoclingExtractor
        return DoclingExtractor()
    except ImportError:
        pytest.skip("DoclingExtractor not available")


def _has_fixture(pdf_name):
    return os.path.exists(os.path.join(FIXTURES_DIR, pdf_name))


# ═══════════════════════════════════════════════════════════════════════════════
# Full pipeline integration tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.llm
class TestFullPipeline:

    @pytest.mark.parametrize("case", INTEGRATION_CASES, ids=[c["id"] for c in INTEGRATION_CASES])
    def test_pipeline_end_to_end(self, case, pipeline, docling_extractor):
        """
        Full pipeline: PDF → extract → chunk → filter → generate rules → validate.
        """
        pdf_path = os.path.join(FIXTURES_DIR, case["pdf"])
        if not os.path.exists(pdf_path):
            pytest.skip(f"Fixture not found: {case['pdf']}")

        # ── Step 1: Extract text from PDF (Module 1 — DoclingExtractor) ──
        result = docling_extractor.extract(pdf_path)
        text   = result if isinstance(result, str) else result.get("text", "")
        tables = result.get("tables", []) if isinstance(result, dict) else []

        assert len(text) > 50, "Extraction returned too little text"

        # Check expected terms appear in extracted text
        text_lower = text.lower()
        for term in case["expect_terms"]:
            assert term.lower() in text_lower, \
                f"Expected term '{term}' not found in extracted text"

        # ── Step 2: Chunk the text (Module 1 — SectionChunker) ──
        chunks = pipeline["chunker"].chunk(text)
        assert len(chunks) >= case["min_chunks"], \
            f"Expected ≥{case['min_chunks']} chunks, got {len(chunks)}"

        for section_num in case["expect_sections"]:
            section_nums = [c["section_number"] for c in chunks]
            assert section_num in section_nums, \
                f"Expected section '{section_num}' not found in chunks"

        # ── Step 3: Filter by keywords (Module 1 — KeywordFilter) ──
        filtered = pipeline["kf"].score_chunks(chunks)
        high_chunks = [c for c in filtered if c.get("count_high", 0) > 0]
        assert len(high_chunks) >= 1, "No HIGH confidence chunks found"

        # ── Step 4: Generate rules from filtered text (Module 3) ──
        all_rules = []
        for chunk in high_chunks:
            text_to_process = chunk.get("filtered_text", chunk.get("text", ""))
            rules = pipeline["gen"].generate_rules(text_to_process)
            if rules:
                all_rules.extend(rules)

        # Also process tables if any
        if tables:
            pipeline["builder"].process_all_tables(tables, pipeline["gen"])

        assert len(all_rules) >= case["expect_rules_min"], \
            f"Expected ≥{case['expect_rules_min']} rules, got {len(all_rules)}"

        # ── Step 5: Validate generated rules ──
        for rule in all_rules:
            rule_data = rule if isinstance(rule, dict) else json.loads(rule)
            # Must have required fields
            for field in ["element", "property", "operator", "value"]:
                assert field in rule_data, \
                    f"Rule missing '{field}': {rule_data}"

        # Check that expected elements appear
        all_elements = set()
        for rule in all_rules:
            rd = rule if isinstance(rule, dict) else json.loads(rule)
            all_elements.add(rd.get("element", "").lower())

        for expected_el in case["expect_elements"]:
            matches = [e for e in all_elements if expected_el in e or e in expected_el]
            assert matches, \
                f"Expected element '{expected_el}' not found. Got: {all_elements}"

        # Check that expected numeric values appear
        all_values = set()
        for rule in all_rules:
            rd = rule if isinstance(rule, dict) else json.loads(rule)
            try:
                all_values.add(float(rd.get("value", 0)))
            except (TypeError, ValueError):
                pass

        for expected_val in case.get("expect_values", []):
            close_match = any(abs(v - expected_val) < 1 for v in all_values)
            assert close_match, \
                f"Expected value {expected_val} not found. Got: {all_values}"

        # ── Save results for debugging ──
        self._save_result(case["id"], all_rules)

    def _save_result(self, case_id, rules):
        os.makedirs(RESULTS_DIR, exist_ok=True)
        path = os.path.join(RESULTS_DIR, f"{case_id}_rules.json")
        data = [r if isinstance(r, dict) else json.loads(r) for r in rules]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# Consistency tests — same input, multiple runs
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.llm
class TestPipelineConsistency:

    def test_same_input_similar_output(self, pipeline):
        """
        Running the same text through Module 3 twice should produce
        structurally similar rules (same element, same value).
        LLM output may vary in wording but core data should be stable.
        """
        text = "Every exit stair shall have a clear width of not less than 860 mm."

        rules_1 = pipeline["gen"].generate_rules(text)
        time.sleep(1)  # small delay to avoid rate limiting
        rules_2 = pipeline["gen"].generate_rules(text)

        assert len(rules_1) == len(rules_2), \
            f"Rule count inconsistent: run1={len(rules_1)}, run2={len(rules_2)}"

        r1 = rules_1[0] if isinstance(rules_1[0], dict) else json.loads(rules_1[0])
        r2 = rules_2[0] if isinstance(rules_2[0], dict) else json.loads(rules_2[0])

        assert r1.get("element") == r2.get("element"), \
            f"Element inconsistent: '{r1.get('element')}' vs '{r2.get('element')}'"

        try:
            v1, v2 = float(r1.get("value", 0)), float(r2.get("value", 0))
            assert abs(v1 - v2) < 1, f"Value inconsistent: {v1} vs {v2}"
        except (TypeError, ValueError):
            pass  # non-numeric values — skip comparison


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline without real PDF — uses synthetic text (always runnable)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
@pytest.mark.llm
class TestSyntheticPipeline:
    """
    Integration test that doesn't need a real PDF fixture.
    Uses pre-extracted text to test Module 1 chunking → Module 3 rule gen.
    """

    SYNTHETIC_DOC = """# 4 Stairs
Every exit stair shall have a clear width of not less than 860 mm.
The riser height shall not be more than 200 mm.
The tread run shall not be less than 255 mm.

# 6 Guards and Handrails
Guards shall not be less than 900 mm in height.
Handrails shall be between 865 mm and 965 mm in height.

# 7 Windows and Glazing
Each window providing emergency egress shall have an unobstructed opening
of not less than 0.35 m2 with no dimension less than 380 mm.
"""

    def test_synthetic_full_pipeline(self, pipeline):
        # Chunk
        chunks = pipeline["chunker"].chunk(self.SYNTHETIC_DOC)
        assert len(chunks) >= 3

        # Filter
        filtered    = pipeline["kf"].score_chunks(chunks)
        high_chunks = [c for c in filtered if c.get("count_high", 0) > 0]
        assert len(high_chunks) >= 1

        # Generate rules
        all_rules = []
        for chunk in high_chunks:
            text  = chunk.get("filtered_text", chunk.get("text", ""))
            rules = pipeline["gen"].generate_rules(text)
            if rules:
                all_rules.extend(rules)

        # Should produce rules for stairs, guards, and windows
        assert len(all_rules) >= 3, f"Expected ≥3 rules, got {len(all_rules)}"

        elements = set()
        for r in all_rules:
            rd = r if isinstance(r, dict) else json.loads(r)
            elements.add(rd.get("element", "").lower())

        # At minimum, stairs and guards should appear
        assert any("stair" in e for e in elements), f"No stair rules. Got: {elements}"
        assert any("guard" in e for e in elements), f"No guard rules. Got: {elements}"
