from typing import Optional, List
from clickupy import user
from pydantic import BaseModel

class InvitedBy(BaseModel):
    id: str = None
    username: str = None
    color: str = None
    email: str = None
    initials: str = None
    profile_picture: None = None


class Member(BaseModel):
    user: user.User
    invited_by: Optional[InvitedBy] = None


class Team(BaseModel):
    id: str = None
    name: str = None
    color: str = None
    avatar: str = None
    members: List[Member] = None


class Teams(BaseModel):
    teams: List[Team] = None

    def __iter__(self):
        return iter(self.teams)

    def build_teams(self):
        return Teams(**self)