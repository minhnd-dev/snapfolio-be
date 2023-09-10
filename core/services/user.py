from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.models.user import User


class UserExistedError(Exception):
    pass


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, username: str, password: str):
        if self.get_user_by_username(username):
            raise UserExistedError
        password_hash = self.pwd_context.hash(password)
        user = User(username=username, password=password_hash)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def change_password(self, user: User, new_password: str):
        password_hash = self.pwd_context.hash(new_password)
        user.password = password_hash
        self.db.commit()
