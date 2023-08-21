from sqlalchemy.orm import Session
from core.models.tag import Tag


class TagService:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, label: str):
        tag = Tag(label=label)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

