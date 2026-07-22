from pathlib import Path

from fastapi.testclient import TestClient


def test_create_and_list_todos(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test_todos.db"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    import todo_api.db as database
    from todo_api.app import app

    database.init_db()

    client = TestClient(app)

    response = client.post(
        "/api/todos",
        json={
            "title": "FastAPI を学ぶ",
            "detail": "FastAPI の基本を学ぶ",
            "created_by": "alice",
            "status": "進行中",
        },
    )
    assert response.status_code == 201

    payload = response.json()
    assert payload["title"] == "FastAPI を学ぶ"
    assert payload["detail"] == "FastAPI の基本を学ぶ"
    assert payload["created_by"] == "alice"
    assert payload["status"] == "進行中"
    assert payload["created_at"]
    assert payload["updated_at"]

    list_response = client.get("/api/todos")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["title"] == "FastAPI を学ぶ"
    assert items[0]["detail"] == "FastAPI の基本を学ぶ"
    assert items[0]["created_by"] == "alice"
    assert items[0]["status"] == "進行中"


def test_update_status_and_delete_todo(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test_todos.db"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    import todo_api.db as database
    from todo_api.app import app

    database.init_db()

    client = TestClient(app)
    create_response = client.post(
        "/api/todos",
        json={
            "title": "テスト用 TODO",
            "detail": "詳細を入力する",
            "created_by": "bob",
            "status": "未着手",
        },
    )
    todo_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/todos/{todo_id}",
        json={"status": "完了"},
    )
    assert update_response.status_code == 200
    update_payload = update_response.json()
    assert update_payload["status"] == "完了"
    assert update_payload["updated_at"]

    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/todos")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_invalid_status_is_rejected(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test_todos.db"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    import todo_api.db as database
    from todo_api.app import app

    database.init_db()

    client = TestClient(app)
    response = client.post(
        "/api/todos",
        json={
            "title": "壊れた入力",
            "detail": "無効なステータスを送る",
            "created_by": "carol",
            "status": "不正な値",
        },
    )

    assert response.status_code == 422
