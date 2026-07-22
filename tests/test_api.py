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


def test_search_sort_and_pagination(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test_todos.db"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    import todo_api.db as database
    from todo_api.app import app

    database.init_db()

    client = TestClient(app)
    todos = [
        {
            "title": "FastAPI を学ぶ",
            "detail": "ルーティングを復習する",
            "created_by": "alice",
            "status": "進行中",
        },
        {
            "title": "買い物リスト",
            "detail": "牛乳を買う",
            "created_by": "bob",
            "status": "未着手",
        },
        {
            "title": "FastAPI のテストを書く",
            "detail": "pytest を使う",
            "created_by": "carol",
            "status": "完了",
        },
    ]
    for todo in todos:
        response = client.post("/api/todos", json=todo)
        assert response.status_code == 201

    search_response = client.get("/api/todos", params={"q": "FastAPI"})
    assert search_response.status_code == 200
    search_items = search_response.json()
    assert len(search_items) == 2
    assert all("FastAPI" in item["title"] for item in search_items)

    status_response = client.get("/api/todos", params={"status": "完了"})
    assert status_response.status_code == 200
    status_items = status_response.json()
    assert len(status_items) == 1
    assert status_items[0]["title"] == "FastAPI のテストを書く"

    sort_response = client.get("/api/todos", params={"sort": "title", "order": "asc"})
    assert sort_response.status_code == 200
    sorted_titles = [item["title"] for item in sort_response.json()]
    assert sorted_titles == sorted(sorted_titles)

    page_response = client.get("/api/todos", params={"limit": 2, "offset": 1})
    assert page_response.status_code == 200
    assert len(page_response.json()) == 2

    invalid_sort_response = client.get("/api/todos", params={"sort": "not_a_column"})
    assert invalid_sort_response.status_code == 422

    invalid_limit_response = client.get("/api/todos", params={"limit": 0})
    assert invalid_limit_response.status_code == 422


def test_error_response_format_is_consistent(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test_todos.db"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    import todo_api.db as database
    from todo_api.app import app

    database.init_db()

    client = TestClient(app)

    not_found_response = client.delete("/api/todos/9999")
    assert not_found_response.status_code == 404
    not_found_body = not_found_response.json()
    assert isinstance(not_found_body["detail"], str)
    assert not_found_body["errors"] is None

    validation_response = client.post(
        "/api/todos",
        json={
            "title": "不正な入力",
            "detail": "無効なステータスを送る",
            "created_by": "dave",
            "status": "不正な値",
        },
    )
    assert validation_response.status_code == 422
    validation_body = validation_response.json()
    assert isinstance(validation_body["detail"], str)
    assert isinstance(validation_body["errors"], list)
    assert len(validation_body["errors"]) >= 1
    assert {"field", "message"} <= validation_body["errors"][0].keys()


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
