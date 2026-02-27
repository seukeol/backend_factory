from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(32))
    section_id: Mapped[int] = mapped_column(Integer())
    group_name: Mapped[str] = mapped_column(String(32))
