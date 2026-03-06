# BIM Guard - AI Agent Instructions

## Project Overview

BIM Guard is a full-stack web application designed for analyzing and validating Building Information Models (BIM) using IFC files.

## Repository Structure (Turborepo Monorepo)

- `apps/web/`: Frontend application (Next.js, React, TypeScript, Tailwind CSS, `web-ifc`).
- `apps/api/`: Backend service (Python, FastAPI, `ifcopenshell` for parsing and rule validation).
- `docs/`: Project documentation (MkDocs).

## Tech Stack & Conventions

### Frontend (`apps/web/`)

- **Framework:** Next.js (App Router), React, TypeScript.
- **Styling:** Tailwind CSS, `shadcn/ui` (Radix UI primitives).
- **State Management:** Zustand (`useBIMStore.ts`).
- **Data Fetching:** TanStack React Query.
- **3D Viewer:** `@thatopen/components` for IFC parsing and visualization in the browser.
- **Conventions:**
  - Use functional components and modern React hooks.
  - Server Components by default; add `"use client"` only when necessary (e.g., for 3D viewer, interactivity, or state).
  - Place generic UI components in `apps/web/components/ui/`.
  - Follow Feature-Sliced Design (FSD): Place domain-specific logic and components in `apps/web/features/` (e.g., `features/viewer`, `features/compliance`, `features/rule-studio`).

### Backend (`apps/api/`)

- **Framework:** Python, FastAPI.
- **BIM Processing:** `ifcopenshell` (Python).
- **Conventions:**
  - Strictly use Python type hints (`def process_ifc(file: UploadFile) -> dict:`).
  - Keep route handlers (in `endpoints/`) thin and delegate logic to `services/` (e.g., `services/ifc_parser.py`).
  - Follow PEP 8 standards.

### General Rules for the AI Agent

1. **Context First:** Always check whether a requested change affects the `apps/web` or `apps/api` environment and apply the correct language rules.
2. **Imports:** Use absolute paths for Next.js imports where configured.
3. **Dependencies:** Do not introduce new third-party packages unless absolutely necessary.
4. **Documentation:** When creating new backend endpoints, ensure they are well-documented for FastAPI's Swagger UI.
5. **IFC Handling:** Remember that large IFC files are resource-heavy. Prefer streaming, background workers, or WebAssembly (WASM on the frontend) where applicable.

## Common Commands

- **Start Development Servers (Frontend & Backend):** `npx turbo run dev` (run from the monorepo root)
- **Build all apps:** `npx turbo run build`
- **Type Checking (Frontend):** `npm run type-check -w web`
