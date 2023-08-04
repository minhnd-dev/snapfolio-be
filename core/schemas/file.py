from pydantic import BaseModel

class FileBase(BaseModel):
    name: str
    path: str
    content_type: str | None
    user_id: int | None


class FileCreate(FileBase):
    pass


class FileGet(FileBase):
    pass
