# BIMGuard AI

A professional compliance automation platform for IFC models, built as a full-stack Monorepo using Turborepo, Next.js 16, and FastAPI.

## Features

- **Automated Rule Extraction**: Ingest PDFs (Standards, Codes, BEPs) and extract machine-readable validation rules.
- **3D IFC Compliance Checking**: Validate IFC models against extracted rules using `@thatopen/components`.
- **IDE-Style Analysis**: A technical interface for deep-dive inspection of compliance issues.
- **Reporting**: Generate BCF reports for flagged issues.

## Tech Stack & Architecture

This repository is structured as a **Monorepo** using npm workspaces and Turborepo.

- **Frontend (`apps/web`)**: Next.js 16.1.6 (App Router), Tailwind CSS v4, Shadcn UI, `@thatopen/components` (Three.js BIM Core).
- **Backend (`apps/api`)**: Python FastAPI for heavy lifting and rule extraction processing.

## Getting Started

### Prerequisites

- **[Node.js](https://nodejs.org/en/download)**: v20 or higher
- **[Python](https://www.python.org/downloads/)**: 3.10 or higher

### Installation

1. **Install Node Dependencies** (From the root of the project):

   ```bash
   npm install
   ```

2. **Setup Python Environment** (For the backend API):

   ```bash
   cd apps/api
   python -m venv venv

   # Activate virtual environment
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate # Linux/Mac

   pip install -r requirements.txt
   cd ../..
   ```

### Running the Application Structure

Thanks to Turborepo, you can run the entire stack (Frontend + Backend) simultaneously with a single command from the root folder:

```bash
npm run dev
```

- **Next.js Web App** will be available at [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend Docs** will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

## Documentation

For a detailed multi-phase development plan, see the [Development Roadmap](docs/roadmap.md).

To run the Zensical documentation:

```bash
# Ensure you are in the python environment where zensical is installed, or install it globally
pip install zensical
zensical serve -a localhost:8001
```

## Repository Structure

```text
bim-guard/
├── apps/
│   ├── api/                   # FastAPI Backend
│   │   ├── app/               # API Routes and Services
│   │   └── main.py            # FastAPI Entrypoint
│   └── web/                   # Next.js Frontend
│       ├── app/               # App Router Pages
│       ├── components/        # React & Radix Components
│       ├── lib/               # Utilities & Context
│       └── public/            # Static Assets
├── docs/                      # General markdown documentation
├── turbo.json                 # Turborepo orchestration config
└── package.json               # Root workspace definitions
```

## Core Workflows

1. **Insight Ingestion**: Upload a PDF -> Verify extracted rules in the **Rule Studio**.
2. **Compliance Check**: Select a project -> Upload IFC -> Apply Rules.
3. **Analysis Review**: Inspect results in the **Compliance Viewer** (3D + List).
4. **Reporting**: Export valid issues to BCF/Reporting formats.

## Contributing

We welcome contributions! The basic workflow includes:

1. **Fork** the repository: [https://github.com/osama-ata/bim-guard](https://github.com/osama-ata/bim-guard)
2. **Clone** and open in VS Code: `git clone <your-fork-url> && cd bim-guard && code .`
3. **Branch**: `git checkout -b feature/my-feature`
4. **Link workspaces**: run `npm install`
5. **Push**: `git push origin feature/my-feature`
6. **Create a Pull Request** back to the main repository.

For more detailed instructions, please read our [Contributing Guide](docs/guides/contributing.md).

## License

Private
