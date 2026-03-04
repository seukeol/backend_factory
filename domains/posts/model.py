from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, SmallInteger, Integer


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    department: Mapped[str] = mapped_column(String(32))