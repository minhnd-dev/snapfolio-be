from pydantic import BaseModel


class TagBase(BaseModel):
    label: str

