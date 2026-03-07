import ifcopenshell

def count_walls(file_content: bytes) -> int:
    """
    Parses an IFC file from bytes and counts the number of IfcWall entities.
    """
    try:
        # Decode bytes to string, handling common encodings
        try:
            content_str = file_content.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 which is common in older IFC files
            content_str = file_content.decode('latin-1')

        # ⚡ Bolt: Parse IFC directly from string in memory
        # This avoids expensive disk I/O operations (writing and reading temporary files)
        ifc_file = ifcopenshell.file.from_string(content_str)
        walls = ifc_file.by_type("IfcWall")
        return len(walls)
    except Exception as e:
        raise Exception(f"Failed to parse IFC file: {str(e)}")
