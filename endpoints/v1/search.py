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
