from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import os

from core.models.file import File
from core.models.tag import Tag
from core.models.user import User

from core.services.tag import TagService


class FileNotFound(Exception):
    pass


class FileService:
    def __init__(self, db: Session):
        self.db = db

    async def create_file(self, file: UploadFile, user: User):
        file_path = f"files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        db_file = File(
            name=file.filename,
            path=file_path,
            content_type=file.content_type,
            user=user,
        )
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

    def get_user_files(self, user_id: int) -> list[File]:
        return list(self.db.scalars(select(File).filter(File.user_id == user_id)).all())

    def get_user_files_by_tag(self, user_id, tag_id):
        return list(
            self.db.scalars(
                select(File)
                .join(File.tags.and_(Tag.id == tag_id))
                .filter(and_(File.user_id == user_id))
            )
        )

    def get_file_by_id(self, file_id: int, user_id: int | None = None) -> File | None:
        return (
            self.db.query(File)
            .filter(and_(File.id == file_id, File.user_id == user_id))
            .first()
        )

    def delete_file_by_id(self, user_id: int, file_id: int):
        file = (
            self.db.query(File)
            .filter(and_(File.id == file_id, File.user_id == user_id))
            .first()
        )
        if file:
            self.db.delete(file)
            if os.path.exists(f"files/{file.path}"):
                os.remove(f"files/{file.path}")
        self.db.commit()

    def delete_files_by_id(self, user_id: int, files: list[int]):
        for file_id in files:
            self.delete_file_by_id(user_id, file_id)

    def add_tags(self, user_id: int, file_id: int, tag_labels: list[str]):
        file = self.get_file_by_id(file_id, user_id)

        if not file:
            raise FileNotFound

        tag_service = TagService(self.db)

        tags = []
        new_tag_labels = []
        for tag_label in tag_labels:
            tag = tag_service.get_tag_by_label(user_id, tag_label)
            if tag in file.tags:
                continue
            if not tag:
                new_tag_labels.append(tag_label)
                continue
            tags.append(tag)

        new_tag_ids = tag_service.create_tag(user_id, new_tag_labels)
        for tag_id in new_tag_ids:
            tags.append(tag_service.get_tag_by_id(user_id, tag_id))

        file.tags += tags
        self.db.commit()
