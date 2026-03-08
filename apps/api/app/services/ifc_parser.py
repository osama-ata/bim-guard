import ifcopenshell

def count_walls(file_content: bytes) -> int:
    """
    Parses an IFC file from bytes and counts the number of IfcWall entities.
    """
    try:
        # ⚡ Bolt Optimization: Parse IFC directly from memory string instead of disk I/O
        # Using tempfile introduces unnecessary disk write/read operations which
        # bottlenecks the API under load. ifcopenshell.file.from_string is more efficient.
        ifc_string = file_content.decode('utf-8')
        ifc_file = ifcopenshell.file.from_string(ifc_string)

        walls = ifc_file.by_type("IfcWall")
        return len(walls)
    except Exception as e:
        # Avoid leaking internal error details per security directive
        raise Exception("Failed to parse IFC file")
