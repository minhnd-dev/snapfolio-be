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


@router.post("/files/")
async def create_file(token: Annotated[str, Depends(oauth2_scheme)], file: UploadFile, db: Session = Depends(get_db)):
    file_service = FileService(db)
    auth_service = AuthService(db)
    user = auth_service.get_current_user(token)
    await file_service.create_file(file, user.id)
    return {"type": file.content_type, "name": file.filename}


@router.get("/file/{file_name_or_id}")
def get_file_by_id(file_name_or_id: str, db: Session = Depends(get_db)):
    file_service = FileService(db)

    file_path = file_service.get_file_by_id(file_name_or_id)
    if not file_path:
        file_path = f"files/{file_name_or_id}"    
    return FileResponse(file_path)


@router.get("/files/user", response_model=list[FileGet])
def get_user_files(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    result = file_service.get_user_files(user.id)
    return result


@router.delete("/files/{file_id}")
def delete_file(token: Annotated[str, Depends(oauth2_scheme)], file_id: str):
    auth_service = AuthService(db)
    file_service = FileService(db)

    user = auth_service.get_current_user(token)
    file_service.delete_file_by_id(user.id, file_id)

