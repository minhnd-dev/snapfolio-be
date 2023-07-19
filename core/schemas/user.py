from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserCreate):
    class Config:
        orm_mode = True


class User(UserBase):
    class Config:
        orm_mode = True
