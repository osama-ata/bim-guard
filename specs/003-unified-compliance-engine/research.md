# Research: Unified Compliance Engine

**Branch**: `003-unified-compliance-engine` | **Date**: 2026-03-11

## R1: Document-to-Rule Conversion Pipeline (Module 1 & 3)

**Decision**: Use `PyMuPDF` (fitz) for reliable text stream extraction from PDFs, followed by a structured LLM pipeline (GPT-4o or similar) to map natural language requirements to a predefined `BIMRule` JSON schema.

**Rationale**: `PyMuPDF` is exceptionally fast and preserves spatial layout, which is critical for associating rule text with specific document sections. By enforcing a standard JSON schema for rules (naming, geometric, spatial), we simplify the Comparator's job. Human-in-the-Loop is facilitated by returning a "confidence score" alongside the extracted fields.

**Alternatives considered**:
- **AWS Textract/Azure Form Recognizer**: High cost and potential data residency issues. Overkill for predominantly text-based BEPs.
- **Tesseract OCR**: Poor accuracy for complex layouts and tables found in building codes.

---

## R2: Spatial "Halo" Generation (Module 4)

**Decision**: Implement "Halos" as offset meshes using `ifcopenshell.geom` and `trimesh`. Specifically, utilize Minkowski Sum for simple primitives or V-HACD (Volumetric Hierarchical Approximate Convex Decomposition) to simplify complex geometries before applying offsets.

**Rationale**: Standard "hard" clash detection only finds physical intersections. By generating a simplified collision hull (Halo) and performing intersection tests using the GJK (Gilbert-Johnson-Keerthi) algorithm via `trimesh` or `scipy`, we can identify spatial violations with high performance. V-HACD ensures that complex equipment (pumps, UPS) is simplified into manageable convex hulls for faster processing.

**Alternatives considered**:
- **Pure Boundig Box checks**: High rate of false positives.
- **Full BREP intersection**: Computationally prohibitive for large models.

---

## R3: BCF 2.1 vs 3.0 Export (Module 5)

**Decision**: Target **BCF 2.1 XML** for the initial implementation.

**Rationale**: While BCF 3.0 is more modern, BCF 2.1 remains the industry standard with the broadest compatibility across Revit, Navisworks, and Solibri. It is localized, easy to generate as a ZIP of XML files, and avoids the complexity of the newer REST-based 3.0 requirements.

---

## R4: Frontend 3D Logic & "Halo" Visualization

**Decision**: Leverage `@thatopen/components` for the main viewer and implement a custom `HaloLayer` in Three.js for semi-transparent visualization.

**Rationale**: `@thatopen/components` provides the best out-of-the-box IFC parsing and fragment management for web. A custom layer allows us to toggle "Halo" visibility without modifying the core IFC fragments, ensuring smooth performance.
