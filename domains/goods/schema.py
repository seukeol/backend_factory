from pydantic import BaseModel


class GoodBase(BaseModel):
    name: str
    wb_article: int | None = None
    oz_article: int | None = None
    current_stock: int

class GoodCreate(GoodBase):
    article: str

class GoodEdit(GoodBase):
    article: str
    name: str | None = None
    current_stock: int | None = None