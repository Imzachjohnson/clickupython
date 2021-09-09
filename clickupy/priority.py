from pydantic import BaseModel,  ValidationError, validator

class Priority(BaseModel):
    id: int = None
    priority: str = None
    color: str = None
    orderindex: str = None