from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.models.user import User
from core.repositories.user import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def create_user(self, username: str, password: str):
        password_hash = self.pwd_context.hash(password)
        return self.repository.create_user(username, password_hash)

    def get_user_by_username(self, username: str) -> User:
        return self.repository.get_user_by_username(username)