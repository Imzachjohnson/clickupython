
from typing import Optional
from pydantic import BaseModel,  ValidationError, validator

class Asssignee(BaseModel):
    id: str
    color: str
    username: str
    initials: str
    profilePicture: str