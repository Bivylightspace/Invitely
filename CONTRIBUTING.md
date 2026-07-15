# Contributing to Invitely

Thanks for your interest in contributing! This project uses FastAPI, SQLAlchemy (sync + async), and Pydantic-style settings. The notes below make it quick to contribute code, tests, and docs.

- **Report issues first:** Open an issue describing the bug or feature with steps to reproduce and expected behavior.
- **Work on a branch:** Create a descriptive branch from `dev` (example: `feature/auth-google` or `fix/db-connection`).
- **Commit messages:** Use short, descriptive messages. Prefer Conventional Commits when possible (e.g., `feat: add health endpoint`).
- **Pull requests:** Open a PR against `dev`. Include summary, motivation, and testing steps. Link related issues.

Required steps for PRs:

1. Run tests locally: `pytest` (or the project's test command).
2. Format code: `black .` and `isort .`.
3. Run linters: `ruff .` or `flake8 .` (if configured).
4. Ensure type hints are present for public functions and models where applicable.

Code review focuses on readability, tests, and minimal risk changes. If you're unsure about an approach, open an issue or draft PR for feedback.

Contact/maintainers: Create an issue or add reviewers via the PR interface.
