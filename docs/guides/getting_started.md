# Getting Started

## 1. Install Workspace Dependencies

```bash
pnpm install
```

## 2. Sync the Backend Environment

```bash
cd apps/api
uv sync

# Optional: activate the environment for direct backend commands
# Windows
.\.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

cd ../..
```

## 3. Run the Monorepo

```bash
pnpm dev
```

This starts the Next.js app and the FastAPI service using the repository's configured monorepo
workflow.
