from pydantic import BaseModel
from core.schemas.tag import TagGet


class FileBase(BaseModel):
    name: str
    path: str
    content_type: str | None
    user_id: int | None
    code: str
    size: int


class FileCreate(FileBase):
    pass


class FileGet(FileBase):
    id: int
    tags: list[TagGet]
    pass


class GetUserFilesResonse(BaseModel):
    data: list[FileGet]
    total: int
