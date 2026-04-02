"""
tests/test_module1.py
----------------------
Unit tests for Module 1 — SectionChunker, KeywordFilter, TableRuleBuilder,
DoclingExtractor (PDF parsing), and regression snapshots.

Run with: pytest tests/test_module1.py -v

SETUP:
  Place 1-3 real OBC PDF pages in tests/fixtures/
  e.g.  tests/fixtures/sample_obc_stairs.pdf
"""

import os
import json
import pytest
import pandas as pd

from module1_doc_parser.section_chunker    import SectionChunker
from module1_doc_parser.keyword_filter     import KeywordFilter
from module1_doc_parser.table_rule_builder import TableRuleBuilder
from module1_doc_parser.keywords.keyword_master import (
    ALL_KEYWORDS, KEYWORD_WEIGHTS, BIGRAM_PHRASES
)

TEST_DB       = "tests/test_rules_m1.db"
FIXTURES_DIR  = os.path.join(os.path.dirname(__file__), "fixtures")
SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "snapshots")


# ═══════════════════════════════════════════════════════════════════════════════
# Keyword master tests
# ═══════════════════════════════════════════════════════════════════════════════

def test_keyword_total_count():
    assert len(ALL_KEYWORDS) >= 193, "Should have at least 193 keywords"

def test_keyword_weights_assigned():
    for kw in ALL_KEYWORDS:
        assert kw in KEYWORD_WEIGHTS, f"No weight for keyword: '{kw}'"

def test_bigrams_sorted_longest_first():
    for i in range(len(BIGRAM_PHRASES) - 1):
        assert len(BIGRAM_PHRASES[i]) >= len(BIGRAM_PHRASES[i + 1]), \
            "Bigrams must be sorted longest-first for correct matching"

def test_critical_keywords_present():
    flat = [kw.lower() for kw in ALL_KEYWORDS]
    for expected in ["shall", "must", "minimum", "maximum",
                     "need not", "deemed to comply", "prohibited",
                     "fire-resistance rating", "means of egress"]:
        assert expected in flat, f"Critical keyword missing: '{expected}'"

def test_keyword_weights_are_positive_integers():
    """Every weight must be a positive int — catches typos like 0 or -1."""
    for kw, weight in KEYWORD_WEIGHTS.items():
        assert isinstance(weight, int) and weight > 0, \
            f"Invalid weight for '{kw}': {weight}"


# ═══════════════════════════════════════════════════════════════════════════════
# SectionChunker tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def chunker():
    return SectionChunker()

def test_chunker_detects_markdown_headings(chunker):
    text = """# 4 Stairs
Every stair shall have a clear width of not less than 860 mm.

# 6 Guards and Handrails
Guards shall not be less than 900 mm in height.
"""
    chunks = chunker.chunk(text)
    nums   = [c["section_number"] for c in chunks]
    assert "4" in nums
    assert "6" in nums

def test_chunker_detects_plain_headings(chunker):
    text = """4 Stairs
Every stair shall have a clear width of not less than 860 mm.

6 Guards and Handrails
Guards shall not be less than 900 mm in height.
"""
    chunks = chunker.chunk(text)
    nums   = [c["section_number"] for c in chunks]
    assert "4" in nums
    assert "6" in nums

def test_chunker_returns_correct_section_names(chunker):
    text = "# 4 Stairs\nEvery stair shall have a clear width."
    chunks = chunker.chunk(text)
    assert chunks[0]["section_name"] == "Stairs (Detailed - Part 9)"

def test_chunker_empty_text(chunker):
    chunks = chunker.chunk("")
    assert chunks == []

def test_chunker_text_goes_to_right_section(chunker):
    text = """# 4 Stairs
Stair width shall be not less than 860 mm.

# 7 Windows and Glazing
Windows shall provide egress opening area of 0.35 m2.
"""
    chunks = chunker.chunk(text)
    stair_chunk   = next(c for c in chunks if c["section_number"] == "4")
    window_chunk  = next(c for c in chunks if c["section_number"] == "7")
    assert "860" in stair_chunk["text"]
    assert "0.35" in window_chunk["text"]

