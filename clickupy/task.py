from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator, Field
from clickupy.customfield import CustomField
from clickupy.status import Status
from clickupy.creator import Creator
from clickupy import client
from clickupy import attachment
from clickupy.priority import Priority

import ntpath

import os


class ClickupList(BaseModel):
    id: str = None


class Folder(BaseModel):
    id: str = None


class Space(BaseModel):
    id: str = None


class Task(BaseModel):
    id: str = None
    custom_id: None = None
    name: str = None
    text_content: str = None
    description: str = None
    status: Status = None
    orderindex: str = None
    date_created: str = None
    date_updated: str = None
    date_closed: None = None
    creator: Creator = None
    task_assignees: List[Any] = Field(None, alias="assignees")
    task_checklists: List[Any] = Field(None, alias="checklists")
    task_tags: List[Any] = Field(None, alias="tags")
    parent: str = None
    priority: Optional[Priority]
    due_date: str = None
    start_date: str = None
    time_estimate: str = None
    time_spent: Optional[str] = None
    custom_fields: List[CustomField] = None
    list: ClickupList
    folder: Folder
    space: Folder
    url: str

    @validator('priority')
    def check_status(cls, v):

        if v == "":
            v = 4

            return v

    def build_task(self):
        return Task(**self)

    def delete(self):
        client.ClickUpClient.delete_task(self, self.id)

    def upload_attachment(self, client_instance: client, file_path: str):
        return client_instance.upload_attachment(self.id, file_path)

    def update(self, client_instance: client,  name: str = None, description: str = None, status: str = None, priority: int = None, time_estimate: int = None,
               archived: bool = None, add_assignees: List[str] = None, remove_assignees: List[int] = None):

        return client_instance.update_task(self.id, name, description, status, priority, time_estimate, archived, add_assignees, remove_assignees)

    def add_comment(self, client_instance: client, comment_text: str, assignee: str = None, notify_all: bool = True):
        return client_instance.create_task_comment(self.id, comment_text, assignee, notify_all)

    def get_comments(self, client_instance):
        return client_instance.get_task_comments(self.id)


class Tasks(BaseModel):
    tasks: List[Task] = None

    def build_tasks(self):
        return Tasks(**self)
