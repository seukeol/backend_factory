from pydantic import BaseModel


class GoodGetFilter(BaseModel):
    article: int | None = None
    name: str | None = None
    current_stock: int | None = None


class GoodCreate(BaseModel):
    name: str
    current_stock: int | None = None
    min_stock: int | None = None
    max_stock: int | None = None
    opt_stock: int | None = None
    marketplace_cons: int | None = None
    website_cons: int | None = None


class GoodEdit(BaseModel):
    article: int
    name: str | None = None
    current_stock: int | None = None
    min_stock: int | None = None
    max_stock: int | None = None
    opt_stock: int | None = None
    marketplace_cons: int | None = None
    website_cons: int | None = None


class GoodTopup(BaseModel):
    article: int
    amount: int

#component
class GoodComponentCreate(BaseModel):
    good_article: int
    detail_article: int
    quantity: int
    color: str | None = None


class GoodComponentEdit(BaseModel):
    id: int
    quantity: int | None = None
    color: str | None = None