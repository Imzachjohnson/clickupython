
from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator
from clickupy.typeconfig import TypeConfig

class CustomField(BaseModel):
    id: str
    name: str
    type: str
    type_config: TypeConfig
    date_created: str
    hide_from_guests: bool
    value: Optional[str]
    required: bool