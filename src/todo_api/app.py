from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from .db import create_todo, delete_todo, init_db, list_todos, update_todo_status
from .schemas import TodoCreateRequest, TodoResponse, TodoUpdateRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TODO API", version="1.0.0", lifespan=lifespan)


@app.post("/api/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo_endpoint(payload: TodoCreateRequest) -> TodoResponse:
    todo = create_todo(
        title=payload.title,
        detail=payload.detail,
        created_by=payload.created_by,
        status=payload.status.value,
    )
    return TodoResponse(**todo)


@app.get("/api/todos", response_model=list[TodoResponse])
def list_todos_endpoint() -> list[TodoResponse]:
    todos = list_todos()
    return [TodoResponse(**todo) for todo in todos]


@app.patch("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo_status_endpoint(todo_id: int, payload: TodoUpdateRequest) -> TodoResponse:
    todo = update_todo_status(todo_id=todo_id, status=payload.status.value)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")
    return TodoResponse(**todo)


@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_endpoint(todo_id: int) -> None:
    deleted = delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")
