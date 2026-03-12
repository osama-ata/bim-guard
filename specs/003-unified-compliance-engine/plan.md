# Implementation Plan: BIMGuard AI – Unified Compliance Engine

**Branch**: `003-unified-compliance-engine` | **Date**: 2026-03-11 | **Spec**: [spec.md](spec.md)

## Summary
Build a unified compliance platform that automates the transition from natural language requirements (PDFs) to 3D spatial and metadata validation in IFC models. The system will utilize an LLM-powered ingestion engine for rule extraction and a geometric "Halo" generation engine for soft-clash detection.

## Technical Context
**Language/Version**: Python 3.12, TypeScript/Next.js
**Primary Dependencies**: FastAPI, ifcopenshell, PyMuPDF, trimesh, @thatopen/components
**Storage**: File-based (MVP)
**Testing**: pytest (backend)
**Target Platform**: Web
**Project Type**: Full-stack web application (Turborepo monorepo)

## Project Structure

### Documentation
```text
specs/003-unified-compliance-engine/
├── spec.md              # Feature Specification
├── plan.md              # This document
├── research.md          # Phase 0 Research
├── data-model.md        # Phase 1 Data Design
└── contracts/
    └── api-spec.md      # API Endpoints
```

### Source Code Allocation
- **`apps/api/modules/`**:
  - `module1_doc_reader.py`: PDF text stream extraction.
  - `module3_rule_builder.py`: LLM pipeline for JSON rule generation.
  - `module4_comparator.py`: Geometric and Metadata validation logic.
- **`apps/web/features/compliance/`**:
  - `components/rule-studio/`: Split-screen ingestion UI.
  - `components/viewer/`: Spatial "Halo" visualization layer.
  - `hooks/useComplianceCheck.ts`: API integration hooks.

## Constitution Check
- **Context First**: Plan covers both Next.js frontend and Python backend environments.
- **Imports**: Following absolute import conventions.
- **Dependencies**: Adding `PyMuPDF` and `trimesh` (necessary for core feature logic).
- **Large IFC Handling**: Spatial checks will be performed on simplified V-HACD convex hulls to ensure scalability.
