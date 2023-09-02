from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.models.database import get_db
from core.schemas.user import UserCreate, UserRead, User as UserSchema, Token
from core.services.auth import AuthService
from core.services.user import UserService, UserExistedError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


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
    return {
        "access_token": auth_service.create_access_token(user.username),
        "refresh": auth_service.create_refresh_token(user.username)
    }


@router.post("/token/refresh", response_model=Token)
def refresh_access_token(refresh: str, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh_token(refresh)


@router.post("/user")
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        user_service.create_user(user.username, user.password)
        return {"msg": "success"}
    except UserExistedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
