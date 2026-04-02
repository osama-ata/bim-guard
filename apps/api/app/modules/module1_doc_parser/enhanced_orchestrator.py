"""
enhanced_orchestrator.py
--------------------------
Module 1 pipeline with all 4 improvements active.

Pipeline flow:
    PDF
      ↓ Docling Extractor         → prose text + table DataFrames
      ↓ Table Rule Builder        → tables → rules.db (no LLM)
      ↓ Section Chunker           → 13 OBC section chunks
      ↓ Keyword Filter            → scored paragraphs (existing)
      ↓ TF-IDF Analyzer           → IMPROVEMENT 1: discovers missing keywords
      ↓ Dependency Parser         → IMPROVEMENT 2: upgrades missed obligations
      ↓ BERT Classifier           → IMPROVEMENT 3: sentence-level rule probability
      ↓ Confidence Scorer         → IMPROVEMENT 4: combines all signals → SEND/SKIP
      ↓ RuleConverter (GPT-4o)    → only SEND paragraphs → structured rules
      ↓ RuleGenerator             → validate + enrich
      ↓ RuleStore                 → rules.db

USAGE:

    # Full enhanced pipeline
    python enhanced_orchestrator.py data/input_docs/OBC_Part9.pdf

    # Or import:
    from enhanced_orchestrator import run_enhanced_pipeline
    result = run_enhanced_pipeline(
        pdf_path       = "data/input_docs/OBC_Part9.pdf",
        run_sections   = ["4"],           # test one section first
        use_bert       = False,           # set True after training
        discover_keywords = True,         # run TF-IDF keyword discovery
    )
"""

import sys
from pathlib import Path

from config import DB_PATH, OPENAI_API_KEY

# Module 1
from module1_doc_parser.docling_extractor  import DoclingExtractor
from module1_doc_parser.table_rule_builder import TableRuleBuilder
from module1_doc_parser.section_chunker    import SectionChunker
from module1_doc_parser.keyword_filter     import KeywordFilter
from module1_doc_parser.tfidf_analyzer     import TFIDFAnalyzer
from module1_doc_parser.dependency_parser  import DependencyParser
from module1_doc_parser.confidence_scorer  import ConfidenceScorer

# Module 3
from module3_rule_builder.rule_store      import RuleStore
from module3_rule_builder.rule_generator  import RuleGenerator
from module3_rule_builder.rule_converter  import RuleConverter
from module3_rule_builder.obc_seed_rules  import seed_rules


