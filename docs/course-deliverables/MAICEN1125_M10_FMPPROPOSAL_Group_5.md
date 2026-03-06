# Final Master’s Project Proposal – Group 5

**BIMGUARD AI – A Unified Compliance Engine for BEP and Spatial Code Validation**

## 1 Selected Topic Area

This project addresses two core areas defined in the FMP Syllabus:

- AI applied to BIM technology: Utilizing AI to validate BIM data and enrich models for interoperability.
- AI applied to automation and robotics: Specifically, regarding automated spatial validation and rule generation to support maintainability.

## 2 Problem Statement and Use Case Definition

### 2.1 The Challenge: The Design-to-Technical Gap

The AEC industry faces a critical “Design-to-Technical Gap,” a primary driver of an estimated 15.8 billion dollars in annual losses in the U.S. capital facilities sector due to rework and interoperability failures.

This gap is most evident in the industry’s inability to detect “soft clashes,” violations of invisible but mandatory operational, maintenance, or accessibility zones.

Current tools (e.g., Navisworks) focus on physical “hard clashes” and lack the semantic nuance to enforce requirements that exist only in text documents.

This results in buildings that are geometrically perfect but operationally illegal or unsafe, leading to severe legal repercussions and negligence claims, as seen in cases like Ellis v. ICC Group Inc.

### 2.2 Specific Use Case

The project targets a weekly BIM coordination cycle for a large-scale data center.

In the existing workflow, “model drop day” relies on manual checklists to verify compliance against the BIM Execution Plan (BEP) and technical codes.

BIMGUARD AI automates this by acting as a “Digital Inspector” at two critical decision-making points:

1. **Gatekeeper Check**: Upon upload, the system validates the model against the BEP, flagging missing parameters or naming violations (e.g., ISO 19650 compliance).
2. **Soft Clash Detection**: It programmatically generates “Halo” clearance zones around maintainable equipment (e.g., UPS units, pumps) to detect blocked access or unsafe working clearances that standard clash detection misses.

## 3 Technical Rationale and Relevance of AI

BIMGUARD AI bridges the gap between unstructured human documentation and structured model data through a “Dual-Core” engine.

The application of AI is crucial for transitioning from static validation to proactive design assistance.

### 3.1 AI Approach and Methodology

- Natural Language Processing (NLP): We utilize NLP (via OpenAI/Anthropic APIs) to interpret unstructured PDF documents, including Building Energy Performance Standards (BEPs) and building codes. The system extracts human-readable rules and converts them into machine-executable Regular Expressions (Regex) and structured constraints.

- Computational Geometry and the “Halo” Effect: Unlike standard bounding-box checks, our “Logic Engine” utilizes the IfcOpenShell library to calculate and generate volumetric buffers (“Halos”) representing required clearance zones.

- White Box Architecture: To ensure transparency and trust, a key “Responsible AI” principle, the system avoids “Black Box” logic by storing rules in open standards (JSON/SHACL), making the decision-making process auditable.

### 3.2 Data Strategy and Integration

The system processes IFC models (geometry and metadata) and PDF documents (BEP and Codes).

It integrates directly into the coordination workflow by outputting results not as static reports, but as BIM Collaboration Format (BCF) files.

This allows the user to import identified issues (with coordinates and viewpoints) directly into authoring tools, such as Revit, for immediate resolution.

## 4 Team Description

- **Letícia Cristovam Clemente (Project Manager and Workflow Lead)**: Design Associate at Olsson supporting Google Data Centers. She brings expertise in BIM coordination, workflow validation, and CPM scheduling, and her role focuses on data structuring and interdisciplinary management.

- **Mark Shane Haines (MEP Services Lead Coordinator)**: BIM Consultant and owner of Aspiring Design 3D Consultancy (New Zealand). He possesses deep domain expertise in BIM Documentation Workflows and scan-to-BIM space planning, predominantly for the Semiconductor industry.

- **Malak Yaseen (Product Driver and Domain Lead)**: BIM Architect and founder of Archinova.ai (Canada/Middle East). With a background in architectural design and 3D rendering, she leads the product vision and visual presentation of the project.

- **Osama Ata (Software Developer and Systems Architect)**: Contracts Manager at Archirodon. He leverages his practical experience with AI solutions to guide the selection and implementation of technology stacks.

- **Marc Azzam (BIM Manager)**: Based in Abu Dhabi with extensive experience in implementing and managing Building Information Modeling processes across large-scale projects. He is skilled in interdisciplinary coordination, BIM execution planning, and digital workflow optimization, ensuring seamless integration between design, engineering, and construction teams.
