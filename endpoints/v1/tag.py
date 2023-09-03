from typing import Annotated

from fastapi.security import OAuth2PasswordBearer

from core.schemas.tag import TagPut
from core.services.auth import AuthService
from core.services.tag import TagService
from fastapi import APIRouter, Depends
from core.models.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/tags")
def get_tags(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tag_service = TagService(db)
    user = auth_service.get_current_user(token)

    return tag_service.get_user_tags(user)


@router.post("/tags")
def create_tags(token: Annotated[str, Depends(oauth2_scheme)], labels: list[str], db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tag_service = TagService(db)
    user = auth_service.get_current_user(token)

    tag_service.create_tag(user.id, labels)
    return {"msg": "success"}


@router.delete("/tags")
def delete_tags(token: Annotated[str, Depends(oauth2_scheme)], tag_ids: list[int], db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tag_service = TagService(db)

    user = auth_service.get_current_user(token)
    tag_service.delete_tags_by_ids(user.id, tag_ids)
    return {"msg": "success"}


@router.put("/tags")
def update_tags(token: Annotated[str, Depends(oauth2_scheme)], tags: list[TagPut], db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tag_service = TagService(db)

    user = auth_service.get_current_user(token)
    tag_service.update_tags(user, tags)

    return {"msg": "success"}


@router.patch("/tags/{tag_id}")
def update_tag(token: Annotated[str, Depends(oauth2_scheme)], tag_id: int, label: str, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tag_service = TagService(db)

    user = auth_service.get_current_user(token)
    tag_service.update_tag(user.id, tag_id, label)
    return {"msg": "success"}
