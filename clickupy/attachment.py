from pydantic import BaseModel


class Attachment(BaseModel):

    id: str
    version: int
    date: str
    title: str
    extension: str
    thumbnail_small: str
    thumbnail_large: str
    url: str


def build_attachment(self):
    return Attachment(**self)
