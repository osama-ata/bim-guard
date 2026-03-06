# 🛡️ BIMGUARD AI

**Unified Compliance Engine for BIM Validation**

**Group 5** — Letícia · Malak · Marc · Mark · Osama

`FMP Plenary 1` | `MAICEN Module 10`

---

## THE GOAL: Automating Complex Compliance Validation

BIMGUARD streamlines the validation of complex 3D geometry and project requirements to ensure absolute adherence to Building Codes and ISO 19650 standards.

- **$15.8B**: Annual U.S. losses from interoperability failures _(NIST GCR 04-867)_
- 📐 **Code Conformance**: Automating architectural cross-checks against Building Codes (e.g., fire protection walls, accessibility and door swings).
- 📋 **BEP & EIR Alignment**: Ensuring strict adherence to ISO 19650 naming, classification, and parameter rules directly within the validation pipeline.

---

## OUR SOLUTION: A "Digital Inspector" for openBIM

BIMGUARD AI bridges unstructured documents (BEPs, EIRs, codes) and structured IFC models through a dual-core engine.

### 🧠 NLP Core — Rule Extraction

LLMs (OpenAI/Anthropic) parse BEP, EIR & code PDFs → convert clauses into structured, human-reviewed JSON/SHACL rules.

> **Focus areas:** `Naming Rules` · `Classification` · `Parameters`

### 📐 Geometry Core — Halo Engine

Generates volumetric "Halo" clearance zones around end-of-line and in-line assets. Accounts for Final LOD gaps (e.g., seismic bracing), optimum centre-to-centre service distances, and prevents galvanic corrosion by verifying pipe material distances.

> **Focus areas:** `Maintenance Access` · `Service Spacing` · `Material Checking`

---

## USE CASE: Weekly Coordination & Compliance

On "model drop day," BIMGUARD AI automates critical checkpoints:

**1. Gatekeeper Check**
Validates uploaded IFC against BEP and EIR requirements — flags missing parameters, naming violations (ISO 19650), and incorrect classification codes.

**2. Geometry & Clearance Checks**
Generates "Halo" zones around assets for maintenance access. Validates architectural code compliance (fire ratings, accessibility) and cross-checks service spacing/materials.

**Output:** **BCF Issues** communicating breached codes/standards, assigned to correct parties with trackable progress.

---

## PROGRESS: Where We Are Now

### ✅ Completed

- Problem framing & methodology submitted
- Next.js 16 + Tailwind v4 frontend scaffold
- 3D IFC viewer (`@thatopen/components`)
- FastAPI backend with Docker setup
- MkDocs project documentation site

### 🚧 In Progress

- Rule Studio — PDF ingestion → rule extraction
- Properties panel & element inspection
- Halo engine prototype with IfcOpenShell
- BCF export integration and issue tracking
- Compliance analysis workflow UI

**Tech Stack:** `Next.js` · `FastAPI` · `IfcOpenShell` · `Three.js` · `OpenAI API` · `IFC4 RV`

---

## OPEN DISCUSSION: Questions for the Cohort

We'd appreciate your thoughts on these areas:

- 🎯 **Scope Boundary:** How deep should the LLM-driven rule extraction go? Full automation vs. a structured suggestion interface where experts curate rules?
- ⚖️ **Validation Approach:** What metrics best demonstrate compliance accuracy — precision/recall on expert-annotated BEPs/EIRs, or real-world pilot results from live projects?
- 🌍 **Multi-Jurisdiction Rules:** Building codes vary by country and region. Any experience with modular rule-package architectures for handling jurisdiction-specific requirements?

---

# 🛡️ Thank You

**We welcome your feedback and questions.**

📂 `github.com/osama-ata/bim-guard` | `Group 5 — MAICEN M10`
