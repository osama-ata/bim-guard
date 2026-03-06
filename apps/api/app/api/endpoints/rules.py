import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter()

RULES_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data",
    "rules",
    "obc_part9.json"
)

@router.get("/")
def get_rules():
    """
    Temporary endpoint to serve static compliance rules from obc_part9.json.
    This simulates Module 3 (Rule Extraction and Database).
    """
    if not os.path.exists(RULES_FILE_PATH):
        raise HTTPException(status_code=404, detail="Rules data file not found.")
        
    try:
        with open(RULES_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading rules data: {str(e)}")