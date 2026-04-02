"""
tests/conftest.py
------------------
Shared fixtures and pytest configuration for all BIMGuard tests.
"""

import os
import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# Register custom markers so pytest doesn't warn about them
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests that need real PDFs and are slow")
    config.addinivalue_line("markers", "llm: marks tests that call the LLM (slow, costs tokens)")
    config.addinivalue_line("markers", "integration: marks end-to-end pipeline tests")


# ═══════════════════════════════════════════════════════════════════════════════
# Shared paths
# ═══════════════════════════════════════════════════════════════════════════════

FIXTURES_DIR  = os.path.join(os.path.dirname(__file__), "fixtures")
SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "snapshots")


@pytest.fixture(scope="session", autouse=True)
def ensure_directories():
    """Create test output directories if they don't exist."""
    for d in [FIXTURES_DIR, SNAPSHOTS_DIR]:
        os.makedirs(d, exist_ok=True)
