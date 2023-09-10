from operator import not_

from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, delete
import os

from sqlalchemy.sql.functions import count

from core.models.file import File
from core.models.tag import Tag
from core.models.user import User

from core.services.tag import TagService
from uuid import uuid4


class FileNotFound(Exception):
    pass


class FileService:
    def __init__(self, db: Session):
        self.db = db

    async def create_file(self, file: UploadFile, user: User):
        file_code = str(uuid4())
        file_path = f"files/{file_code}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        db_file = File(
            name=file.filename,
            path=file_path,
            content_type=file.content_type,
            user=user,
            code=file_code,
            size=file.size,
        )
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

    def get_user_files(
        self, user_id: int, limit: int, offset: int
    ) -> (list[File], int):
        query = select(File).filter(File.user_id == user_id).limit(limit).offset(offset)

        total = self.db.scalar(select(count()).filter(File.user_id == user_id))

        return list(self.db.scalars(query).all()), total

    def get_user_files_by_tag(self, user_id, tag_id) -> (list[File], int):
        data = list(
            self.db.scalars(
                select(File)
                .join(File.tags.and_(Tag.id == tag_id))
                .filter(and_(File.user_id == user_id))
            )
        )
        total = self.db.scalar(
            select(count())
            .join(File.tags.and_(Tag.id == tag_id))
            .filter(and_(File.user_id == user_id))
        )
        return data, total

    def get_file_by_id(self, file_id: int, user_id: int | None = None) -> File | None:
        return (
            self.db.query(File)
            .filter(and_(File.id == file_id, File.user_id == user_id))
            .first()
        )

    def get_file_by_code(self, file_code: str) -> File | None:
        return self.db.scalar(select(File).filter(File.code == file_code))

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

    def delete_files_by_id(self, user_id: int, files: list[int], select_all: False):
        if select_all:
            stmt = select(File.id).filter(
                and_(File.id.not_in(files), File.user_id == user_id)
            )
            files = self.db.scalars(stmt)
        for file_id in files:
            self.delete_file_by_id(user_id, file_id)

    def update_file_tags(self, user_id: int, file_id: int, tag_labels: list[str]):
        tag_labels = set(tag_labels)
        tag_service = TagService(self.db)

        file = self.get_file_by_id(file_id, user_id)
        if not file:
            raise FileNotFound

        # remove deleted tags
        file.tags = [tag for tag in file.tags if tag.label in tag_labels]

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

    def update_files_tags(
        self,
        user_id: int,
        files_ids: list[int],
        added: list[str],
        removed: list[str],
        select_all: bool = False,
    ):
        if select_all:
            stmt = select(File.id).filter(
                and_(File.id.not_in(files_ids), File.user_id == user_id)
            )
            files_ids = self.db.scalars(stmt)

        added_tags = []
        for tag_label in set(added):
            if tag_label in removed:
                continue
            tag = self.db.scalar(select(Tag).where(and_(Tag.label==tag_label, Tag.user_id==user_id)))
            if not tag:
                tag = Tag(label= tag_label, user_id=user_id)
                self.db.add(tag)
                self.db.commit()
                self.db.refresh(tag)
            added_tags.append(tag)

        for file_id in files_ids:
            file = self.db.scalar(select(File).where(and_(File.id == file_id, File.user_id == user_id)))
            existed_tags = [tag.label for tag in file.tags]
            for tag in added_tags:
                if tag.label not in existed_tags:
                    file.tags.append(tag)

            file.tags = [tag for tag in file.tags if tag.label not in removed]
        self.db.commit()
