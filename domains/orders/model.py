# domains/orders/model.py
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum
from enum import Enum as PyEnum


class OrderStatus(str, PyEnum):
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    good_article: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(Integer())
    amount_done: Mapped[int] = mapped_column(Integer(), default=0)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.in_progress)