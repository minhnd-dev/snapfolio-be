from pydantic import BaseModel, field_validator
from fastapi import HTTPException
import string


class Token(BaseModel):
    access_token: str
    refresh: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_user_name(cls, username) -> 'UserBase':
        if len(username) < 2:
            raise HTTPException(400, "User name must be at least 2 characters long")
        if len(username) > 64:
            raise HTTPException(400, "User name must be shorter than 65 characters")
        for char in username:
            if char not in string.ascii_letters + string.digits:
                raise HTTPException(400, "User name cannot contains special characters")
        return username



class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password) -> 'UserCreate':
        if len(password) < 8:
            raise HTTPException(400, "Password must be at least 8 characters long")
        if len(password) > 64:
            raise HTTPException(400, "Password must be shorter than 65 characters")
        return password


class UserRead(UserCreate):
    pass


class User(UserBase):
    pass
