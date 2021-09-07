from pydantic import BaseModel,  ValidationError, validator

class Status(BaseModel):
    status: str
    color: str
    orderindex: int
    type: str