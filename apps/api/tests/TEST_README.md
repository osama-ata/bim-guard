# BIMGuard Test Suite — Module 1 & 3

## Quick Start

```bash
# Run fast unit tests only (no LLM, no PDFs)
pytest tests/test_module1.py -v -m "not slow"

# Run Module 3 deterministic tests only
pytest tests/test_module3.py -v -m "not llm"

# Run LLM-dependent tests (Module 3 rule generation)
pytest tests/test_module3.py -v -m llm

# Run integration tests (needs fixtures + LLM)
pytest tests/test_integration.py -v -m integration

# Run everything
pytest tests/ -v

# Run the eval harness (accuracy scoring)
python -m tests.eval_harness
python -m tests.eval_harness --case stair_width
python -m tests.eval_harness --report
```

## File Overview

```
tests/
├── conftest.py              # Shared fixtures, marker registration
├── test_module1.py          # Module 1 unit tests (chunker, filter, tables, PDF parsing)
├── test_module3.py          # Module 3 unit tests (rule generation, schema, LLM path)
├── test_integration.py      # End-to-end pipeline: PDF → rules
├── test_compliance.py       # (your existing file — unchanged)
├── eval_harness.py          # LLM-as-judge accuracy scoring tool
├── fixtures/                # Put your test PDFs here
│   └── sample_obc_stairs.pdf
├── snapshots/               # Auto-generated regression baselines
│   ├── chunker_basic.json
│   └── m3_stair_width.json
├── integration_results/     # Auto-saved pipeline output for debugging
└── eval_results/            # Timestamped accuracy scores
```

## Setup

### 1. Add test PDF fixtures

Place 1-3 real OBC PDF pages in `tests/fixtures/`:

```
tests/fixtures/sample_obc_stairs.pdf    # A page with stair requirements
tests/fixtures/sample_obc_fire.pdf      # (optional) fire safety section
```

Then update `INTEGRATION_CASES` in `test_integration.py` to match your files.

### 2. Set LLM credentials

For the eval harness and LLM-marked tests:

```bash
# If using Anthropic (default)
export ANTHROPIC_API_KEY=sk-ant-...

# If using OpenAI
# Edit eval_harness.py: LLM_PROVIDER = "openai"
export OPENAI_API_KEY=sk-...
```

### 3. Install test dependencies

```bash
pip install pytest pandas anthropic
```

## Test Markers

| Marker        | Meaning                              | Run command              |
|---------------|--------------------------------------|--------------------------|
| (no marker)   | Fast, deterministic, always runnable | `pytest tests/ -m "not slow and not llm"` |
| `@pytest.mark.slow` | Needs real PDF fixtures       | `pytest -m slow`         |
| `@pytest.mark.llm`  | Calls the LLM (slow, costs $) | `pytest -m llm`          |
| `@pytest.mark.integration` | Full pipeline test     | `pytest -m integration`  |

## Snapshots

Snapshots auto-generate on first run. To reset:
```bash
rm tests/snapshots/*.json
pytest tests/ -v  # recreates them
```

## Eval Harness — Tracking Accuracy Over Time

The eval harness scores Module 3 on three dimensions (1-5 each):

- **Correctness** — right element, property, operator, value?
- **Completeness** — all requirements captured?
- **Executability** — can Module 4 use this rule against IFC?

Run it after any prompt change, model swap, or code update:

```bash
python -m tests.eval_harness          # full eval
python -m tests.eval_harness --report # compare historical scores
```

Results are saved with timestamps in `tests/eval_results/` so you can track
whether changes improve or degrade accuracy.
