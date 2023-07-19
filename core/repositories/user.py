from sqlalchemy.orm import Session

from core.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        result = self.db.query(User).filter(User.username == username).first()
        return result

    def create_user(self, username: str, password_hash: str):
        user = User(username=username, password=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user