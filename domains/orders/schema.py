from pydantic import BaseModel
from .model import OrderStatus


class OrderCreate(BaseModel):
    good_article: int
    quantity: int


class OrderEdit(BaseModel):
    id: int
    status: OrderStatus | None = None
    quantity: int | None = None


class OrderGetFilter(BaseModel):
    good_article: int | None = None
    status: OrderStatus | None = None

class OrderTopup(BaseModel):
    id: int
    amount_done: int