from enum import Enum

from pydantic import BaseModel, Field


class TodoStatus(str, Enum):
    NOT_STARTED = "未着手"
    IN_PROGRESS = "進行中"
    COMPLETED = "完了"
    PENDING = "保留"


class TodoCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    detail: str = Field(min_length=1, max_length=1000)
    created_by: str = Field(min_length=1, max_length=100)
    status: TodoStatus = TodoStatus.NOT_STARTED


class TodoUpdateRequest(BaseModel):
    status: TodoStatus


class TodoResponse(BaseModel):
    id: int
    title: str
    detail: str
    created_by: str
    status: TodoStatus
    created_at: str
    updated_at: str