def test_chunker_preserves_all_content(chunker):
    """No text should be silently dropped between sections."""
    text = """# 4 Stairs
Line A about stairs.
Line B about stairs.

# 6 Guards and Handrails
Line C about guards.
"""
    chunks    = chunker.chunk(text)
    all_text  = " ".join(c["text"] for c in chunks)
    for phrase in ["Line A", "Line B", "Line C"]:
        assert phrase in all_text, f"Content silently dropped: '{phrase}'"

def test_chunker_char_count_field(chunker):
    """Each chunk should have a char_count that matches the actual text length."""
    text = "# 4 Stairs\nEvery stair shall have a clear width of 860 mm."
    chunks = chunker.chunk(text)
    for c in chunks:
        if "char_count" in c:
            assert c["char_count"] == len(c["text"]), \
                "char_count doesn't match actual text length"


# ═══════════════════════════════════════════════════════════════════════════════
# KeywordFilter tests
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def kf():
    return KeywordFilter()

def test_keyword_filter_high_confidence(kf):
    chunk = {
        "section_number": "4",
        "section_name":   "Stairs",
        "text":           (
            "Every exit stair shall not be less than 860 mm in clear width.\n\n"
            "The riser height shall be between 125 mm and 200 mm minimum maximum.\n\n"
            "Guards shall be required at all landings with a height of not less than 900 mm."
        ),
        "char_count": 200,
    }
    filtered   = kf.score_chunks([chunk])
    high_count = filtered[0]["count_high"]
    assert high_count >= 1, "Expected at least 1 HIGH confidence paragraph"

def test_keyword_filter_low_confidence_flagged(kf):
    chunk = {
        "section_number": "4",
        "section_name":   "Stairs",
        "text":           "See the appendix for further reference details only.",
        "char_count":     55,
    }
    filtered     = kf.score_chunks([chunk])
    filtered_txt = filtered[0]["filtered_text"]
    assert "[LOW_CONFIDENCE]" in filtered_txt

def test_keyword_filter_bigram_scored_highest(kf):
    chunk = {
        "section_number": "4", "section_name": "Stairs",
        "text": "The rise shall not exceed 200 mm.",
        "char_count": 35,
    }
    filtered = kf.score_chunks([chunk])
    paras    = filtered[0]["scored_paragraphs"]
    assert paras[0]["score"] >= 6

def test_keyword_filter_new_group10_permissive(kf):
    chunk = {
        "section_number": "4", "section_name": "Stairs",
        "text": "The handrail need not be continuous if an opening is provided.",
        "char_count": 65,
    }
    filtered = kf.score_chunks([chunk])
    matched  = filtered[0]["scored_paragraphs"][0]["matched"]
    assert "need not" in matched

def test_keyword_filter_new_group11_deemed(kf):
    chunk = {
        "section_number": "4", "section_name": "Stairs",
        "text": "This design is deemed to comply with the structural requirements.",
        "char_count": 65,
    }
    filtered = kf.score_chunks([chunk])
    matched  = filtered[0]["scored_paragraphs"][0]["matched"]
    assert "deemed to comply" in matched

def test_keyword_filter_multiple_chunks(kf):
    """Filter should handle a batch of chunks without mixing results."""
    chunks = [
        {
            "section_number": "4", "section_name": "Stairs",
            "text": "Every stair shall have a clear width of 860 mm.",
            "char_count": 50,
        },
        {
            "section_number": "6", "section_name": "Guards",
            "text": "Guards shall not be less than 900 mm in height.",
            "char_count": 50,
        },
    ]
    filtered = kf.score_chunks(chunks)
    assert len(filtered) == 2
    assert filtered[0]["section_number"] == "4"
    assert filtered[1]["section_number"] == "6"

def test_keyword_filter_no_keywords(kf):
    """Text with zero compliance keywords should get low/zero score."""
    chunk = {
        "section_number": "1", "section_name": "Intro",
        "text": "This is a general introduction to the document.",
        "char_count": 50,
    }
    filtered = kf.score_chunks([chunk])
    paras    = filtered[0]["scored_paragraphs"]
    if paras:
        assert paras[0]["score"] <= 2, "Non-compliance text should score low"


