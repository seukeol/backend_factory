from pydantic import BaseModel



class DetailGetFilter(BaseModel):
    article: int | None = None
    name: str | None = None
    post: int | None = None



class DetailCreate(BaseModel):
    name: str
    department: str | None = None
    post: int
    post_alt: int | None = None
    stock: int | None = None



class DetailEdit(BaseModel):
    article: int
    name: str | None = None
    department: str | None = None
    post: int | None = None
    post_alt: int | None = None
    stock: int | None = None
    availability: int | None = None


class DetailTopup(BaseModel):
    article: int
    amount: int


#component
class DetailComponentCreate(BaseModel):
    parent_article: int
    child_article: int
    quantity: int


class DetailComponentEdit(BaseModel):
    id: int
    quantity: int

class DetailComponentFilter(BaseModel):
    parent_article: int | None = None
    child_article: int | None = None
    quantity: int | None = None
