from datetime import datetime
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, SmallInteger, Boolean, Date

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(SmallInteger(), primary_key=True, autoincrement=True)
    good_article: Mapped[str] = mapped_column(String(32)) #foreign key
    amount_needed: Mapped[int] = mapped_column(SmallInteger())
    amount_done: Mapped[int] = mapped_column(SmallInteger())
    section_id: Mapped[int] = mapped_column(SmallInteger())
    group_name: Mapped[str] = mapped_column(String(32))
    result: Mapped[bool] = mapped_column(Boolean())
    deadline: Mapped[datetime] = mapped_column(Date())