# ═══════════════════════════════════════════════════════════════════════════════
# TableRuleBuilder tests
# ═══════════════════════════════════════════════════════════════════════════════

import os
from module3_rule_builder.rule_store     import RuleStore
from module3_rule_builder.rule_generator import RuleGenerator

@pytest.fixture
def store_and_gen():
    store = RuleStore(TEST_DB)
    store.clear_all_rules()
    gen   = RuleGenerator(store)
    yield store, gen
    store.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_table_builder_extracts_range_rules(store_and_gen):
    store, gen = store_and_gen
    builder    = TableRuleBuilder(store)

    df = pd.DataFrame({
        "Measurement": ["Rise", "Run"],
        "Min":         [125,   255],
        "Max":         [200,   355],
    })
    tables = [{"table_index": 0, "dataframe": df, "row_count": 2, "col_count": 3}]
    saved  = builder.process_all_tables(tables, gen)
    assert saved == 2
    assert store.count() == 2

def test_table_builder_skips_non_minmax_table(store_and_gen):
    store, gen = store_and_gen
    builder    = TableRuleBuilder(store)

    df = pd.DataFrame({
        "Element": ["Stair", "Door"],
        "Notes":   ["See 9.8", "See 9.6"],
    })
    tables = [{"table_index": 0, "dataframe": df, "row_count": 2, "col_count": 2}]
    saved  = builder.process_all_tables(tables, gen)
    assert saved == 0
    assert store.count() == 0

def test_table_builder_rule_schema(store_and_gen):
    """Every saved rule must have the required fields for Module 4 to consume."""
    store, gen = store_and_gen
    builder    = TableRuleBuilder(store)

    df = pd.DataFrame({
        "Measurement": ["Rise"],
        "Min":         [125],
        "Max":         [200],
    })
    tables = [{"table_index": 0, "dataframe": df, "row_count": 1, "col_count": 3}]
    builder.process_all_tables(tables, gen)

    rules = store.get_all_rules()
    required_fields = {"element", "property", "operator", "value"}
    for rule in rules:
        rule_data = rule if isinstance(rule, dict) else json.loads(rule)
        missing   = required_fields - set(rule_data.keys())
        assert not missing, f"Rule missing fields: {missing} — rule: {rule_data}"

def test_table_builder_multiple_tables(store_and_gen):
    """Should process multiple tables in one call."""
    store, gen = store_and_gen
    builder    = TableRuleBuilder(store)

    df1 = pd.DataFrame({"Measurement": ["Rise"], "Min": [125], "Max": [200]})
    df2 = pd.DataFrame({"Measurement": ["Width"], "Min": [860], "Max": [1200]})
    tables = [
        {"table_index": 0, "dataframe": df1, "row_count": 1, "col_count": 3},
        {"table_index": 1, "dataframe": df2, "row_count": 1, "col_count": 3},
    ]
    saved = builder.process_all_tables(tables, gen)
    assert saved == 2
    assert store.count() == 2


# ═══════════════════════════════════════════════════════════════════════════════
# DoclingExtractor tests (PDF parsing — the critical gap)
# ═══════════════════════════════════════════════════════════════════════════════
#
# These require real PDFs in tests/fixtures/.  Mark them so they only run
# when fixtures are present (won't break CI if PDFs aren't committed).

def _fixture_pdf(name):
    path = os.path.join(FIXTURES_DIR, name)
    return pytest.param(path, marks=pytest.mark.skipif(
        not os.path.exists(path), reason=f"Fixture not found: {name}"
    ))

# ── Adjust the PDF name below to match your actual fixture file ──
SAMPLE_PDF = "sample_obc_stairs.pdf"

@pytest.fixture
def docling_extractor():
    """Import lazily — Docling may not be installed in all environments."""
    try:
        from module1_doc_parser.docling_extractor import DoclingExtractor
        return DoclingExtractor()
    except ImportError:
        pytest.skip("DoclingExtractor not available (Docling not installed)")

