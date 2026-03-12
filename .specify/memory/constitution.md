<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template placeholder -> I. Monorepo Boundary Integrity
- Template placeholder -> II. Contract-Driven Compliance Delivery
- Template placeholder -> III. Mandatory Verification Gates
- Template placeholder -> IV. Resource-Aware BIM Processing
- Template placeholder -> V. Dependency and Documentation Discipline
Added sections:
- Engineering Constraints
- Delivery Workflow
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ docs/guides/contributing.md
- ✅ docs/guides/getting_started.md
- ✅ README.md (reviewed, no change required)
- ✅ specs/003-unified-compliance-engine/quickstart.md (reviewed, no change required)
- ✅ .specify/templates/commands/ (directory absent, no update required)
Follow-up TODOs:
- None
-->
# BIM Guard Constitution

## Core Principles

### I. Monorepo Boundary Integrity
All work MUST preserve the monorepo's explicit boundaries: Next.js frontend code belongs in
`apps/web`, FastAPI backend code belongs in `apps/api`, and durable product or process
documentation belongs in `docs` or `specs`. Frontend changes MUST follow the existing
feature-sliced structure, keep generic UI in shared component locations, and avoid adding
`"use client"` unless browser-only behavior requires it. Backend route handlers MUST stay thin
and delegate domain logic to services or modules with explicit type hints.

Rationale: BIM Guard is intentionally split between browser visualization, API processing, and
project documentation. Respecting those seams keeps changes reviewable and prevents hidden
coupling between the apps.

### II. Contract-Driven Compliance Delivery
Every feature that changes user-visible behavior, API responses, validation logic, or exchanged
data MUST be specified before implementation with independently testable user scenarios,
functional requirements, and measurable success criteria. Changes that add or alter API surfaces,
rule payloads, or shared data contracts MUST document the contract in the relevant spec artifacts
and keep FastAPI documentation accurate.

Rationale: BIM Guard spans UI workflows, compliance rules, and backend services. Explicit
contracts keep those layers aligned and make changes safe to implement incrementally.

### III. Mandatory Verification Gates
Each change MUST include verification proportional to the risk of the behavior being modified.
Backend logic changes MUST add or update automated tests in `apps/api/tests` when practical.
Frontend changes MUST pass the relevant type-checking, linting, and targeted interaction tests
where those checks exist. Bug fixes that address regressions MUST include a regression test or a
documented reason why one is not practical. No work is complete until the changed paths have a
recorded verification step.

Rationale: The platform combines heavy BIM workflows with user-facing analysis views. Requiring
explicit verification is the lowest-cost control against silent breakage.

### IV. Resource-Aware BIM Processing
IFC, PDF, and other model-processing workflows MUST be designed for large-file behavior. Browser
code SHOULD prefer WebAssembly or client-side parsing only when it avoids unnecessary server load,
and backend code MUST use streaming, batching, or background execution for long-running or
resource-heavy operations where applicable. New features MUST document material performance or
memory assumptions whenever they process model geometry, extracted rules, or file uploads.

Rationale: BIM Guard operates on large BIM artifacts that can exhaust browser or server resources
quickly. Performance discipline is a product requirement, not an optimization pass.

### V. Dependency and Documentation Discipline
New third-party packages MUST not be introduced without a concrete justification tied to delivery,
maintenance, or performance. All changes that affect setup, contributor workflow, runtime
operations, or public behavior MUST update the corresponding documentation in the repository in the
same change. Commands and examples MUST reflect the actual monorepo layout and supported tooling.

Rationale: This repository mixes Node and Python toolchains. Unjustified dependencies and stale
docs are both operational risks that slow delivery and onboarding.

## Engineering Constraints

- Frontend work MUST preserve the established stack: Next.js App Router, TypeScript, Tailwind,
  shadcn/ui, Zustand, TanStack Query, and `@thatopen/components` unless an amendment approves a
  change.
- Backend work MUST preserve the established stack: FastAPI, Python type hints, service-oriented
  business logic, and documented request/response models.
- Shared interfaces between frontend and backend MUST remain explicit. Ad hoc payload changes that
  bypass types, specs, or OpenAPI documentation are not allowed.
- Security, privacy, and file-handling decisions MUST favor least privilege and predictable failure
  modes, especially for uploaded IFC and document assets.

## Delivery Workflow

1. Define or update the feature specification with prioritized user scenarios, edge cases,
	requirements, and success criteria.
2. Produce or update the implementation plan, including a Constitution Check that names the
	affected apps, contracts, validation approach, and performance considerations.
3. Break implementation into independently valuable tasks grouped by user story, with verification
	tasks included when behavior changes.
4. Implement within the correct app boundaries, update docs alongside code, and verify the changed
	behavior before review.
5. During review, confirm compliance with all five core principles and either resolve violations or
	document an approved amendment.

## Governance

This constitution supersedes conflicting local workflow preferences for this repository. Amendments
MUST be made by updating this document together with any affected templates, guidance, or runtime
docs in the same change. Compliance reviews for plans, tasks, pull requests, and release-critical
changes MUST explicitly evaluate monorepo boundaries, contract accuracy, verification coverage,
resource handling, and documentation updates.

Versioning policy follows semantic versioning for governance changes. MAJOR versions apply to
breaking principle removals or redefinitions. MINOR versions apply to new principles or materially
expanded sections. PATCH versions apply to clarifications that do not change the required behavior.

When a requirement in this constitution cannot be met, the exception MUST be documented in the
relevant plan or review artifact with the reason, scope, mitigation, and owner before work is
approved.

**Version**: 1.0.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12
