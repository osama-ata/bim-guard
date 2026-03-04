import ifcopenshell
import tempfile
import os

def count_walls(file_content: bytes) -> int:
    """
    Parses an IFC file from bytes and counts the number of IfcWall entities.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
        
    try:
        ifc_file = ifcopenshell.open(tmp_path)
        walls = ifc_file.by_type("IfcWall")
        return len(walls)
    except Exception as e:
        raise Exception(f"Failed to parse IFC file: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
