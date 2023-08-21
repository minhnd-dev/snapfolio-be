from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from core.models import user as user_model


SECRET_KEY = "jwt secret key"
REFRESH_SECRET_KEY = "jwt refresh secret key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(user_model.User).filter(user_model.User.username == username).first()
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(username: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
        expire = datetime.utcnow() + expires_delta
        data = {
            "sub": username,
            "exp": expire
        }
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(username: str, expires_delta: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)) -> str:
        data = {
            "sub": username,
            "exp": datetime.utcnow() + expires_delta
        }
        refresh_token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
        return refresh_token

    def refresh_token(self, refresh_token: str) -> dict[str, str]:
        current_user = self.get_current_user(refresh_token, refresh=True)

        return {
            "token": self.create_access_token(current_user.username),
            "refresh": self.create_refresh_token(current_user.username)
        }

    def get_current_user(self, token: str, refresh=False) -> user_model.User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        secret = SECRET_KEY if not refresh else REFRESH_SECRET_KEY
        try:
            payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.db.query(user_model.User).filter(user_model.User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
