from pydantic import BaseModel

class FileBase(BaseModel):
    name: str
    path: str
    content_type: str | None
    size: int | None
    user_id: str | None


class FileCreate(FileBase):
    pass
