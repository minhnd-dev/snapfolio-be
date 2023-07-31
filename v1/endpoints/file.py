from fastapi import FastAPI, File, UploadFile, APIRouter, Depends
import random

from sqlalchemy.orm import Session

from core.models.database import get_db
from core.services.file import FileService

router = APIRouter()

@router.post("/files/")
async def create_file(file: UploadFile, db: Session = Depends(get_db)):
    file_service = FileService(db)
    await file_service.create_file(file)
    return {"type": file.content_type, "name": file.filename}
    
