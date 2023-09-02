from pydantic import BaseModel


class TagBase(BaseModel):
    id: int
    label: str


class TagGet(TagBase):
    pass

