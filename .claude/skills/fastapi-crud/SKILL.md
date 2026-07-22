# FastAPI CRUD Skill

## Purpose

Use this skill when working on the FastAPI TODO API routes, schema design, or SQLite persistence logic.

## Working Style

- Keep the API focused on a small number of clear routes.
- Treat the database layer as a narrow persistence boundary.
- Avoid overengineering with repository abstraction or dependency injection that is not needed.

## Project-Specific Guidance

- API package lives in `src/todo_api/`.
- Route entrypoint is `src/todo_api/app.py`.
- Persistence code is in `src/todo_api/db.py`.
- Request/response models are in `src/todo_api/schemas.py`.

## Preferred Approach

1. Define the shape of the request/response first.
2. Keep business logic in thin endpoint handlers.
3. Make persistence operations explicit and straightforward.
4. Validate the end-to-end flow with a test or a manual smoke check.

## Minimal Success Criteria

- The API remains small enough to understand in one pass.
- The CRUD flow is clear and consistent.
- The change can be explained in a GitHub-facing README.
