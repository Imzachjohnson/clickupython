
from typing import Optional
from pydantic import BaseModel,  ValidationError, validator

class Asssignee(BaseModel):
    id: int
    color: str
    username: str
    initials: str
    profilePicture: str