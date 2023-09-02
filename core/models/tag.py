from core.models.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from core.models.file_tag import file_tag


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    label: Mapped[str] = mapped_column(String(64))
    user: Mapped[list["User"]] = relationship("User", back_populates="tags")
    files: Mapped[list["File"]] = relationship(secondary=file_tag, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, label={self.label})>"
