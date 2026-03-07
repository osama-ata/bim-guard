import json
import os
from functools import lru_cache
from fastapi import APIRouter, HTTPException

router = APIRouter()

RULES_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "rules",
    "obc_part9.json"
)

@lru_cache(maxsize=1)
def get_cached_rules(path: str):
    """
    Reads and parses the JSON rules file, caching the result.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/")
def get_rules():
    """
    Temporary endpoint to serve static compliance rules from obc_part9.json.
    This simulates Module 3 (Rule Extraction and Database).
    """
    if not os.path.exists(RULES_FILE_PATH):
        raise HTTPException(status_code=404, detail="Rules data file not found.")
        
    try:
        return get_cached_rules(RULES_FILE_PATH)
    except Exception as e:
        # Clear cache in case of transient errors
        get_cached_rules.cache_clear()
        raise HTTPException(status_code=500, detail=f"Error reading rules data: {str(e)}")