from fastapi import APIRouter, UploadFile, File, HTTPException
from ...services import ifc_parser
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def analyze_ifc(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith('.ifc'):
        raise HTTPException(status_code=400, detail="Only .ifc files are supported")
        
    try:
        content = await file.read()
        wall_count = ifc_parser.count_walls(content)
        spatial_tree = ifc_parser.extract_spatial_tree(content)
        return {
            "filename": file.filename,
            "wall_count": wall_count,
            "spatial_tree": spatial_tree,
            "message": "Analysis completed successfully"
        }
    except Exception as e:
        logger.error(f"Error processing IFC file: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the file.")
