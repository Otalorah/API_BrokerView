from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    name:str
    lastname: str
    email: str


class UserToken(UserBase):
    user_sheet: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True