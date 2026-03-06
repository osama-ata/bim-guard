# Final Master’s Project Submission 1: Problem Framing and Methodological Definition

## BIMGUARD AI — A Unified Compliance Engine for BEP and Spatial Code Validation

**Authors:** Letícia Cristovam Clemente | Malak Yaseen | Marc Azzam | Mark Shane Haines | Osama Ata

## 1.1 Problem Framing Analysis

### Market Need Assessment

The AECO industry faces substantial inefficiencies from inadequate interoperability among design, engineering, and facility management systems. A NIST study estimated annual losses of 15.8 billion USD in the U.S. capital facilities sector, driven mainly by rework, manual data re-entry, and fragmented information flows (Gallaher et al., 2004). As project complexity increases and digital delivery becomes standard, demand grows for automated, standards-based BIM validation that works across heterogeneous toolchains rather than within a single proprietary platform.

### State-of-Practice Review

Existing industry tools offer only partial solutions. Model coordination platforms like Navisworks support both hard clashes (physical intersections) and clearance-based soft clashes and are used at key coordination milestones. However, these platforms require manually configured clash tests and cannot natively process unstructured documentation—such as BIM Execution Plans (BEPs), project requirements, and building codes—to automatically derive the rules they enforce. In contrast, BIMGUARD AI processes BEP and code documents to suggest rule logic, reducing manual effort and interpretation errors.

The openBIM ecosystem, based on IFC and Model View Definitions (MVDs) like IFC2x3 Coordination View and IFC4 Reference View, enables vendor-neutral model exchange (buildingSMART International, 2020). Yet automated compliance checking workflows for IFC models remain largely research-driven, typically addressing narrow rule sets (Eastman et al., 2009).

### Gap Identification

A significant gap exists between human-authored requirements in unstructured documents and the structured, machine-readable rules needed for large-scale IFC model validation. Geometric coordination workflows mainly address clashes between physical elements, while many regulatory and operational requirements deal with “soft” spatial conditions: maintenance zones, clearances in front of equipment, and safe egress widths—invisible volumes that must remain unobstructed rather than explicit model objects.

For example, a storage cabinet may intrude into the required clear zone in front of an electrical panel as defined by NFPA 70, creating a hazard that standard clash detection does not flag (NFPA, 2023). On the information side, naming conventions, classification schemes, and parameter requirements from ISO 19650–aligned requirements and project BEPs are still checked manually using spreadsheets and ad-hoc scripts.

BIMGUARD AI addresses this gap by:

- Operating directly on IFC models exported via openBIM MVDs—primarily IFC4 Reference View, with IFC2x3 Coordination View as fallback—ensuring tool independence.
- Using Large Language Models (LLMs) to translate selected BEP and building code clauses into structured, human-reviewed rule definitions.
- Programmatically generating and verifying “Halo” clearance volumes and information rules against IFC geometry and metadata, producing vendor-neutral BCF issues usable by any BCF-enabled platform.

_(Figure 1. Problem gap analysis: current practice versus BIMGUARD AI coverage.)_

## 1.2 Data Strategy

### Data Sources and Types

The system uses two main data streams. Structured geometry and metadata come from IFC models exported using openBIM Model View Definitions. The primary target is IFC4 Reference View (RV 1.2), designed by buildingSMART for workflows where models are viewed and analysed but not parametrically edited—aligning with BIMGUARD AI’s role as an external compliance engine. Where authoring tools cannot produce reliable IFC4 exports, IFC2x3 Coordination View 2.0 serves as a fallback.

Unstructured documentation includes PDF or text files containing BEPs, project information requirements, and relevant building code sections at national and international levels, including ISO-based frameworks (ISO, 2018). These documents define both geometric constraints (for example, clearances, access zones) and information requirements (for example, naming, classification).

A central challenge arises from the variation of building codes among regions and countries, which differ in terminology, scope, and specific rule thresholds. To address this, BIMGUARD AI adopts a modular rule-package architecture. Project teams can define, select, or combine rule sets for specific jurisdictions or project types, linking each rule to its legal source. This allows for local variations while maintaining a consistent validation framework.

### Data Preparation Workflow

The data pipeline is multi-stage. IFC data is parsed using IfcOpenShell to extract geometry, spatial structure, element classifications, property sets, and relationships, while text is extracted from BEP and regulatory PDFs. During normalisation, parsed IFC features are loaded into structured dataframes (via pandas/numpy) exposing element types, locations, and rule-checking attributes. Intermediate representations—element catalogues, adjacency tables, and equipment lists—are built from IFC entities and property sets.

