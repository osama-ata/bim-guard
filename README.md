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

### 1. Frontend Setup (Next.js)

```bash
npm install
npm run dev
```

### 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
# Activate virtual environment
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload
```

_FastAPI API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs)._

### 3. Documentation (Zensical)

```bash
# From the backend virtual environment:
pip install zensical
cd ..
zensical serve -a localhost:8001
```

_Zensical documentation site will be available at [http://localhost:8001](http://localhost:8001)._

## Open [http://localhost:3000](http://localhost:3000) with your browser to see the Next.js application.

## Prerequisites

- **[Node.js](https://nodejs.org/en/download)**: v20 or higher
- **Package Manager**: [npm](https://www.npmjs.com/get-npm) (bundled with Node.js)

## Roadmap

For a detailed multi-phase development plan, see the [Development Roadmap](docs/roadmap.md).

### Converting to PDF

If you need to generate a PDF version of the roadmap, use the following command (requires Pandoc and LaTeX):

```bash
pandoc docs/roadmap.md -o docs/roadmap.pdf --pdf-engine=xelatex -V mainfont="Segoe UI Symbol"
```

### Currently Implemented

- [x] **Core Viewer**: High-performance IFC model loading and rendering
- [x] **Fragment Management**: Efficient model handling with import/export capabilities
- [x] **Camera Controls**: Basic navigation and auto-fit functionality
- [x] **Performance Monitoring**: Real-time FPS and memory usage stats
- [x] **UI/UX**: Modern, responsive interface with Dark/Light mode support

### Planned Features

- [ ] **Properties Panel**: Inspect element attributes and metadata
- [ ] **Measurement Tools**: Distance, angle, and area measurements
- [ ] **Sectioning**: Clipping planes and section box tools
- [ ] **BCF Support**: BIM Collaboration Format integration for issue tracking

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

## Contributing

We welcome contributions! The basic workflow includes:

1. **Fork** the repository: [https://github.com/osama-ata/bim-guard](https://github.com/osama-ata/bim-guard)
2. **Clone** and open in VS Code: `git clone <your-fork-url> && cd bim-guard && code .`
3. **Branch**: `git checkout -b feature/my-feature`
4. **Push**: `git push origin feature/my-feature`
5. **Create a Pull Request** back to the main repository.

For more detailed instructions, please read our [Contributing Guide](docs/guides/contributing.md).

## License

Private
