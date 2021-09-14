from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator, Field


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profilePicture: str = None
    initials: Optional[str] = None
    role: Optional[int] = None
    custom_role: Optional[None] = None
    last_active: Optional[str] = None
    date_joined: Optional[str] = None
    date_invited: Optional[str] = None
