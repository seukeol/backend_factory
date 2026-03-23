from pydantic import BaseModel


class PostBase(BaseModel):
    name: str
    department: str

class PostFilter(BaseModel):
    id: int | None = None
    name: str | None = None
    department: str | None = None


