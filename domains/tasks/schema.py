from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    good_article: str
    amount_needed: int
    amount_done: int
    section_id: int
    group_name: str
    deadline: datetime

class TaskTopup(BaseModel):
    id: int
    amount_done: int
    amount_needed: int

class TaskFilter(BaseModel):
    id: int | None = None
    good_article: str | None=None
    section_id: int | None=None
    group_name: str | None=None
    result: str | None=None
    deadline: datetime | None=None

class TaskCreate(TaskBase):
    pass

class TaskEdit(BaseModel):
    id: int
    good_article: str | None=None
    amount_needed: int | None=None
    amount_done: int | None=None
    section_id: int | None=None
    group_name: str | None=None
    result: str | None=None
    deadline: datetime | None=None