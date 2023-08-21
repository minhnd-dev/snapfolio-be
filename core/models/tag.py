from core.models.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    label: Mapped[str] = mapped_column(String(64))
    
    def __repr__(self):
        return f"<Tag(id={self.id}, label={self.label})>"
