from pydantic import BaseModel


class TagBase(BaseModel):
    id: int
    label: str


class TagGet(TagBase):
    pass


class TagPut(BaseModel):
    id: int | None
    label: str
