
from typing import Optional
from pydantic import BaseModel,  ValidationError, validator

class TypeConfig(BaseModel):
    include_guests: Optional[bool]
    include_team_members: Optional[bool]