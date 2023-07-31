from random import randint

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.repositories.file import FileRepository
from core.schemas.file import FileCreate


class FileService:
    def __init__(self, db: Session):
        self.repository = FileRepository(db)

    async def create_file(self, file: UploadFile):
        with open(file.filename, "wb") as f:
            f.write(await file.read())
        self.repository.create_file(FileCreate(
            name=file.filename,
            path=file.filename,
            content_type=file.content_type,
            user_id=1
        ))
