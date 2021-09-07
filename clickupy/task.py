from typing import Optional, List, Any
from uuid import UUID
from pydantic import BaseModel,  ValidationError, validator

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