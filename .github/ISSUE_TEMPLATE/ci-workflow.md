---
name: Scaffold CI workflow for formatting, linting and tests
about: Request to add GitHub Actions CI to run `black`, `isort`, linter, and tests on PRs
title: "Scaffold CI: black, isort, lint, tests on PRs"
labels: infrastructure, ci
assignees: ''
---

## Description

Add a GitHub Actions workflow that runs on pull requests to enforce code quality and prevent regressions. The workflow should run:

- `black --check .` (formatting)
- `isort --check-only .` (import ordering)
- `ruff check .` (or `flake8`) (linting)
- `pytest -q` (tests)

## Motivation and Context

Running these checks on PRs ensures consistent style, catches lint issues early, and prevents regressions in tests before merging.

## Acceptance Criteria

- A workflow file is added at `.github/workflows/ci.yml` that runs on `pull_request`.
- The workflow sets up Python, installs dependencies, and runs the commands above.
- The workflow exits non-zero on failures, causing PR checks to fail.

## How Has This Been Tested?

Provide steps to validate the workflow after it's merged (example):

1. Open a PR with intentionally misformatted code and verify the workflow fails on `black`.
2. Open a PR with lint errors and verify `ruff`/`flake8` fails.
3. Verify tests run and pass/fail appropriately.

## Files/Changes Suggested

- Add `.github/workflows/ci.yml` (see suggested config in repository PR)

## Types of changes

- [x] Infrastructure / CI

## Checklist

- [ ] Add workflow file to `.github/workflows/ci.yml`
- [ ] Update `requirements.txt` or install dev tools in workflow as needed
- [ ] Verify on a test PR