def run_enhanced_pipeline(
    pdf_path:          str,
    run_sections:      str | list = "all",
    seed_db_first:     bool       = True,
    use_bert:          bool       = False,
    bert_mode:         str        = "zero_shot",
    bert_model_path:   str        = None,
    discover_keywords: bool       = True,
) -> dict:
    """
    Run the full enhanced Module 1 + 3 pipeline.

    Args:
        pdf_path          (str):        path to OBC PDF
        run_sections      (str|list):   "all" or ["4","6"]
        seed_db_first     (bool):       seed 25 pre-built rules first
        use_bert          (bool):       enable BERT classifier (requires install)
        bert_mode         (str):        "zero_shot" or "fine_tuned"
        bert_model_path   (str):        path to fine-tuned model if mode=fine_tuned
        discover_keywords (bool):       run TF-IDF keyword discovery report

    Returns:
        dict: pipeline summary
    """
    pdf_path = Path(pdf_path)
    print(f"\n{'='*65}")
    print(f"  BIMGuard AI — Enhanced Module 1 + 3 Pipeline")
    print(f"  PDF         : {pdf_path.name}")
    print(f"  BERT        : {'ON (' + bert_mode + ')' if use_bert else 'OFF'}")
    print(f"  Discovery   : {'ON' if discover_keywords else 'OFF'}")
    print(f"{'='*65}\n")

    # ── Initialise stores ─────────────────────────────────────────────────────
    store     = RuleStore(DB_PATH)
    generator = RuleGenerator(store)
    converter = RuleConverter(api_key=OPENAI_API_KEY, rule_store=store)

    if seed_db_first:
        seed_rules(store, generator)

    rules_before = store.count()

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 1 — Docling extraction
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── STEP 1: DOCLING EXTRACTION ──")
    extractor    = DoclingExtractor()
    text, tables = extractor.extract(pdf_path)

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 2 — Tables → direct rules
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── STEP 2: TABLE RULE BUILDER ──")
    table_builder = TableRuleBuilder(store)
    table_rules   = table_builder.process_all_tables(tables, generator)

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 3 — Section chunker
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── STEP 3: SECTION CHUNKER ──")
    chunks = SectionChunker().chunk(text)

    # Filter to requested sections
    if run_sections != "all":
        chunks = [c for c in chunks if c["section_number"] in run_sections]

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 4 — Keyword filter (existing)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── STEP 4: KEYWORD FILTER ──")
    filtered_chunks = KeywordFilter().score_chunks(chunks)

    # ─────────────────────────────────────────────────────────────────────────
    # IMPROVEMENT 1 — TF-IDF keyword discovery
    # ─────────────────────────────────────────────────────────────────────────
    if discover_keywords:
        print("\n── IMPROVEMENT 1: TF-IDF KEYWORD DISCOVERY ──")
        analyzer   = TFIDFAnalyzer(top_n=30)
        new_kws    = analyzer.discover(filtered_chunks)
        analyzer.print_report(new_kws)

    # ─────────────────────────────────────────────────────────────────────────
    # IMPROVEMENT 2 — Dependency parsing
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── IMPROVEMENT 2: DEPENDENCY PARSER ──")
    dep_parser  = DependencyParser()
    dep_chunks  = dep_parser.analyse_chunks(filtered_chunks)

    # ─────────────────────────────────────────────────────────────────────────
    # IMPROVEMENT 3 — BERT classifier (optional)
    # ─────────────────────────────────────────────────────────────────────────
    bert_chunks = None
    if use_bert:
        print("\n── IMPROVEMENT 3: BERT CLASSIFIER ──")
        from module1_doc_parser.bert_classifier import BERTClassifier
        bert = BERTClassifier(mode=bert_mode, model_path=bert_model_path)
        bert_chunks = bert.classify_chunks(filtered_chunks)
    else:
        print("\n── IMPROVEMENT 3: BERT CLASSIFIER — SKIPPED (use_bert=False) ──")
        print("  To enable: set use_bert=True")
        print("  To train:  clf = BERTClassifier(); clf.train()")

    # ─────────────────────────────────────────────────────────────────────────
    # IMPROVEMENT 4 — Combined confidence scoring
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── IMPROVEMENT 4: CONFIDENCE SCORER ──")
    scorer         = ConfidenceScorer()
    final_chunks   = scorer.combine(
        filtered_chunks = filtered_chunks,
        dep_chunks      = dep_chunks,
        bert_chunks     = bert_chunks,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # MODULE 3 — NLP Engine → RuleGenerator → RuleStore
    # Only sends SEND_HIGH / SEND_MEDIUM / SEND_LOW paragraphs to LLM
    # SKIP paragraphs are excluded — saves API cost
    # ─────────────────────────────────────────────────────────────────────────
    print("\n── MODULE 3: NLP ENGINE (GPT-4o + RAG) ──")
    prose_rules = 0

    for chunk in final_chunks:
        section = chunk["section_number"]
        name    = chunk["section_name"]
        skipped = chunk.get("count_skip", 0)
        sent    = chunk.get("count_send", chunk.get("total_paragraphs", 0))

        print(f"\n  Section {section}: {name}")
        print(f"    Sending: {sent} paragraphs | Skipping: {skipped}")

        raw_rules = converter.extract_rules(chunk)
        print(f"    LLM returned: {len(raw_rules)} rules")

        if raw_rules:
            saved_ids = generator.save_batch(raw_rules)
            prose_rules += len(saved_ids)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_rules = store.count()
    db_summary  = store.summary()
    skipped_total = sum(c.get("count_skip", 0) for c in final_chunks)

    print(f"\n{'='*65}")
    print(f"  ENHANCED PIPELINE COMPLETE")
    print(f"  Table rules (no LLM)         : {table_rules}")
    print(f"  Prose rules (LLM)            : {prose_rules}")
    print(f"  Paragraphs SKIPPED (no cost) : {skipped_total}")
    print(f"  Total rules in DB            : {total_rules}")
    print(f"{'='*65}\n")

    return {
        "pdf_file":       str(pdf_path),
        "table_rules":    table_rules,
        "prose_rules":    prose_rules,
        "total_rules":    total_rules,
        "skipped_paras":  skipped_total,
        "sections_run":   len(final_chunks),
        "db_summary":     db_summary,
    }


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced_orchestrator.py <pdf_path>")
        print("Example: python enhanced_orchestrator.py data/input_docs/OBC_Part9.pdf")
        sys.exit(1)

    run_enhanced_pipeline(
        pdf_path          = sys.argv[1],
        run_sections      = "all",
        seed_db_first     = True,
        use_bert          = False,    # set True after: pip install transformers torch
        discover_keywords = True,
    )
