from core.services.tag import TagService
from fastapi import APIRouter, Depends
from core.models.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/tag")
def create_tag(label: str, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    tag_service.create_tag(label)
    return {"msg": "success"}



