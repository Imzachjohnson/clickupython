from typing import Optional, List, Any
from uuid import UUID


class Task:
    id: str
    custom_id: None
    name: str
    text_content: str
    description: str
    status: Status
    orderindex: str
    date_created: str
    date_updated: str
    date_closed: None
    creator: Creator
    assignees: List[Any]
    checklists: List[Any]
    tags: List[Any]
    parent: None
    priority: None
    due_date: None
    start_date: None
    time_estimate: None
    time_spent: None
    custom_fields: List[CustomField]
    list: Folder
    folder: Folder
    space: Folder
    url: str

    def __init__(self, id: str, custom_id: None, name: str, text_content: str, description: str, status: Status, orderindex: str, date_created: str, date_updated: str, date_closed: None, creator: Creator, assignees: List[Any], checklists: List[Any], tags: List[Any], parent: None, priority: None, due_date: None, start_date: None, time_estimate: None, time_spent: None, custom_fields: List[CustomField], list: Folder, folder: Folder, space: Folder, url: str) -> None:
        self.id = id
        self.custom_id = custom_id
        self.name = name
        self.text_content = text_content
        self.description = description
        self.status = status
        self.orderindex = orderindex
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_closed = date_closed
        self.creator = creator
        self.assignees = assignees
        self.checklists = checklists
        self.tags = tags
        self.parent = parent
        self.priority = priority
        self.due_date = due_date
        self.start_date = start_date
        self.time_estimate = time_estimate
        self.time_spent = time_spent
        self.custom_fields = custom_fields
        self.list = list
        self.folder = folder
        self.space = space
        self.url = url
