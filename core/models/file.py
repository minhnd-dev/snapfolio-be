from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.database import Base
from core.models.file_tag import file_tag


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    code: Mapped[str] = mapped_column(String(256))
    size: Mapped[int]
    path: Mapped[str] = mapped_column(String(256))
    content_type: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="files")
    tags: Mapped[list["Tag"]] = relationship(secondary=file_tag, back_populates="files")

    def __repr__(self):
        return f"<File(id={self.id}, name={self.name}, path={self.path}, user_id={self.user_id})>"