For rule conversion, NLP/LLMs propose candidate rules from human-readable text, captured in structured templates specifying target class, parameter, operator, threshold, and citation. Domain experts review these candidates before encoding them as machine-executable JSON rules and, where appropriate, SHACL constraints on linked IFC data.

### Data Governance and Ethics

To promote responsible AI practice, the project adopts a White Box Architecture. All operational rules are maintained in open, human-readable formats (JSON, SHACL) and explicitly linked to originating clauses in BEPs, codes, and standards. LLM outputs are treated as suggestions: each proposed rule undergoes human review, version control, and provenance documentation before inclusion in the rulebase.

Evaluation metrics including precision and recall against expert-annotated benchmarks will be defined during the pilot phase. This ensures transparency, auditability, and human oversight while mitigating risks of hidden bias or misinterpretation.

## 1.3 AI Approach

### AI Model Family and Architectures

BIMGUARD AI adopts a hybrid architecture using IFC as the primary data source.

- **Natural Language Processing (NLP):** Large Language Models accessed via cloud APIs (for example, OpenAI, Anthropic) interpret selected clauses from BEPs and building codes. An LLM-based approach was chosen over traditional NER or rule-based NLP parsers because building regulations exhibit high linguistic variability and context-dependent semantics that fixed-pattern extractors cannot reliably handle. LLMs convert human-readable requirements into candidate machine-readable rules—parameter constraints, minimum clearances, naming patterns—which domain experts then review and formalise.

- **Computational Geometry over IFC:** The spatial reasoning layer operates directly on IFC models using IfcOpenShell as an open-source geometry engine. This layer computes element locations, bounding volumes, and derived “Halo” clearance regions around maintainable equipment, without reliance on proprietary model APIs. All geometric checks—hard clashes and soft/clearance violations—are expressed in terms of IFC entities, property sets, and coordinates.

- **Rule Representation and Validation Logic:** Validated rules are stored in open, tool-agnostic formats (JSON, SHACL), enabling transparent and auditable rule sets applicable to any IFC model regardless of authoring tool. Computational performance may become a constraint when processing extremely large or federated models. Future phases may therefore explore Graph Neural Networks on IFC-derived graphs to detect recurrent non-compliant patterns more efficiently; however, the initial implementation remains explicitly rule-based and openBIM-centric.

### Conceptual Pipeline

The pipeline (Figure 2) ensures all core processing occurs on IFC and open formats, with proprietary BIM tools as interchangeable clients at the edges. At input, users upload an IFC model (IFC4 Reference View preferred, IFC2x3 fallback) and relevant documentation as PDF or text files; no proprietary API access is required. The workflow follows three steps: Upload (users provide the model and documentation), Review (the system processes data, interprets requirements, and runs compliance checks automatically), and Receive (users get clear, actionable BCF issue reports importable into any BCF-enabled platform).

During processing, the LLM proposes candidate rules from curated excerpts in a structured template; accepted rules are stored as JSON/SHACL. Simultaneously, the IFC model is parsed and the geometry engine computes Halo volumes using rulebase parameters. Validation encompasses information checks (naming and parameter conventions per ISO 19650, mandatory attributes, classification codes) and spatial checks (Halo volume intersections, insufficient clearances, missing access zones). Each non-compliance is linked to the specific IFC element(s), rule identifier, and documentation reference. Output consists of BCF issues—including viewpoints, element references, and rule metadata—consumable by any BCF-enabled BIM platform.

_(Figure 2. BIMGUARD AI conceptual pipeline: from openBIM input to vendor-neutral BCF output.)_

## References

- buildingSMART International. (2020). _IFC4 Reference View._ https://standards.buildingsmart.org/MVD/RELEASE/IFC4/ADD2_TC1/RV1_2/
- Eastman, C., Lee, J., Jeong, Y., & Lee, J. (2009). Automatic rule-based checking of building designs. _Automation in Construction, 18_(8), 1011–1033.
- Gallaher, M. P., O’Connor, A. C., Dettbarn, J. L., & Gilday, L. T. (2004). _Cost Analysis of Inadequate Interoperability in the U.S. Capital Facilities Industry (NIST GCR 04-867)._ National Institute of Standards and Technology.
- ISO. (2018). _ISO 19650-1:2018 — Organisation and digitisation of information about buildings and civil engineering works._ International Organization for Standardization.
- NFPA. (2023). _NFPA 70: National Electrical Code._ National Fire Protection Association.
