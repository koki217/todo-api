from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .db import create_todo, delete_todo, init_db, list_todos, update_todo_status
from .schemas import TodoCreateRequest, TodoResponse, TodoStatus, TodoUpdateRequest

SortField = Literal["id", "title", "created_at", "updated_at"]
SortOrder = Literal["asc", "desc"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TODO API", version="1.0.0", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"] if part != "body"),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "リクエストの内容が不正です", "errors": errors},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "errors": None},
    )


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
def list_todos_endpoint(
    q: str | None = Query(default=None, min_length=1, max_length=255),
    status_filter: TodoStatus | None = Query(default=None, alias="status"),
    sort: SortField = Query(default="created_at"),
    order: SortOrder = Query(default="desc"),
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[TodoResponse]:
    todos = list_todos(
        q=q,
        status=status_filter.value if status_filter else None,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )
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
