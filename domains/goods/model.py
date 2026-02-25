from database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, SmallInteger

class Good(Base):
    __tablename__ = "goods"
    article: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    wb_article: Mapped[int] = mapped_column(SmallInteger())
    oz_article: Mapped[int] = mapped_column(SmallInteger())
    current_stock: Mapped[int] = mapped_column(SmallInteger())
