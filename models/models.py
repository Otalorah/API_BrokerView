from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    name:str
    lastname: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True