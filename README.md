# TODO Management API

A minimal FastAPI-based TODO management API for learning, prototyping, and GitHub publication.

## Overview

This repository implements a small REST API with SQLite persistence.

The app supports:
- creating a TODO item with `title`, `detail`, `created_by`, and `status`
- listing all TODO items
- updating a TODO status
- deleting a TODO item

The goal is to keep the implementation easy to understand, easy to test, and easy to publish.

> **No authentication.** This API has no authentication, user management, or
> access control of any kind — every endpoint is open to anyone who can reach
> it. It is intended for local learning and portfolio use only, and is not
> meant to be deployed as a public-facing production service.

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- pytest

## Repository Structure

```text
todo_api/
├── src/
│   └── todo_api/
│       ├── __init__.py
│       ├── app.py
│       ├── db.py
│       └── schemas.py
├── tests/
│   └── test_api.py
├── docs/
│   ├── REQUIREMENTS.md
│   ├── API_DESIGN.md
│   └── IMPLEMENTATION_PLAN.md
├── .github/
│   └── workflows/
│       └── python-test.yml
├── README.md
├── pyproject.toml
└── .gitignore
```

## Getting Started

### 1. Create a virtual environment

```bash
cd 06_Practice/todo_api
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -e .[dev]
```

### 3. Run the API locally

```bash
uvicorn todo_api.app:app --reload
```

If you want to run from the repository root without editable install, use:

```bash
PYTHONPATH=src uvicorn todo_api.app:app --reload
```

## API Endpoints

### Create a TODO

```bash
curl -X POST http://127.0.0.1:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "detail": "Review the routing and response model basics.",
    "created_by": "alice",
    "status": "未着手"
  }'
```

### List TODOs

```bash
curl http://127.0.0.1:8000/api/todos
```

Optional query parameters:

- `q` — search keyword matched against `title` and `detail` (substring match)
- `status` — filter by exact status (`未着手` / `進行中` / `完了` / `保留`)
- `sort` — one of `id`, `title`, `created_at`, `updated_at` (default: `created_at`)
- `order` — `asc` or `desc` (default: `desc`)
- `limit` — page size, 1–100 (default: `100`)
- `offset` — number of items to skip (default: `0`)

```bash
curl "http://127.0.0.1:8000/api/todos?q=FastAPI&status=進行中&sort=title&order=asc&limit=10&offset=0"
```

### Update a TODO status

```bash
curl -X PATCH http://127.0.0.1:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "進行中"}'
```

### Delete a TODO

```bash
curl -X DELETE http://127.0.0.1:8000/api/todos/1
```

## Database

The app uses SQLite and stores data in a local file named `todos.db` by default.

If you need to override the database path, set:

```bash
export TODO_DB_PATH=/path/to/your/todos.db
```

## Testing

```bash
pytest -q
```

## Notes

This project is intentionally small and focused on the fundamentals:
- clear API boundaries
- SQLite persistence
- small request/response models
- testable structure

It is suitable as a personal learning portfolio project and a starting point for future API work.

## Contributing

For contribution guidelines, development workflow, and CI expectations, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](./LICENSE).
