from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.models.database import get_db
from core.schemas.user import UserCreate, UserRead, User as UserSchema, Token
from core.models.user import User as UserModel
from core.services.auth import AuthService
from core.services.user import UserService

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/user", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    db_user = user_service.create_user(user.username, user.password)
    return db_user


@router.get("/user", response_model=UserRead)
async def get_user(username: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    result = user_service.get_user_by_username(username)
    return result
