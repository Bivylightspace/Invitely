# Code Style — Invitely

This document summarizes the preferred coding style for the project.

Formatting

- Use `black` for formatting: `black .`
- Use `isort` for import ordering: `isort .`

Linting & type checking

- Prefer `ruff` or `flake8` for linting.
- Add/maintain type hints. Use `mypy` where desired for stricter checking.

Python idioms

- Use f-strings for formatting.
- Avoid wildcard imports.
- Keep functions small and single-responsibility.

Project-specific conventions

- SQLAlchemy models: prefer `Mapped[...]` annotations and `mapped_column` for columns.
- Relationships: declare `relationship(..., back_populates=...)` and set `cascade` where appropriate.
- Async vs Sync DB: the project contains both sync (`create_engine`) and async (`create_async_engine`) engines — use the async session dependency (`get_async_db`) for async routes.
- Config: centralize environment-driven settings in `api/utils/config.py`.

Docstrings & tests

- Use concise docstrings on public modules and functions.
- Add unit tests for new behavior; run tests with `pytest`.

Pre-commit

- If using pre-commit, include hooks for `black`, `isort`, `ruff`, and `pytest` (optional).

When in doubt, open an issue or PR asking for style guidance.
