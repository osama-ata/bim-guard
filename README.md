# BIMGuard AI

A professional compliance automation platform for IFC models, built with Next.js 16, Tailwind v4, and Shadcn UI.

## Features

- **Automated Rule Extraction**: Ingest PDFs (Standards, Codes, BEPs) and extract machine-readable validation rules.
- **3D IFC Compliance Checking**: Validate IFC models against extracted rules using `@thatopen/components`.
- **IDE-Style Analysis**: A technical interface for deep-dive inspection of compliance issues.
- **Reporting**: Generate BCF reports for flagged issues.

## Tech Stack

- **Frontend Framework**: Next.js 16.1.6 (App Router)
- **Styling**: Tailwind CSS v4 + Shadcn UI
- **BIM Core**: `@thatopen/components` & `@thatopen/fragments` (v3.3)
- **Visualization**: Three.js
- **Icons**: Lucide React

## Getting Started

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Run the development server**:

   ```bash
   npm run dev
   ```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

---

## Development Conventions

This project follows **SOLID principles** for maintainability and testability.

### Architecture Overview

```
bim-guard/
├── app/                        # Next.js App Router
│   ├── analysis/               # Compliance Analysis Flows (Run & Results)
│   ├── library/                # Asset Management (Documents & Rules)
│   ├── projects/               # Project Management
│   ├── layout.tsx              # Root Layout (Sidebar + Header)
│   └── page.tsx                # Dashboard
├── components/
│   ├── compliance/             # Analysis & 3D Viewer Components
│   ├── dashboard/              # Dashboard Widgets
│   ├── layout/                 # Global UI (Sidebar, Header)
│   ├── rule-studio/            # Rule Extraction Components
│   ├── ui/                     # Shadcn Primitives
│   └── viewer/                 # Base Viewer Components
├── lib/                        # Utilities & Context
└── public/                     # Static Assets
```

## Core Workflows

1. **Insight Ingestion**: Upload a PDF -> Verify extracted rules in the **Rule Studio**.
2. **Compliance Check**: Select a project -> Upload IFC -> Apply Rules.
3. **Analysis Review**: Inspect results in the **Compliance Viewer** (3D + List).
4. **Reporting**: Export valid issues to BCF/Reporting formats.

## Development

This project follows **SOLID principles** and uses a modular component architecture.

- **Services** (e.g., `CameraService`) encapsulate business logic.
- **Components** are composed to build complex views (e.g., `ComplianceResultsPage`).

## License

Private
