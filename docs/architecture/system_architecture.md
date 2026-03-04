---
title: "BIMGuard AI System Architecture"
output: pdf_document
export_on_save:
  prince: true
prince:
  css: "style.css"
presentation:
  width: 1200
  height: 900
---

# BIMGuard AI System Architecture

This document visualizes the system architecture for **BIMGuard AI**. It is structured around five core functional modules that automate the transition from static requirements to digital compliance.

## 1. High-Level System Architecture

This diagram illustrates the system flow, categorized into the five requested modules: **(1) Document Reader**, **(2) IFC Reader**, **(3) Rule Converter**, **(4) Comparator**, and **(5) Reporting**.

```mermaid
graph TD
    %% Actors
    subgraph "Actors"
        User((User))
    end

    %% Frontend
    subgraph Frontend
        UI[Next.js Web App]
        Upload["File Uploader<br/>(PDF Standards, BEPs, IFC Models)"]
        Vis["Results Visualization"]
        Exp["Export Reports"]
        
        UI --> Upload
        UI --> Vis
        UI --> Exp
    end

    %% Orchestration
    Orchestrator["Workflow Orchestrator"]
    
    %% Backend Modules
    subgraph "Backend System"
    
        %% Data Store
        subgraph DB ["Data_Store"]
            RuleStore[("Rule Database<br/>(JSON/Regex/SHACL)")]
        end

        %% Module 1: Document Parsing
        subgraph Mod1 ["Module_1_Document_Reader"]
            DocParser["Doc_Parser<br/>(PDF/Text Extraction)"]
        end

        %% Module 2: IFC Reading
        subgraph Mod2 ["Module_2_IFC_Data_Extractor"]
            IFCRead["IFC_Parser<br/>(IfcOpenShell)"]
            AttrExt["Attribute_Extractor"]
            GeomExt["Geometry_Extractor"]
            
            IFCRead --> AttrExt
            IFCRead --> GeomExt
        end

        %% Module 3: Rule Logic
        subgraph Mod3 ["Module_3_Rule_Converter"]
            NLP["NLP_Engine<br/>(LLM / Prompt_Engineering)"]
            RuleGen["Rule_Generator<br/>(Natural_Language -> Structured_Rules)"]
            
            NLP --> RuleGen
        end

        %% Module 4: Comparison
        subgraph Mod4 ["Module_4_Compliance_Comparator"]
            AttrComp["Attribute_Comparator<br/>(Metadata vs Rules)"]
            SpatComp["Spatial_Comparator<br/>(Geometry vs Rules)"]
        end

    end

        %% Module 5: Output
        subgraph Mod5 ["Module_5_Reporting"]
            ReportGen["Report_Generator<br/>(BCF, PDF, CSV)"]
        end
    %% Workflow Connections
    User --> Frontend
    Frontend --> Orchestrator
    
    %% Flows
    Orchestrator --> Mod1
    Orchestrator --> Mod2 --> Mod4
    Mod4 --> Mod5
    Mod5 --> Orchestrator
    
    %% 1. Read Docs -> 3. Convert to Rules -> Store
    DocParser --> NLP
    RuleGen --> RuleStore --> Mod4

  
```

## 2. Module 1 & 3: Rule Extraction Workflow (Sequence)

This sequence details how the system reads documents (Module 1) and converts them into rules (Module 3).

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Mod1 as Module 1 (Doc Reader)
    participant Mod3 as Module 3 (NLP/Rule Gen)
    participant DB as RuleStore

    User->>Frontend: Upload BEP / Code PDF
    Frontend->>Mod1: Send PDF File
    Mod1->>Mod1: Extract Raw Text from PDF
    Mod1-->>Mod3: Send Text Chunks
    
    Note over Mod3: Prompt: "Convert text requirements<br/>to machine-readable logic"
    
    Mod3->>Mod3: LLM Interpretation
    Mod3->>Mod3: Generate JSON/Regex Rules
    Mod3->>DB: Save Rules to Database
    
    Mod3-->>Frontend: Return Extracted Rules
    Frontend->>User: Display Rules for Confirmation
```

## 3. Module 2 & 4: Compliance Checking Flow (Geometry)

This flow details the geometric analysis, where IFC data (Module 2) is checked against rules (Module 4).

```mermaid
flowchart LR
    %% Module 2
    subgraph "Module 2: IFC Extraction"
        Input[IFC File] --> IFC[IFC Parser]
        IFC --> Geom[Geometry Extractor]
    end

    %% Module 4
    subgraph "Module 4: Spatial Comparator"
        Geom --> Voxel["V-HACD Decomposition<br/>(Simplify Geometry)"]
        
        Rules[(Rule Store)] --> Logic["Fetch Clearance Rules"]
        
        Voxel --> Minkowski["Halo Generation<br/>(Minkowski Sum)"]
        Logic --> Minkowski
        
        Minkowski --> Collision["Intersection Test<br/>(GJK Algorithm)"]
    end

    %% Module 5
    subgraph "Module 5: Reporting"
        Collision -->|Clash Found| BCF["Generate BCF Issue"]
    end
```

## 4. Implementation Stack (Class Structure)

Below is the recommended codebase structure, organized by the five modules.

```mermaid
classDiagram
    class BIMGuard_App {
        +run_dashboard()
        +orchestrate_workflow()
    }
    
    class Module1_DocReader {
        +parse_pdf()
        +extract_text_sections()
    }

    class Module2_IFCRead {
        +load_ifc_file()
        +get_all_elements()
        +extract_properties()
        +extract_geometry()
    }

    class Module3_RuleBuilder {
        +generate_regex_from_text()
        +build_shacl_shapes()
        +save_rule_to_db()
    }
    
    class Module4_Comparator {
        +validate_metadata()
        +check_naming_conventions()
        +check_spatial_clearances()
    }
    
    class Module5_Reporter {
        +create_bcf_topic()
        +generate_csv_summary()
        +render_visual_report()
    }

    BIMGuard_App --> Module1_DocReader
    BIMGuard_App --> Module2_IFCRead
    BIMGuard_App --> Module3_RuleBuilder
    BIMGuard_App --> Module4_Comparator
    BIMGuard_App --> Module5_Reporter
```
