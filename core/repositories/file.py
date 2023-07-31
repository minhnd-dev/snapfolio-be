from sqlalchemy.orm import Session

from core.models.file import File
from core.schemas.file import FileCreate


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(self, file: FileCreate) -> File:
        db_file = File(
            name=file.name,
            path=file.path,
            content_type=file.content_type,
            user_id=file.user_id,
        )
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        return db_file
