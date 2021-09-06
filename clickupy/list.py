from typing import Optional, List
import json
from pydantic import BaseModel,  ValidationError, validator


class Folder(BaseModel):
    id: int
    name: str
    hidden: Optional[bool]
    access: bool


class Priority(BaseModel):
    priority: str
    color: str


class Status(BaseModel):
    status: str
    color: str
    hide_label: bool


class StatusElement(BaseModel):
    id: str
    status: str
    orderindex: int
    color: str
    type: str


class SingleList(BaseModel):
    id: int = None
    name: str = None
    deleted: bool = None
    archived: bool = None
    orderindex: int = None
    override_statuses: bool = None
    priority: Optional[Priority] = None
    assignee: None = None
    due_date: str = None
    start_date: None
    folder: Folder = None
    space: Folder = None
    statuses: List[StatusElement] = None
    inbound_address: str = None
    permission_level: str = None
    content: Optional[str] = None
    status: Optional[Status] = None
    task_count: Optional[int] = None
    start_date_time: Optional[None] = None
    due_date_time: Optional[bool] = None

    # return a single list
    def build_list(self):
        return SingleList(**self)


class AllLists(BaseModel):
    lists: List[SingleList] = None

    # return a list of lists
    def build_lists(self):
        return AllLists(**self)
