# Python Test Guardrails Skill

## Purpose

Use this skill when adding, updating, or reviewing Python tests for the TODO API project.

## Rules

- Tests must validate real behavior, not placeholder expectations.
- Favor real API requests and observable response payloads.
- Keep fixtures minimal and representative.
- When behavior changes, update tests first when practical.

## Repository Context

- Test suite lives in `tests/`.
- Use `pytest -q` as the standard validation command.
- Keep the package import workflow aligned with the `src/` layout.

## Good Test Shapes

- Create a TODO and assert the persisted or returned representation.
- List TODOs and assert returned ordering or contents.
- Mark TODOs done and verify the state update.
- Delete a TODO and confirm it no longer appears.

## Failure Mode to Avoid

Do not add tests that only prove the test harness is working. Every assertion should prove meaningful API behavior.
