from typing import Annotated
from fastapi import UploadFile, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from core.models.database import get_db
from core.services.auth import AuthService
from core.services.file import FileService
from core.schemas.file import FileGet
from fastapi.responses import FileResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/files/upload")
async def create_file(
    token: Annotated[str, Depends(oauth2_scheme)],
    file: UploadFile,
    db: Session = Depends(get_db),
):
    file_service = FileService(db)
    auth_service = AuthService(db)
    user = auth_service.get_current_user(token)
    await file_service.create_file(file, user)
    return {"type": file.content_type, "name": file.filename}


@router.get("/files/{file_id}")
def get_file_by_id(file_id: int, db: Session = Depends(get_db)):
    file_service = FileService(db)

    file_path = file_service.get_file_by_id(file_id).path
    return FileResponse(file_path)


@router.get("/files/{file_id}/info", response_model=FileGet)
def get_file_info(token: Annotated[str, Depends(oauth2_scheme)], file_id: int, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    return file_service.get_file_by_id(file_id, user.id)


@router.get("/files", response_model=list[FileGet])
def get_user_files(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    result = file_service.get_user_files(user.id)
    return result


@router.get("/files/by-tag/{tag_id}", response_model=list[FileGet])
def get_user_files_by_tag(
    token: Annotated[str, Depends(oauth2_scheme)], tag_id: int, db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    return file_service.get_user_files_by_tag(user.id, tag_id)


@router.delete("/files/multiple")
def delete_file(
    token: Annotated[str, Depends(oauth2_scheme)],
    files: list[int],
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    file_service.delete_files_by_id(user.id, files)

#
# @router.post("/files/{file_id}/tags")
# def add_file_tag(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     file_id: int,
#     tag_labels: list[str],
#     db: Session = Depends(get_db),
# ):
#     auth_service = AuthService(db)
#     file_service = FileService(db)
#
#     user = auth_service.get_current_user(token)
#     file_service.add_tags(user.id, file_id, tag_labels)


@router.post("/files/tags")
def add_tags_to_files(
    token: Annotated[str, Depends(oauth2_scheme)],
    file_ids: list[int],
    tag_labels: list[str],
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    file_service = FileService(db)
    user = auth_service.get_current_user(token)

    for file_id in file_ids:
        file_service.add_tags(user.id, file_id, tag_labels)

    return {"msg": "success"}
