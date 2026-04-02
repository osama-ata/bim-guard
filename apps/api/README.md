# BIMGuard AI — Module 1 + 3

Automated OBC Part 9 compliance rule extraction pipeline.
Converts Ontario Building Code PDFs into structured rules stored in `rules.db`,
ready for IFC model compliance checking in Module 4.

---

## Pipeline Overview

```
OBC PDF
  └── Module 1: Document Parser
        ├── Step 1 — Docling Extractor     → prose text + table DataFrames
        ├── Step 2 — Table Rule Builder    → tables → rules.db (no LLM/regex)
        ├── Step 3 — Section Chunker       → 13 OBC section chunks
        └── Step 4 — Keyword Filter        → scored + confidence-labelled paragraphs
                          ↓
              Module 1 Improvements (optional)
                ├── TF-IDF Analyzer        → discovers missing keywords
                ├── Dependency Parser      → catches missed obligation sentences
                ├── Confidence Scorer      → SEND/SKIP decision per paragraph
                └── BERT Classifier        → sentence-level rule probability
                          ↓
              Module 3: Rule Builder
                ├── Regex Converter (default) → free, no API key, works offline
                ├── GPT-4o Converter (optional) → more accurate, costs per call
                ├── Rule Generator            → validate + enrich entity types
                └── Rule Store                → save to rules.db
```

---

## Switching Between Regex and GPT-4o 

Open `orchestrator.py` and change one line:

```python
USE_GPT4O = False   # regex — free, no API key, works offline
USE_GPT4O = True    # GPT-4o — more accurate, costs per API call
```

---

## Setup

### 1. Navigate to the API folder
```bash
cd apps/api
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

> **First run:** Docling will download its vision models (~2 min, one-time only).
> Use a GPU runtime for faster processing if available.

### 3. Set your API key (only needed if USE_GPT4O = True)
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-key-here
```

---

## Run the Pipeline

```bash
# Full pipeline — all 13 OBC sections
python orchestrator.py data/input_docs/OBC_Part9.pdf

# Test on one section first (recommended)
python orchestrator.py data/input_docs/OBC_Part9.pdf
```

Or from Python:
```python
from orchestrator import run_pipeline

result = run_pipeline(
    pdf_path      = "data/input_docs/OBC_Part9.pdf",
    run_sections  = ["4"],   # test Section 4 (Stairs) first
    seed_db_first = True,
)
print(result)
```

---

## Seed Pre-built Rules

25 pre-built OBC Part 9 rules are included.
Seed them without uploading a PDF:

```bash
python -m modules.module3_rule_builder.obc_seed_rules
```

---

## Run Tests

```bash
pytest tests/ -v
```

---

## File Structure

```
apps/api/
├── app/
│   ├── config.py                           ← all paths + settings
│   ├── orchestrator.py                     ← single entry point
│   │
│   ├── modules/
│   │   ├── module1_doc_parser/
│   │   │   ├── docling_extractor.py        ← Step 1: PDF → text + tables
│   │   │   ├── table_rule_builder.py       ← Step 2: tables → rules directly
│   │   │   ├── section_chunker.py          ← Step 3: text → 13 sections
│   │   │   ├── keyword_filter.py           ← Step 4: spaCy scoring
│   │   │   ├── tfidf_analyzer.py           ← Improvement 1: keyword discovery
│   │   │   ├── dependency_parser.py        ← Improvement 2: grammar signals
│   │   │   ├── confidence_scorer.py        ← Improvement 3: SEND/SKIP decision
│   │   │   ├── bert_classifier.py          ← Improvement 4: sentence classifier
│   │   │   ├── enhanced_orchestrator.py    ← runs all 4 improvements
│   │   │   └── keywords/
│   │   │       └── keyword_master.py       ← 193 keywords, 12 groups
│   │   │
│   │   └── module3_rule_builder/
│   │       ├── rule_store.py               ← SQLite CRUD
│   │       ├── rule_generator.py           ← validate + save rules
│   │       ├── rule_converter.py           ← GPT-4o + RAG NLP engine
│   │       ├── regex_rule_converter.py     ← regex engine (default)
│   │       └── obc_seed_rules.py           ← 25 pre-built OBC rules
│   │
│   ├── data/
│   │   ├── input_docs/                     ← place OBC PDFs here
│   │   ├── ifc_models/                     ← IFC files for Module 2/4
│   │   ├── reports/                        ← output reports (gitignored)
│   │   └── rules/
│   │       └── rules.db                    ← generated, gitignored
│   │
│   └── tests/
│       ├── test_module1.py
│       └── test_module3.py
│
├── requirements.txt
└── .env.example                            ← copy to .env, add API key
```

---

## rules.db Schema

| Field | Type | Description |
|---|---|---|
| rule_id | TEXT | UUID primary key |
| source_doc | TEXT | OBC_Part9_PDF / OBC_Table_Direct / OBC_Part9_Seed |
| section_ref | TEXT | OBC section e.g. 9.8.2.1.(2) |
| rule_type | TEXT | json_check / range_check / regex / exists_check |
| entity_type | TEXT | IFC class e.g. IfcStairFlight |
| property_name | TEXT | IFC property name |
| operator | TEXT | >= / <= / == / != / between / exists |
| value | TEXT | JSON-encoded number, string, or [min, max] |
| unit | TEXT | mm / m / m2 / deg / ratio |
| priority | INT | 1 = critical, 0 = standard |
| description | TEXT | plain English explanation |

---

## Converter Comparison

| | Regex | GPT-4o |
|---|---|---|
| Cost | Free | Per API call |
| API key needed | No | Yes |
| Works offline | Yes | No |
| Catches all phrasing | No | Yes |
| Hallucinations | Never | Occasionally |
| Speed | Instant | 1–3 sec per chunk |
| Best for | Development / testing | Production accuracy |

---

## Next Steps (Module 2 + 4)

Once rules.db is populated:
- **Module 2** reads IFC files and extracts element properties
- **Module 4** compares IFC properties against rules.db and flags failures
- **Module 5** generates BCF / CSV / PDF compliance reports
