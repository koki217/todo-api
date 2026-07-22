import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "todos.db"


def get_db_path() -> Path:
    return Path(os.getenv("TODO_DB_PATH", str(DEFAULT_DB_PATH)))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def _ensure_columns(connection: sqlite3.Connection) -> None:
    table_info = connection.execute("PRAGMA table_info(todos)").fetchall()
    columns = {row[1] for row in table_info}

    if "detail" not in columns:
        connection.execute("ALTER TABLE todos ADD COLUMN detail TEXT NOT NULL DEFAULT ''")
    if "created_by" not in columns:
        connection.execute("ALTER TABLE todos ADD COLUMN created_by TEXT NOT NULL DEFAULT ''")
    if "status" not in columns:
        connection.execute("ALTER TABLE todos ADD COLUMN status TEXT NOT NULL DEFAULT '未着手'")
    if "updated_at" not in columns:
        connection.execute("ALTER TABLE todos ADD COLUMN updated_at TEXT NOT NULL DEFAULT ''")


def init_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                detail TEXT NOT NULL DEFAULT '',
                created_by TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT '未着手',
                updated_at TEXT NOT NULL DEFAULT ''
            )
            """
        )
        _ensure_columns(connection)
        connection.commit()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_todo(title: str, detail: str, created_by: str, status: str) -> dict[str, Any]:
    created_at = _now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO todos (title, detail, created_by, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, detail, created_by, status, created_at, created_at),
        )
        connection.commit()
        todo_id = cursor.lastrowid

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, detail, created_by, status, created_at, updated_at
            FROM todos WHERE id = ?
            """,
            (todo_id,),
        ).fetchone()

    return dict(row)


_SORTABLE_COLUMNS = {"id", "title", "created_at", "updated_at"}


def list_todos(
    q: str | None = None,
    status: str | None = None,
    sort: str = "created_at",
    order: str = "desc",
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    if sort not in _SORTABLE_COLUMNS:
        sort = "created_at"
    direction = "ASC" if order == "asc" else "DESC"

    conditions: list[str] = []
    params: list[Any] = []

    if q:
        conditions.append("(title LIKE ? OR detail LIKE ?)")
        like_pattern = f"%{q}%"
        params.extend([like_pattern, like_pattern])

    if status:
        conditions.append("status = ?")
        params.append(status)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    params.extend([limit, offset])

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT id, title, detail, created_by, status, created_at, updated_at
            FROM todos
            {where_clause}
            ORDER BY {sort} {direction}, id DESC
            LIMIT ? OFFSET ?
            """,
            params,
        ).fetchall()
    return [dict(row) for row in rows]


def update_todo_status(todo_id: int, status: str) -> dict[str, Any] | None:
    updated_at = _now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE todos SET status = ?, updated_at = ? WHERE id = ?",
            (status, updated_at, todo_id),
        )
        connection.commit()
        if cursor.rowcount == 0:
            return None

        row = connection.execute(
            """
            SELECT id, title, detail, created_by, status, created_at, updated_at
            FROM todos WHERE id = ?
            """,
            (todo_id,),
        ).fetchone()

    return dict(row) if row is not None else None


def delete_todo(todo_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        connection.commit()
        return cursor.rowcount > 0
