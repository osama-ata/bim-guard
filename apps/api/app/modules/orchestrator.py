"""
orchestrator.py
----------------
Runs the full BIMGuard Module 1 + Module 3 pipeline end to end.
This is the single entry point — call run_pipeline() with a PDF path.

Pipeline flow:
    PDF file
        ↓  Module 1 — Step 1
    DoclingExtractor          → prose text + table DataFrames
        ↓  Module 1 — Step 2
    TableRuleBuilder          → tables → rules.db directly (no LLM)
        ↓  Module 1 — Step 3
    SectionChunker            → 13 OBC section chunks
        ↓  Module 1 — Step 4
    KeywordFilter             → scored + confidence-labelled paragraphs
        ↓  Handoff M1 → M3
    RuleConverter             → Regex (default) or GPT-4o → structured rule dicts
        ↓  Module 3
    RuleGenerator             → validate + enrich entity types
        ↓
    RuleStore                 → save to rules.db
        ↓
    Return summary dict       → back to caller (CLI or future API)

SWITCHING BETWEEN REGEX AND GPT-4o:
    Set USE_GPT4O = False  → uses regex (free, no API key needed)
    Set USE_GPT4O = True   → uses GPT-4o (accurate, costs per call)

Usage:
    # Run from project root
    python orchestrator.py data/input_docs/OBC_Part9.pdf

    # Or import and call:
    from orchestrator import run_pipeline
    result = run_pipeline("data/input_docs/OBC_Part9.pdf")
"""

import sys
from pathlib import Path

from config import DB_PATH, OPENAI_API_KEY

from modules.module1_doc_parser.docling_extractor  import DoclingExtractor
from modules.module1_doc_parser.table_rule_builder import TableRuleBuilder
from modules.module1_doc_parser.section_chunker    import SectionChunker
from modules.module1_doc_parser.keyword_filter     import KeywordFilter

from modules.module3_rule_builder.rule_store       import RuleStore
from modules.module3_rule_builder.rule_generator   import RuleGenerator
from modules.module3_rule_builder.obc_seed_rules   import seed_rules

# ── SWITCH HERE ───────────────────────────────────────────────────────────────
# False = regex (free, no API key, works offline)
# True  = GPT-4o (more accurate, costs per API call)
USE_GPT4O = False
# ─────────────────────────────────────────────────────────────────────────────

if USE_GPT4O:
    from modules.module3_rule_builder.rule_converter import RuleConverter
else:
    from modules.module3_rule_builder.regex_rule_converter import RegexRuleConverter as RuleConverter


def run_pipeline(
    pdf_path:      str | Path,
    run_sections:  str | list = "all",
    seed_db_first: bool       = True,
) -> dict:
    """
    Run the full Module 1 → Module 3 pipeline on an OBC PDF.

    Args:
        pdf_path      (str | Path): path to the OBC PDF file
        run_sections  (str | list): "all" or list e.g. ["4", "6"]
                                    Use a single section to test first.
        seed_db_first (bool):       seed 25 pre-built OBC rules before processing

    Returns:
        dict: {
            pdf_file        (str),
            converter_used  (str),   "regex" or "gpt-4o"
            table_rules     (int),   rules from tables (no LLM/regex)
            prose_rules     (int),   rules from converter
            total_rules     (int),   total in DB after run
            sections_run    (int),
            db_summary      (dict),
        }
    """
    pdf_path       = Path(pdf_path)
    converter_name = "gpt-4o" if USE_GPT4O else "regex"

    print(f"\n{'='*60}")
    print(f"  BIMGuard AI — Module 1 + 3 Pipeline")
    print(f"  PDF       : {pdf_path.name}")
    print(f"  Converter : {converter_name.upper()}")
    print(f"  Sections  : {run_sections}")
    print(f"  DB        : {DB_PATH}")
    print(f"{'='*60}\n")

    # ── Initialise ────────────────────────────────────────────────────────────
    store     = RuleStore(DB_PATH)
    generator = RuleGenerator(store)

    if USE_GPT4O:
        converter = RuleConverter(api_key=OPENAI_API_KEY, rule_store=store)
    else:
        converter = RuleConverter()   # regex needs no arguments

    # ── Seed pre-built rules ──────────────────────────────────────────────────
    if seed_db_first:
        print("── SEEDING DB WITH PRE-BUILT OBC RULES ──")
        seed_rules(store, generator)

    rules_before = store.count()

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 1 — STEP 1: Docling extraction
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── MODULE 1 / STEP 1: DOCLING EXTRACTION ──")
    extractor    = DoclingExtractor()
    text, tables = extractor.extract(pdf_path)

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 1 — STEP 2: Table → Direct Rules (no converter needed)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── MODULE 1 / STEP 2: TABLE RULE BUILDER ──")
    table_builder = TableRuleBuilder(store)
    table_rules   = table_builder.process_all_tables(tables, generator)

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 1 — STEP 3: Section Chunker
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── MODULE 1 / STEP 3: SECTION CHUNKER ──")
    chunks = SectionChunker().chunk(text)

    # Filter to requested sections only
    if run_sections != "all":
        chunks = [c for c in chunks if c["section_number"] in run_sections]
        print(f"  Running sections: {run_sections}")

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 1 — STEP 4: Keyword Filter
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── MODULE 1 / STEP 4: KEYWORD FILTER ──")
    filtered_chunks = KeywordFilter().score_chunks(chunks)

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 3: Converter → RuleGenerator → RuleStore
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n── MODULE 3: {converter_name.upper()} CONVERTER ──")
    prose_rules = 0

    for chunk in filtered_chunks:
        section = chunk["section_number"]
        name    = chunk["section_name"]
        print(f"\n  Section {section}: {name}")

        raw_rules = converter.extract_rules(chunk)
        print(f"    Extracted : {len(raw_rules)} rules")

        if raw_rules:
            saved_ids   = generator.save_batch(raw_rules)
            prose_rules += len(saved_ids)
            print(f"    Saved     : {len(saved_ids)} rules")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_rules = store.count()
    db_summary  = store.summary()

    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Converter used               : {converter_name}")
    print(f"  Table rules (no converter)   : {table_rules}")
    print(f"  Prose rules ({converter_name})  : {prose_rules}")
    print(f"  Total rules in DB            : {total_rules}")
    print(f"{'='*60}\n")

    return {
        "pdf_file":       str(pdf_path),
        "converter_used": converter_name,
        "table_rules":    table_rules,
        "prose_rules":    prose_rules,
        "total_rules":    total_rules,
        "sections_run":   len(filtered_chunks),
        "db_summary":     db_summary,
    }


# ── CLI entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <path_to_obc_pdf>")
        print("Example: python orchestrator.py data/input_docs/OBC_Part9.pdf")
        print(f"\nCurrent converter: {'GPT-4o' if USE_GPT4O else 'Regex'}")
        print("To switch: change USE_GPT4O = True/False at top of file")
        sys.exit(1)

    run_pipeline(
        pdf_path      = sys.argv[1],
        run_sections  = "all",
        seed_db_first = True,
    )
