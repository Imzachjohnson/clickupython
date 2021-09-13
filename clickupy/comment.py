from typing import List, Any
from clickupy.assignee import Asssignee
from pydantic import BaseModel


class AssignedBy(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profile_picture: str = None


class CommentComment(BaseModel):
    text: str = None


class Comment(BaseModel):
    id: str = None
    comment: List[CommentComment] = None
    comment_text: str = None
    user: AssignedBy = None
    resolved: bool = None
    assignee: AssignedBy = None
    assigned_by: AssignedBy = None
    reactions: List[Any] = None
    date: str = None


    def build_comment(self):
        return Comment(**self)


class Comments(BaseModel):
    comments: List[Comment] = None

    def __iter__(self):
        return iter(self.comments)

    def build_comments(self):
        return Comments(**self)