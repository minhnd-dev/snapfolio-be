from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from core.models.tag import Tag
from core.models.user import User
from core.schemas.tag import TagPut
from core.models.file import File


class TagService:
    def __init__(self, db: Session):
        self.db = db

    def get_tag_by_id(self, user_id: int, tag_id: int) -> Tag | None:
        return self.db.scalar(
            select(Tag).where(and_(Tag.id == tag_id, Tag.user_id == user_id))
        )

    def get_tag_by_label(self, user_id: int, tag_label: str):
        return self.db.scalar(
            select(Tag).where(and_(Tag.label == tag_label, Tag.user_id == user_id))
        )

    def create_tag(self, user_id: int, labels: list[str]) -> list[int]:
        labels = set(labels)
        result = []
        for label in labels:
            if not self.tag_exists(label):
                tag = Tag(
                    label=label,
                    user_id=user_id,
                )
                self.db.add(tag)
                self.db.commit()
                self.db.refresh(tag)
                result.append(tag.id)
        return result

    def delete_tags_by_ids(self, user_id: int, tag_ids: list[int]):
        for tag_id in tag_ids:
            tag = self.get_tag_by_id(user_id, tag_id)
            if tag:
                self.db.delete(tag)
        self.db.commit()

    def update_tag(self, user_id: int, tag_id: int, new_label: str):
        tag = self.get_tag_by_id(user_id, tag_id)
        if tag:
            tag.label = new_label
            self.db.commit()

    def tag_exists(self, label: str) -> bool:
        return (
            self.db.scalars(select(Tag).filter(Tag.label == label)).first() is not None
        )

    def get_user_tags(self, user: User):
        stmt = (
            select(Tag.id, Tag.label, count(File.id).label("count"))
            .join(Tag.files, isouter=True)
            .filter(Tag.user_id == user.id)
            .group_by(Tag.id)
            .order_by(count(File.id).desc(), Tag.label)
        )
        return [row._asdict() for row in self.db.execute(stmt)]

    def update_tags(self, user: User, tags: list[TagPut]):
        tag_ids = [tag.id for tag in tags]

        user.tags = [tag for tag in user.tags if tag.id in tag_ids]

        for tag_put in tags:
            if tag_put.id:
                tag = self.get_tag_by_id(user.id, tag_put.id)
                if tag.label != tag_put.label:
                    tag.label = tag_put.label
            else:
                tag = Tag(label=tag_put.label, user_id=user.id)
                self.db.add(tag)
                self.db.commit()
                self.db.refresh(tag)
        self.db.commit()
