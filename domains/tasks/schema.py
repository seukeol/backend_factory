from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    good_article: str
    amount_needed: int
    department: str
    post: str
    deadline: datetime

class TaskTopup(BaseModel):
    id: int
    amount_done: int
    amount_needed: int

class TaskFilter(BaseModel):
    id: int | None = None
    good_article: str | None=None
    department: str | None=None
    post: str | None=None
    result: str | None=None
    deadline: datetime | None=None

class TaskCreate(TaskBase):
    pass

class TaskEdit(BaseModel):
    id: int
    good_article: str | None=None
    amount_needed: int | None=None
    amount_done: int | None=None
    department: str | None=None
    post: str | None=None
    result: str | None=None
    deadline: datetime | None=None