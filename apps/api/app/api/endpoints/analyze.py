from fastapi import APIRouter, UploadFile, File, HTTPException
from ...services import ifc_parser
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def analyze_ifc(file: UploadFile = File(...)):
    if not file.filename.endswith('.ifc'):
        raise HTTPException(status_code=400, detail="Only .ifc files are supported")
        
    try:
        content = await file.read()
        wall_count = ifc_parser.count_walls(content)
        return {
            "filename": file.filename,
            "wall_count": wall_count,
            "message": "Analysis completed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing IFC file: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the file.")
