# Feature Specification: BIMGuard AI – Unified Compliance Engine

**Feature Branch**: `003-unified-compliance-engine`  
**Created**: 2026-03-11  
**Status**: Draft  
**Input**: User description: "A professional compliance automation platform for IFC models to bridge the Design-to-Technical Gap, detecting soft clashes and BEP violations using AI-extracted rules and geometric Halo generation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Insight Ingestion (Document to Rule Conversion) (Priority: P1)

As a BIM Manager, I want to upload unstructured PDF documents (like Building Energy Performance Standards, BEPs, or Building Codes) so that the system's AI can extract and convert them into machine-executable rules (Regex/JSON) for compliance checking.

**Why this priority**: Documenting logic in executable formats is currently a massive manual bottleneck. Automating this "ingestion" to create the "AI Brain" is essential for systemic scale.

**Independent Test**: Upload a sample BEP PDF, verify that the NLP engine extracts text, and ensure the UI presents a split-screen "Diff" view for Human-in-the-Loop validation.

**Acceptance Scenarios**:

1. **Given** a user is on the Rule Extraction Studio page, **When** they upload a PDF document, **Then** the system displays a progress bar and subsequently presents the extracted rules alongside the original PDF text.
2. **Given** an AI-extracted rule is presented, **When** the user edits and clicks "Approve", **Then** the rule is saved to the Rule Store database in a structured format (JSON/SHACL).

---

### User Story 2 - Gatekeeper Check (Metadata Validation) (Priority: P1)

As a BIM Coordinator, I want to upload an IFC model and select a BEP Rule Set so that the system can automatically flag missing parameters or naming convention violations (e.g., ISO 19650 compliance) upon upload.

**Why this priority**: Enforcing data standards at the "model drop" gate reduces downstream coordination issues and ensures the model is valid for technical analysis.

**Independent Test**: Upload an IFC model with known naming errors, apply a metadata rule set, and verify that the system catches the specific naming violations.

**Acceptance Scenarios**:

1. **Given** an uploaded IFC model and selected BEP rules, **When** the user runs the compliance check, **Then** the system's Attribute Comparator validates the IFC metadata against the rules.
2. **Given** the compliance check completes, **When** there are naming convention violations, **Then** the system logs them as warning/critical issues in the Results Viewer.

---

### User Story 3 - Soft Clash Detection (Spatial "Halo" Validation) (Priority: P1)

As an MEP Services Lead, I want the system to generate "Halo" clearance zones around maintainable equipment (e.g., UPS units, pumps) so that I can detect blocked access or unsafe working clearances that standard Navisworks hard-clash detection misses.

**Why this priority**: Soft clashes represent a significant operational risk that is often overlooked in traditional design coordination.

**Independent Test**: Upload an IFC model containing a pump placed too close to a wall, run the spatial check, and verify the system flags the intersection of the pump's generated clearance "Halo" with the wall.

**Acceptance Scenarios**:

1. **Given** an IFC model containing maintainable equipment, **When** the Spatial Comparator runs, **Then** it generates volumetric buffers ("Halos") using Minkowski Sum and V-HACD decomposition based on the active rules.
2. **Given** a generated Halo intersects with another physical element's geometry, **When** the GJK intersection test runs, **Then** a "Clearance Violation" issue is generated.

---

### User Story 4 - Analysis Review & Reporting (Priority: P2)

As a Project Manager, I want to visualize the compliance issues in a 3D web viewer and export them as BCF files so that I can seamlessly assign them to my design team in their native authoring tools (e.g., Revit).

**Why this priority**: Feedback loops must be closed within the existing professional BIM ecosystem.

**Independent Test**: Generate a mock compliance issue, view it in the 3D canvas, and successfully export a valid .bcfzip file.

**Acceptance Scenarios**:

1. **Given** a completed compliance check with issues, **When** the user clicks an issue in the Left Sidebar, **Then** the 3D Viewer zooms to the element and displays the failing element in red and the "Halo" zone in semi-transparent yellow.
2. **Given** a list of confirmed issues, **When** the user clicks "Export BCF", **Then** the system generates and downloads a standard BIM Collaboration Format (BCF) report.

---

### Edge Cases

- **Non-Text Documents**: Graceful failure or OCR prompt for PDFs containing images instead of text streams.
- **Complex Geometries**: V-HACD decomposition must handle high-vertex meshes without timing out (polygon limits or LOD reduction).
- **Ambiguous Rules**: Human-in-the-Loop UI must highlight low confidence and mandate manual resolution.
- **Ultra-Large Models**: Handling models > 1GB in the web viewer via streaming or fragmentation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse PDF documents (Standards, BEPs) to extract unstructured text requirements.
- **FR-002**: System MUST utilize an NLP Engine (LLM) to convert extracted text into machine-readable logic (JSON/Regex/SHACL).
- **FR-003**: System MUST provide a split-screen "Diff" UI for users to review, edit, and approve AI-generated rules.
- **FR-004**: System MUST parse .ifc files using IfcOpenShell to extract both geometry and attributes.
- **FR-005**: System MUST perform Attribute Comparison between IFC metadata and the Rule Store.
- **FR-006**: System MUST perform Spatial Comparison by generating Clearance Halos (Minkowski Sum) and testing for intersections (GJK Algorithm).
- **FR-007**: System MUST display an IDE-style Compliance Viewer using @thatopen/components and Three.js.
- **FR-008**: System MUST generate and export BIM Collaboration Format (BCF) reports.

### Key Entities

- **Document**: Represents an uploaded PDF (BEP, Code, Standard).
- **Rule**: A structured, machine-readable constraint (JSON/Regex/SHACL).
- **Project**: A workspace containing linked Documents, Rule Sets, and IFC Models.
- **IFC Model**: A 3D building model file uploaded by the user.
- **Compliance Issue**: A flagged violation (Metadata/Spatial).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: >80% accuracy in Rule Extraction prior to human intervention.
- **SC-002**: Handle IFC models up to 500MB without backend OOM errors.
- **SC-003**: 90% of spatial "soft clashes" defined in rules are successfully identified.
- **SC-004**: 100% valid BCF export compatible with standard BIM tools (Revit, Solibri).
