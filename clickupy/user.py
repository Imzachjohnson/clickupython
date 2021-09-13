from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator, Field


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profilePicture: str = None
