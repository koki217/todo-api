# Contributing

Thank you for contributing to this project.

This repository is a small FastAPI + SQLite TODO API intended as a personal learning and portfolio project. The development workflow is designed to be simple, testable, and compatible with AI-assisted development using Claude Code.

## Development Philosophy

- Keep changes small and easy to review.
- Prefer clear, readable Python code over clever abstractions.
- Add or update tests when behavior changes.
- Document non-obvious decisions in the repository docs.
- Treat CI as the source of truth for validation.

## Development Setup

```bash
cd 06_Practice/todo_api
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Local Development Workflow

### Run the API

```bash
uvicorn todo_api.app:app --reload
```

If you are running from outside the package root, use:

```bash
PYTHONPATH=src uvicorn todo_api.app:app --reload
```

### Run tests

```bash
pytest -q
```

## Claude Code Workflow

This project is intended to be developed in a Claude Code-friendly way.

Recommended working style:

1. Start with a narrow, testable change.
2. Write or update a test first when behavior changes.
3. Make the minimum implementation change needed.
4. Run the relevant tests locally.
5. Confirm that the change is compatible with the repository structure and CI workflow.

When using Claude Code for implementation, keep the following in mind:

- Prefer a single responsibility per function.
- Preserve the `src/` package layout.
- Keep `README.md`, `docs/`, and code aligned.
- Avoid introducing hidden environment-dependent behavior.

## Pull Request Expectations

Before opening a pull request:

- Run `pytest -q` successfully.
- Confirm the API still starts locally.
- Keep the change scoped to the problem being solved.
- Avoid unrelated formatting or refactoring in the same change.

A good PR should include:

- a short summary of the change
- the reason for the change
- the validation performed

## CI / CD Expectations

This repository uses GitHub Actions for automated verification.

The CI workflow should validate:

- project installation via `python -m pip install -e ".[dev]"`
- test execution via `python -m pytest -q`

The expected standard is:

- all tests pass
- no new regression is introduced
- the app remains runnable from the repository configuration

## Coding Conventions

- Use Python naming conventions such as `snake_case` for functions and variables.
- Keep route handlers, persistence logic, and schema definitions separated cleanly.
- Favor small modules with clear purpose.
- Use type hints where practical.

## Commit Guidance

Use concise, descriptive commit messages.

Examples:

- `TODO API の CRUD ルートを整理`
- `pytest で src レイアウトを検証できるように修正`
- `CI ワークフローを pyproject ベースに更新`

## Questions

If you are unsure about the expected repository shape, validation flow, or the right way to scope a change, open an issue or start with the smallest possible implementation and verify it locally before submitting a PR.
