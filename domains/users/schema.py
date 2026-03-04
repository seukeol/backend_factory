from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str
    name: str
    department: str



class UserFilter(BaseModel):
    id: int | None = None
    login: str | None=None
    name: str | None=None
    department: str | None=None


class UserLogin(BaseModel):
    login: str


class UserCreate(UserBase):
    pass

class UserEdit(BaseModel):
    id: int
    name: str | None=None
    department: str | None=None
