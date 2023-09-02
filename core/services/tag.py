from sqlalchemy.orm import Session
from core.models.tag import Tag


class TagService:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, user_id: int, labels: list[str]):
        labels = set(labels)
        for label in labels:
            pass





