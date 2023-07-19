from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.database import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str]

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
