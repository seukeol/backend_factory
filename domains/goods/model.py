from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Good(Base):
    __tablename__ = "goods"
    article: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    current_stock: Mapped[int] = mapped_column(Integer(), default=0)
    min_stock: Mapped[int] = mapped_column(Integer(), default=0)
    max_stock: Mapped[int] = mapped_column(Integer(), default=0)
    opt_stock: Mapped[int] = mapped_column(Integer(), default=0)
    marketplace_cons: Mapped[int] = mapped_column(Integer(), default=0)
    website_cons: Mapped[int] = mapped_column(Integer(), default=0)


class GoodComponent(Base):
    __tablename__ = "good_components"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    good_article: Mapped[int] = mapped_column(Integer())
    detail_article: Mapped[int] = mapped_column(Integer())
    quantity: Mapped[int] = mapped_column(Integer())