@pytest.mark.slow
class TestDoclingExtractor:
    """
    Tests that run against real PDFs.
    Run with:  pytest tests/test_module1.py -m slow -v
    Skip with: pytest tests/test_module1.py -m "not slow"
    """

    @_fixture_pdf(SAMPLE_PDF)
    def test_extraction_returns_text(self, pdf_path, docling_extractor):
        """PDF extraction must return non-empty text."""
        result = docling_extractor.extract(pdf_path)
        text   = result if isinstance(result, str) else result.get("text", "")
        assert len(text) > 100, "Extracted text is suspiciously short"

    @_fixture_pdf(SAMPLE_PDF)
    def test_extraction_contains_expected_terms(self, pdf_path, docling_extractor):
        """
        Extracted text should contain known terms from the fixture PDF.
        ── CUSTOMIZE these expected terms for your actual fixture PDF ──
        """
        result = docling_extractor.extract(pdf_path)
        text   = result if isinstance(result, str) else result.get("text", "")
        text_lower = text.lower()

        expected_terms = ["stair", "shall", "mm"]  # adjust to your PDF
        for term in expected_terms:
            assert term in text_lower, \
                f"Expected term '{term}' not found in extracted text"

    @_fixture_pdf(SAMPLE_PDF)
    def test_extraction_finds_tables(self, pdf_path, docling_extractor):
        """If the PDF has tables, extraction should return table data."""
        result = docling_extractor.extract(pdf_path)
        tables = result.get("tables", []) if isinstance(result, dict) else []
        # This is a soft check — skip if your fixture has no tables
        if tables:
            assert len(tables) >= 1
            assert tables[0].get("row_count", 0) > 0

    @_fixture_pdf(SAMPLE_PDF)
    def test_extraction_handles_corrupt_pdf(self, docling_extractor):
        """Corrupt or missing files should raise cleanly, not crash."""
        with pytest.raises(Exception):
            docling_extractor.extract("/tmp/does_not_exist.pdf")


# ═══════════════════════════════════════════════════════════════════════════════
# Regression snapshot tests
# ═══════════════════════════════════════════════════════════════════════════════
#
# First run: saves output as snapshot.  Subsequent runs: compares against it.
# To update snapshots: delete the file in tests/snapshots/ and re-run.

class TestSnapshots:

    def _snapshot_path(self, name):
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
        return os.path.join(SNAPSHOTS_DIR, f"{name}.json")

    def test_chunker_snapshot(self, chunker):
        text = """# 4 Stairs
Every stair shall have a clear width of not less than 860 mm.

# 6 Guards and Handrails
Guards shall not be less than 900 mm in height.
"""
        chunks   = chunker.chunk(text)
        snap_file = self._snapshot_path("chunker_basic")

        if not os.path.exists(snap_file):
            with open(snap_file, "w") as f:
                json.dump(chunks, f, indent=2)
            pytest.skip("Snapshot created — re-run to verify")

        with open(snap_file) as f:
            expected = json.load(f)

        assert len(chunks) == len(expected), \
            f"Chunk count changed: {len(expected)} → {len(chunks)}"
        for got, exp in zip(chunks, expected):
            assert got["section_number"] == exp["section_number"]
            assert got["section_name"]   == exp["section_name"]

    def test_keyword_filter_snapshot(self, kf):
        chunk = {
            "section_number": "4", "section_name": "Stairs",
            "text": (
                "Every exit stair shall not be less than 860 mm in clear width.\n\n"
                "The riser height shall be between 125 mm and 200 mm."
            ),
            "char_count": 120,
        }
        filtered  = kf.score_chunks([chunk])
        snap_file = self._snapshot_path("keyword_filter_basic")

        if not os.path.exists(snap_file):
            with open(snap_file, "w") as f:
                json.dump(filtered, f, indent=2)
            pytest.skip("Snapshot created — re-run to verify")

        with open(snap_file) as f:
            expected = json.load(f)

        assert filtered[0]["count_high"] == expected[0]["count_high"], \
            "HIGH confidence count changed — check keyword scoring"
