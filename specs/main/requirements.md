# **Feature Specification: BIMGuard AI – Unified Compliance Engine**

**Feature Branch**: main (Core Platform)

**Created**: \[Current Date\]

**Status**: Draft

**Input**: User description: "A professional compliance automation platform for IFC models to bridge the Design-to-Technical Gap, detecting soft clashes and BEP violations using AI-extracted rules and geometric Halo generation."

## **User Scenarios & Testing *(mandatory)***

### **User Story 1 \- Insight Ingestion (Document to Rule Conversion) (Priority: P1)**

As a BIM Manager, I want to upload unstructured PDF documents (like Building Energy Performance Standards, BEPs, or Building Codes) so that the system's AI can extract and convert them into machine-executable rules (Regex/JSON) for compliance checking.

**Why this priority**: This is the foundation of the platform's "AI Brain." Without extracted rules, the system has nothing to validate the IFC models against.

**Independent Test**: Can be fully tested by uploading a sample BEP PDF, verifying that the NLP engine extracts text, and ensuring the UI presents a split-screen "Diff" view for Human-in-the-Loop validation.

**Acceptance Scenarios**:

1. **Given** a user is on the Rule Extraction Studio page, **When** they upload a PDF document, **Then** the system displays a progress bar and subsequently presents the extracted rules alongside the original PDF text.  
2. **Given** an AI-extracted rule is presented, **When** the user edits and clicks "Approve", **Then** the rule is saved to the Rule Store database in a structured format (JSON/SHACL).

### ---

**User Story 2 \- Gatekeeper Check (Metadata Validation) (Priority: P1)**

As a BIM Coordinator, I want to upload an IFC model and select a BEP Rule Set so that the system can automatically flag missing parameters or naming convention violations (e.g., ISO 19650 compliance) upon upload.

**Why this priority**: Automating manual checklists for "model drop days" is a primary value proposition, reducing immediate rework and enforcing data standards.

**Independent Test**: Can be fully tested by uploading an IFC model with known naming errors, applying a static metadata rule set, and verifying that the system catches the specific naming violations.

**Acceptance Scenarios**:

1. **Given** an uploaded IFC model and selected BEP rules, **When** the user runs the compliance check, **Then** the system's Attribute Comparator validates the IFC metadata against the rules.  
2. **Given** the compliance check completes, **When** there are naming convention violations, **Then** the system logs them as warning/critical issues in the Results Viewer.

### ---

**User Story 3 \- Soft Clash Detection (Spatial "Halo" Validation) (Priority: P1)**

As an MEP Services Lead, I want the system to generate "Halo" clearance zones around maintainable equipment (e.g., UPS units, pumps) so that I can detect blocked access or unsafe working clearances that standard Navisworks hard-clash detection misses.

**Why this priority**: Resolving the industry's inability to detect "soft clashes" is the core differentiator of BIMGUARD AI, directly preventing operational and legal liabilities.

**Independent Test**: Can be fully tested by uploading an IFC model containing a pump placed too close to a wall, running the spatial check, and verifying the system flags the intersection of the pump's generated clearance "Halo" with the wall.

**Acceptance Scenarios**:

1. **Given** an IFC model containing maintainable equipment, **When** the Spatial Comparator runs, **Then** it generates volumetric buffers ("Halos") using Minkowski Sum and V-HACD decomposition based on the active rules.  
2. **Given** a generated Halo intersects with another physical element's geometry, **When** the GJK intersection test runs, **Then** a "Clearance Violation" issue is generated.

### ---

**User Story 4 \- Analysis Review & Reporting (Priority: P2)**

As a Project Manager, I want to visualize the compliance issues in a 3D web viewer and export them as BCF files so that I can seamlessly assign them to my design team in their native authoring tools (e.g., Revit).

**Why this priority**: While validation is critical, the results must be actionable. BCF export integrates BIMGUARD AI directly into the existing industry workflow.

**Independent Test**: Can be fully tested by generating a mock compliance issue, viewing it in the 3D canvas, and successfully exporting a valid .bcfzip file.

**Acceptance Scenarios**:

1. **Given** a completed compliance check with issues, **When** the user clicks an issue in the Left Sidebar, **Then** the 3D Viewer zooms to the element and displays the failing element in red and the "Halo" zone in semi-transparent yellow.  
2. **Given** a list of confirmed issues, **When** the user clicks "Export BCF", **Then** the system generates and downloads a standard BIM Collaboration Format (BCF) report.

### ---

**Edge Cases**

* What happens when a PDF document contains images of text rather than actual text streams? (System should gracefully fail or prompt for OCR).  
* How does the system handle highly complex IFC geometries (e.g., detailed meshes) during V-HACD decomposition? (System should implement polygon limits, LOD reduction, or timeouts to prevent memory exhaustion).  
* What happens when the AI rule extractor outputs ambiguous or contradictory logic? (Human-in-the-Loop UI must highlight low confidence scores and mandate manual correction).  
* How does the system handle extremely large IFC models (\>1GB) in the Next.js web viewer?

## **Requirements *(mandatory)***

### **Functional Requirements**

* **FR-001**: System MUST parse PDF documents (Standards, BEPs) to extract unstructured text requirements (Module 1).  
* **FR-002**: System MUST utilize an NLP Engine (LLM) to convert extracted text into machine-readable logic (JSON/Regex/SHACL) (Module 3).  
* **FR-003**: System MUST provide a split-screen "Diff" UI for users to review, edit, and approve AI-generated rules before saving them to the Rule Database.  
* **FR-004**: System MUST parse .ifc files using IfcOpenShell to extract both geometry and attributes (Module 2).  
* **FR-005**: System MUST perform Attribute Comparison between IFC metadata and the Rule Store to validate naming conventions and parameter presence (Module 4).  
* **FR-006**: System MUST perform Spatial Comparison by generating Clearance Halos (Minkowski Sum) around elements and testing for intersections (GJK Algorithm) (Module 4).  
* **FR-007**: System MUST display an IDE-style Compliance Viewer using @thatopen/components and Three.js, highlighting failing elements and spatial halos.  
* **FR-008**: System MUST generate and export BIM Collaboration Format (BCF) reports for flagged issues (Module 5).

### **Key Entities *(include if feature involves data)***

* **Document**: Represents an uploaded PDF (BEP, Code, Standard). Contains raw text chunks and metadata.  
* **Rule**: A structured, machine-readable constraint (JSON/Regex/SHACL) extracted from a Document. Attributes include Category (e.g., IfcWall), Logic, and Confidence Score.  
* **Project**: A workspace containing linked Documents, Rule Sets, and IFC Models.  
* **IFC Model**: A 3D building model file uploaded by the user.  
* **Compliance Issue**: A flagged violation. Attributes include Type (Metadata/Spatial), Element ID, Description, Coordinates, and Status.

## **Success Criteria *(mandatory)***

### **Measurable Outcomes**

* **SC-001**: Users can successfully extract structured validation rules from standard BEP PDFs with an AI confidence/accuracy rate of \>80% prior to human intervention.  
* **SC-002**: System handles IFC model processing (up to 500MB) and Rule extraction without backend timeout or out-of-memory errors.  
* **SC-003**: 90% of spatial "soft clashes" defined in the Rule Store are successfully identified by the Halo generation and intersection engine.  
* **SC-004**: System successfully exports 100% valid BCF files that can be imported seamlessly into standard authoring tools (e.g., Revit, Solibri, Navisworks).