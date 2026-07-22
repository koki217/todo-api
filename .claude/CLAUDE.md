# CLAUDE.md

This repository is a minimal FastAPI + SQLite TODO API intended for learning, prototyping, and GitHub publication.

## Project Goal

Keep the implementation small, easy to understand, and easy to validate.

## Repository Conventions

- Use the `src/` package layout.
- Keep application code under `src/todo_api/`.
- Keep tests under `tests/`.
- Keep documentation under `docs/`.
- Keep GitHub automation under `.github/`.

## Development Rules

- Prefer small, reviewable changes.
- Add or update tests when behavior changes.
- Keep route handlers, persistence logic, and schemas separated cleanly.
- Use Python naming conventions such as `snake_case`.
- Preserve the existing `pyproject.toml`-based development workflow.

## Validation Commands

Run these commands before finalizing changes:

```bash
pytest -q
```

For runtime verification:

```bash
uvicorn todo_api.app:app --reload
```

## CI Expectations

The CI workflow should validate that:

- the project installs via `python -m pip install -e ".[dev]"`
- tests pass with `python -m pytest -q`

## Preferred Change Style

When implementing changes:

1. Start from the smallest possible testable adjustment.
2. Update the related test when behavior changes.
3. Keep the implementation aligned with the repo structure.
4. Confirm the app still runs with the expected startup command.

## AI Customization Assets

This repository now includes repository-scoped agent and skill definitions under `.claude/agents/` and `.claude/skills/`.

- Use `api-architect` for FastAPI and API shape changes.
- Use `test-qa` for validating behavior changes and updating tests.
- Use `release-maintainer` for GitHub publication and repository hygiene work.
- Use the local skills for CRUD implementation, test guardrails, and publication-readiness guidance.
- Use the `issue-pr-workflow` skill when creating GitHub issues or opening pull requests, so branch names, issue bodies, and PR bodies follow this repo's templates and branch naming policy.

## Notes

This repo is intentionally minimal and should remain easy to understand for personal portfolio and learning purposes.
