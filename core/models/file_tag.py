from sqlalchemy import Table, ForeignKey, Column
from core.models.database import Base

file_tag = Table(
    "file_tag",
    Base.metadata,
    Column("file_id", ForeignKey("file.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True)
)