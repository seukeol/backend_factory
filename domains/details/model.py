from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer



class Detail(Base):
    __tablename__ = "details"
    article: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    stock: Mapped[int] = mapped_column(Integer(), default=0)
    availability: Mapped[int] = mapped_column(Integer(), default=0)
    department: Mapped[str] = mapped_column(String())
    post: Mapped[int] = mapped_column(Integer())
    post_alt: Mapped[int] = mapped_column(Integer(), nullable=True)


class DetailComponent(Base):
    __tablename__ = "detail_components"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    parent_article: Mapped[int] = mapped_column(Integer())
    child_article: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(Integer())