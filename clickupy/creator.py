from pydantic import BaseModel,  ValidationError, validator

class Creator(BaseModel):
    id: int = None
    username: str = None
    color: str = None
    profile_picture: str = None