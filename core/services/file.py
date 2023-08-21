from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import os

from core.models.file import File


class FileService:
    def __init__(self, db: Session):
        self.db = db 

    async def create_file(self, file: UploadFile, user_id: int):
        file_path = f"files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        db_file = File(
            name=file.filename,
            path=file_path,
            content_type=file.content_type,
            user_id=user_id,
        )
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

    def get_user_files(self, user_id: int) -> list[File]:
        return self.db.query(File).filter(File.user_id==user_id).all()

    def get_file_by_id(self, file_id: str) -> str:
        file = self.db.query(File).filter(File.id==file_id).first()
        if not file:
            return ""
        return file.path

    def delete_file_by_id(self, user_id: int, file_id: str):
        file_id_str = int(file_id)
        file = self.db.query(File).filter(and_(File.id==file_id_str, File.user_id==user_id)).first()
        if file:
            self.db.delete(file)
            if os.path.exists(f"files/{file.path}"):
                os.remove(f"files/{file.path}")
        self.db.commit()

    def delete_files_by_id(self, user_id: int, files: list[str]):
        for file_id in files:
            self.delete_file_by_id(user_id, file_id)
