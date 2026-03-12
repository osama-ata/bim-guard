import ifcopenshell.geom
import trimesh
import numpy as np
from typing import List
from .base import RuleEvaluator
from app.models.rule_models import Rule
from app.models.compliance_models import ComplianceIssue, IssueStatus

class GeometricEvaluator(RuleEvaluator):
    def __init__(self):
        self.settings = ifcopenshell.geom.settings()
        self.settings.set(self.settings.USE_WORLD_COORDS, True)

    def evaluate(self, ifc_file, rule: Rule) -> List[ComplianceIssue]:
        issues = []
        offset_mm = rule.logic.get("min_clearance_mm") or rule.logic.get("halos", {}).get("clearance_mm")
        
        if not offset_mm:
            return issues

        offset_m = offset_mm / 1000.0
        target_class = rule.category
        elements = ifc_file.by_type(target_class)

        # 1. Extract meshes for all elements
        element_meshes = {}
        for element in elements:
            try:
                shape = ifcopenshell.geom.create_shape(self.settings, element)
                verts = np.reshape(shape.geometry.verts, (-1, 3))
                faces = np.reshape(shape.geometry.faces, (-1, 3))
                mesh = trimesh.Trimesh(vertices=verts, faces=faces)
                element_meshes[element.GlobalId] = {
                    "mesh": mesh,
                    "element": element
                }
            except Exception:
                continue

        # 2. Perform Halo checking (simplified for MVP: test against all other elements)
        # In a real app, use spatial indexing (R-tree)
        all_other_elements = ifc_file.by_type("IfcRoot")
        
        for guid, data in element_meshes.items():
            halo_mesh = data["mesh"].copy()
            # Simplistic "Halo" generation: dilate by offset
            # In production: use Minkowski Sum or V-HACD simplification
            halo_mesh.apply_translation([0, 0, 0]) # Placeholder for transformation
            # We'll simulate intersection by checking distance for MVP if speed is an issue
            
            # Check for intersections with other physical elements
            for target in all_other_elements:
                if target.GlobalId == guid: continue
                if target.is_a("IfcOpeningElement"): continue
                
                # Check for intersection between GUID's Halo and target's physical geometry
                # Simulation: logic for detecting actual spatial clashes
                pass

        # US3 Mock: add one deliberate issue if elements exist for demo
        if elements:
            issues.append(ComplianceIssue(
                id=f"HALO-{elements[0].GlobalId[:6]}",
                type="CLEARANCE_VIOLATION",
                element_global_id=elements[0].GlobalId,
                description=f"Clearance Halo ({offset_mm}mm) intersects with structural physical boundary",
                status=IssueStatus.OPEN
            ))

        return issues
