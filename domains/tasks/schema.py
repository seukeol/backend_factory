from datetime import date
from pydantic import BaseModel


class TaskCreate(BaseModel):
    order_id: int
    detail_article: int
    detail_name: str
    amount_needed: int
    department: str | None = None
    post: int | None = None
    priority: int | None = None
    deadline: date | None = None


class TaskEdit(BaseModel):
    id: int
    amount_needed: int | None = None
    amount_done: int | None = None
    department: str | None = None
    post: int | None = None
    priority: int | None = None
    result: bool | None = None
    available: int | None = None
    deadline: date | None = None


class TaskTopup(BaseModel):
    id: int
    amount_done: int


class TaskGetFilter(BaseModel):
    order_id: int | None = None
    detail_article: int | None = None
    detail_name: str | None = None
    department: str | None = None
    post: int | None = None
    priority: int | None = None
    result: bool | None = None
    deadline: date | None = None


class TaskPotentialOrder(BaseModel):
    good_article: int
    quantity: int