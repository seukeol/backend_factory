from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str
    name: str
    section_id: int
    group_name: str


class UserFilter(BaseModel):
    id: int | None = None
    login: str | None=None
    name: str | None=None
    section_id: int | None=None
    group_name: str | None=None

class UserLogin(BaseModel):
    login: str | None = None
    password: str | None = None

class UserCreate(UserBase):
    pass

class UserEdit(BaseModel):
    id: int
    name: str | None=None
    section_id: int | None=None
    group_name: str | None=None