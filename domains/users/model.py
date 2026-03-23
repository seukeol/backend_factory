from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Null


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(32))
    department: Mapped[str] = mapped_column(String(32))
    admin_pass: Mapped[int] = mapped_column(Integer())
