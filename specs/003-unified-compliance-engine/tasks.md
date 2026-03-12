# Tasks: Unified Compliance Engine

**Input**: Design documents from `/specs/003-unified-compliance-engine/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project folders on backend: `apps/api/app/services/rule_evaluators/`, `apps/api/app/data/results/`, `apps/api/app/models/`
- [x] T002 Create project folders on frontend: `apps/web/features/compliance/types/`, `apps/web/features/compliance/hooks/`, `apps/web/features/compliance/components/rule-studio/`
- [x] T003 [P] Add dependencies `PyMuPDF`, `trimesh`, and `scipy` to `apps/api/pyproject.toml`
- [x] T004 Define TypeScript types for compliance in `apps/web/features/compliance/types/compliance.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T005 Create base Pydantic models for RuleSet and Rule in `apps/api/app/models/rule_models.py`
- [x] T006 Create base Pydantic models for ComplianceCheck and ComplianceIssue in `apps/api/app/models/compliance_models.py`
- [x] T007 Implement `ResultStore` for file-based persistence in `apps/api/app/services/result_store.py`
- [x] T008 Implement base `RuleEvaluator` abstract class in `apps/api/app/services/rule_evaluators/base.py`
- [x] T009 [P] Extend `useBIMStore.ts` with compliance state in `apps/web/store/useBIMStore.ts`
- [x] T010 [P] Configure API routing for compliance in `apps/api/app/main.py` and create `apps/api/app/api/endpoints/compliance.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Insight Ingestion (Priority: P1)

**Goal**: Automate PDF rule extraction with human-in-the-loop validation via a split-screen UI.

**Independent Test**: Upload a sample BEP PDF, verify that text is extracted, and rules are presented for approval in the Rule Studio UI.

### Implementation for User Story 1

- [x] T011 [US1] Implement PDF text extraction logic using PyMuPDF in `apps/api/app/modules/module1_doc_reader.py`
- [x] T012 [US1] Implement LLM-based rule extraction pipeline in `apps/api/app/modules/module3_rule_builder.py`
- [x] T013 [US1] Implement `POST /api/v1/ingest` endpoint in `apps/api/app/api/endpoints/compliance.py`
- [x] T014 [US1] Create `IngestionView` split-screen component in `apps/web/features/compliance/components/rule-studio/ingestion-view.tsx`
- [x] T015 [US1] Implement `useRuleIngestion` hook in `apps/web/features/compliance/hooks/useRuleIngestion.ts`

**Checkpoint**: User Story 1 (Rule Ingestion) is functional independently.

---

## Phase 4: User Story 2 - Gatekeeper Check (Priority: P1)

**Goal**: Validate IFC metadata and naming conventions against extracted rule sets.

**Independent Test**: Run a compliance check on an IFC with known naming errors and verify they are flagged in the results.

### Implementation for User Story 4

- [x] T016 [US2] Implement `NamingEvaluator` in `apps/api/app/services/rule_evaluators/naming.py`
- [x] T017 [US2] Implement `MetadataEvaluator` in `apps/api/app/services/rule_evaluators/metadata.py`
- [x] T018 [US2] Implement `ComplianceEngine` service to orchestrate evaluation in `apps/api/app/services/compliance_engine.py`
- [x] T019 [US2] Implement `POST /api/v1/compliance/check` endpoint in `apps/api/app/api/endpoints/compliance.py`
- [x] T020 [US2] Create `RuleSetSelector` component in `apps/web/features/compliance/components/rule-set-selector.tsx`
- [x] T021 [US2] Implement `useComplianceCheck` hook in `apps/web/features/compliance/hooks/useComplianceCheck.ts`

**Checkpoint**: Metadata validation is functional.

---

## Phase 5: User Story 3 - Soft Clash Detection (Priority: P1)

**Goal**: Generate spatial Halos and detect clearance violations using geometric intersection tests.

**Independent Test**: Place an element within the clearance zone of another and verify a "Clearance Violation" is detected.

### Implementation for User Story 3

- [x] T022 [US3] Implement `GeometricEvaluator` (Halos + GJK intersection) in `apps/api/app/services/rule_evaluators/geometric.py`
- [x] T023 [US3] Add `HaloLayer` visualization logic to `apps/web/components/IFCViewer.tsx`
- [x] T024 [US3] Create `HaloControls` component to toggle visibility in `apps/web/features/compliance/components/viewer/halo-controls.tsx`

**Checkpoint**: Spatial compliance checking is functional.

---

## Phase 6: User Story 4 - Analysis Review & Reporting (Priority: P2)

**Goal**: Professional issue visualization and industry-standard BCF export.

**Independent Test**: Navigate to an issue in 3D, verify the zoom-to-element, and export a valid BCF file.

### Implementation for User Story 4

- [x] T025 [US4] Wire `IssueSidebar.tsx` to the compliance results API in `apps/web/features/compliance/components/issue-sidebar.tsx`
- [x] T026 [US4] Wire `InspectorPanel.tsx` to display real violation details in `apps/web/features/compliance/components/inspector-panel.tsx`
- [x] T027 [US4] Implement BCF 2.1 XML generation logic in `apps/api/app/services/bcf_exporter.py`
- [x] T028 [US4] Implement BCF export endpoint in `apps/api/app/api/endpoints/compliance.py`
- [x] T029 [US4] Implement `PATCH` endpoint to update issue status in `apps/api/app/api/endpoints/compliance.py`

**Checkpoint**: All user stories functional and integrated.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T030 Update Swagger documentation for new endpoints on backend
- [x] T031 [P] Run `quickstart.md` validation to ensure developer instructions are correct
- [x] T032 Final end-to-end smoke test of the full compliance pipeline
- [x] T033 Code cleanup and refactoring of `ComplianceEngine` logic

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup (Phase 1). BLOCKS all user stories.
- **User Stories (Phase 3-6)**: All depend on Foundational (Phase 2).
  - US2 builds on the rule structure from US1 but can be mock-tested.
  - US3 and US4 are mostly independent but benefit from US2's endpoint structure.
- **Polish (Phase 7)**: Depends on completion of all stories.

### Parallel Opportunities

- T003, T004, T009, T010 can be done in parallel (backend vs frontend split).
- Once Phase 2 is done, User Story 1 (Ingestion) and User Story 2 (Checking) can proceed in parallel if backend/frontend data is mocked appropriately.
- T031 and T032 can be done in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Setup and Foundation.
2. Implement User Story 1 (Rule Ingestion).
3. Implement User Story 2 (Basic Metadata Checking).
4. **STOP and VALIDATE**: Test basic compliance check flow from PDF to Flagged metadata issue.

### Incremental Delivery

1. Add User Story 3 (Spatial/Halos) to enable soft clash detection.
2. Add User Story 4 (BCF/Reporting) to enable industry integration.
3. Polish and refine performance for large models.
