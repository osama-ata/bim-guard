# Contributing to BIM Guard

We welcome contributions to both the Next.js frontend and the FastAPI backend! Here is the standard development workflow to get you started.

## Delivery Standards

Before implementation, contributors MUST describe behavior changes with clear user scenarios,
requirements, and success criteria in the relevant spec artifacts when the change is non-trivial.
Changes that modify API contracts, validation outputs, or shared types MUST update those contracts
and any related documentation in the same change. Every contribution MUST include verification
appropriate to the risk of the change, such as backend tests, frontend type or lint checks, or a
documented justification when automation is not practical.

## Git Workflow

Follow these steps to contribute code to the repository.

### 1. Fork the Repository

1. Navigate to the original repository at [https://github.com/osama-ata/bim-guard](https://github.com/osama-ata/bim-guard).
2. Click the **Fork** button in the top right corner.
3. Select your personal account as the destination for the fork.

### 2. Clone and Open in VS Code

Once you have forked the repository, clone it locally and open it using Visual Studio Code:

```bash
# Clone your fork (replace YOUR_USERNAME with your GitHub username)
git clone https://github.com/YOUR_USERNAME/bim-guard.git

# Navigate into the project directory
cd bim-guard

# Open in VS Code
code .
```

### 3. Create a Feature Branch

Always create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or for a bug fix:
git checkout -b fix/your-bug-fix
```

### 4. Pull Latest Changes

Before starting new work or pushing your changes, it is good practice to ensure your branch is up to date with the original repository (the `upstream`):

```bash
# Add the original repository as 'upstream' (only need to do this once)
git remote add upstream https://github.com/osama-ata/bim-guard.git

# Fetch the latest changes
git fetch upstream

# Rebase or merge the latest main into your branch
git merge upstream/main
```

### 5. Push Your Changes

After writing and committing your code in VS Code, push your branch to your forked repository on GitHub:

```bash
# Push the branch to your fork
git push origin feature/your-feature-name
```

### 5a. Validate Before Opening a PR

Run the checks relevant to the paths you changed before you open the pull request.

```bash
# Install workspace dependencies once from the repository root
pnpm install

# Sync the backend environment when API code changes
cd apps/api
uv sync
cd ../..

# Run the monorepo development stack when you need integrated verification
pnpm dev
```

### 6. Open a Pull Request (PR)

1. Go to your forked repository on GitHub: `https://github.com/YOUR_USERNAME/bim-guard`.
2. You will see a banner indicating you recently pushed a branch. Click **Compare & pull request**.
3. Ensure the base repository is `osama-ata/bim-guard` and the base branch is `main`.
4. Add a clear title and description outlining the changed behavior, verification performed, and any
	documentation updates.
5. Click **Create pull request**.

Thank you for contributing!
