# domains/tasks/model.py
from datetime import date
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Date, Integer


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer())
    detail_article: Mapped[int] = mapped_column(Integer())
    detail_name: Mapped[str] = mapped_column(String(64))
    amount_needed: Mapped[int] = mapped_column(Integer())
    amount_done: Mapped[int] = mapped_column(Integer(), default=0)
    department: Mapped[str | None] = mapped_column(String(32), nullable=True)
    post: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    priority: Mapped[int] = mapped_column(Integer(), default=1)
    result: Mapped[bool] = mapped_column(Boolean(), default=False)
    available: Mapped[int] = mapped_column(Integer(), default=0)
    deadline: Mapped[date | None] = mapped_column(Date(), nullable=True)