from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.database import Base
from core.models.file_tag import file_tag


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    path: Mapped[str]
    content_type: Mapped[str]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="files")
    tags: Mapped[list["Tag"]] = relationship(secondary=file_tag, back_populates="files")

    def __repr__(self):
        return f"<File(id={self.id}, name={self.name}, path={self.path}, user_id={self.user_id})>"
