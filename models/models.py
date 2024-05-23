from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    lastname: str
    email: str


class UserToken(UserBase):
    user_sheet: str


class UserCreate(UserBase):
    password: str


class EmailUser(BaseModel):
    email: str
