import ifcopenshell
from typing import Any


def parse_ifc(file_content: bytes) -> ifcopenshell.file:
    """Parse IFC bytes into an ifcopenshell file object."""
    ifc_string = file_content.decode("utf-8")
    return ifcopenshell.file.from_string(ifc_string)


def count_walls(file_content: bytes) -> int:
    """
    Parses an IFC file from bytes and counts the number of IfcWall entities.
    """
    try:
        ifc_file = parse_ifc(file_content)
        walls = ifc_file.by_type("IfcWall")
        return len(walls)
    except Exception as e:
        raise Exception(f"Failed to parse IFC file: {str(e)}")


def _get_element_type_name(element: ifcopenshell.entity_instance) -> str:
    """Get a human-friendly type name for an IFC element."""
    return element.is_a()


def _build_node(element: ifcopenshell.entity_instance) -> dict[str, Any]:
    """Build a single tree node dict from an IFC element."""
    return {
        "globalId": element.GlobalId,
        "name": getattr(element, "Name", None) or element.is_a(),
        "type": _get_element_type_name(element),
        "children": [],
    }


def extract_spatial_tree(file_content: bytes) -> dict[str, Any]:
    """
    Extract the BIM Spatial Hierarchy from an IFC file.

    Traverses the decomposition relationships (IfcRelAggregates) and
    containment relationships (IfcRelContainedInSpatialStructure) to
    build a nested tree:

        IfcProject -> IfcSite -> IfcBuilding -> IfcBuildingStorey -> Elements

    Returns a nested dict representing the full spatial tree.
    """
    try:
        ifc_file = parse_ifc(file_content)
    except Exception as e:
        raise Exception(f"Failed to parse IFC file for spatial tree: {str(e)}")

    project = ifc_file.by_type("IfcProject")
    if not project:
        return {"globalId": None, "name": "Empty Model", "type": "Unknown", "children": []}

    root = project[0]
    return _traverse(root)


def _traverse(element: ifcopenshell.entity_instance) -> dict[str, Any]:
    """
    Recursively traverse the IFC spatial hierarchy.

    1. Follow IfcRelAggregates (IsDecomposedBy) to get spatial children
       (Site, Building, Storey).
    2. Follow IfcRelContainedInSpatialStructure (ContainsElements)
       to get the individual building elements at each storey/space.
    """
    node = _build_node(element)

    # 1. Spatial decomposition children  (Project->Site->Building->Storey)
    if hasattr(element, "IsDecomposedBy"):
        for rel in element.IsDecomposedBy:
            for child in rel.RelatedObjects:
                node["children"].append(_traverse(child))

    # 2. Contained elements  (Storey->Walls, Doors, Windows, etc.)
    if hasattr(element, "ContainsElements"):
        for rel in element.ContainsElements:
            for child in rel.RelatedElements:
                node["children"].append(_build_node(child))

    return node
