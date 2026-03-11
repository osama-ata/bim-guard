# BIMGuard AI

A professional compliance automation platform for IFC models, built as a full-stack Monorepo using Turborepo, Next.js 16, and FastAPI.

## Features

- **Automated Rule Extraction**: Ingest PDFs (Standards, Codes, BEPs) and extract machine-readable validation rules. _(TODO: Currently bypassed using a static `obc_part9.json` mock served via API)._
- **3D IFC Compliance Checking**: Validate IFC models against extracted rules using `@thatopen/components`.
- **IDE-Style Analysis**: A technical interface for deep-dive inspection of compliance issues.
- **Reporting**: Generate BCF reports for flagged issues.

## Tech Stack & Architecture

This repository is structured as a **Monorepo** using pnpm workspaces and Turborepo.

- **Frontend (`apps/web`)**: Next.js 16.1.6 (App Router), Tailwind CSS v4, Shadcn UI, `@thatopen/components` (Three.js BIM Core).
- **Backend (`apps/api`)**: Python FastAPI for heavy lifting and rule extraction processing.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system. If not, follow the installation steps below:

- **[Node.js](https://nodejs.org/en/download)**: v20 or higher
- **[Python](https://www.python.org/downloads/)**: 3.10 or higher
- **[pnpm](https://pnpm.io/installation)**: v9 or higher
- **[uv](https://docs.astral.sh/uv/)**: Python package manager

### Installation Guide

#### 1. Install System Dependencies (Node.js & Python)

**Windows (using winget):**

```powershell
winget install OpenJS.NodeJS
winget install Python.Python.3.11
```

**macOS (using Homebrew):**

```bash
brew install node
brew install python@3.11
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install nodejs npm python3 python3-venv python3-pip
```

#### 2. Install Package Managers (pnpm & uv)

Install `pnpm` (Node package manager) and `uv` (Python package manager):

```bash
# Install pnpm globally via npm
npm install -g pnpm

# Install uv globally (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install uv globally (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 3. Install Project Dependencies

1. **Install Node Dependencies** (From the root of the project):

   ```bash
   pnpm install
   ```

2. **Setup Python Environment** (For the backend API):

   ```bash
   cd apps/api
   uv sync

   # Activate virtual environment (if needed for direct script execution)
   .\.venv\Scripts\activate   # Windows
   # source .venv/bin/activate # Linux/Mac

   cd ../..
   ```

### Running the Application Structure

Thanks to Turborepo, you can run the entire stack (Frontend + Backend) simultaneously with a single command from the root folder:

```bash
pnpm dev
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
4. **Link workspaces**: run `pnpm install`
5. **Push**: `git push origin feature/my-feature`
6. **Create a Pull Request** back to the main repository.

For more detailed instructions, please read our [Contributing Guide](docs/guides/contributing.md).

## License

Private
