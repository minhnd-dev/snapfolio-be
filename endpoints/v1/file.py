from typing import Annotated
from fastapi import UploadFile, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from core.models.database import get_db
from core.services.auth import AuthService
from core.services.file import FileService
from core.schemas.file import FileGet, GetUserFilesResonse
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


@router.get("/files/{file_code}")
def get_file_by_id(file_code: str, db: Session = Depends(get_db)):
    file_service = FileService(db)

    file_path = file_service.get_file_by_code(file_code).path
    return FileResponse(file_path)


@router.get("/files/{file_id}/info", response_model=FileGet)
def get_file_info(token: Annotated[str, Depends(oauth2_scheme)], file_id: int, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    return file_service.get_file_by_id(file_id, user.id)


@router.get("/files", response_model=GetUserFilesResonse)
def get_user_files(
    token: Annotated[str, Depends(oauth2_scheme)], limit: int, offset: int, db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    files, total = file_service.get_user_files(user.id, limit, offset)
    return {
        "data": files,
        "total": total
    }


@router.get("/files/by-tag/{tag_id}", response_model=GetUserFilesResonse)
def get_user_files_by_tag(
    token: Annotated[str, Depends(oauth2_scheme)], tag_id: int, db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    files, total = file_service.get_user_files_by_tag(user.id, tag_id)
    return {
        "data": files,
        "total": total
    }


@router.delete("/files/multiple")
def delete_file(
    token: Annotated[str, Depends(oauth2_scheme)],
    files: list[int],
    select_all: bool = False,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    file_service.delete_files_by_id(user.id, files, select_all=select_all)


@router.patch("/files/{file_id}/tags")
def update_file_tags(
    token: Annotated[str, Depends(oauth2_scheme)],
    file_id: int,
    tag_labels: list[str],
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    file_service.update_file_tags(user.id, file_id, tag_labels)
    return {"msg": "success"}


@router.put("/files/tags")
def update_files_tags(
    token: Annotated[str, Depends(oauth2_scheme)],
    files_ids: list[int],
    added: list[str],
    removed: list[str],
    select_all: bool = False,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    file_service = FileService(db)
    user = auth_service.get_current_user(token)

    file_service.update_files_tags(user.id, files_ids, added, removed, select_all)
    return {"msg": "success"}
