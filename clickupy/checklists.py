from typing import Optional, List
from pydantic import BaseModel
from clickupy import assignee

class ChecklistItem(BaseModel):
    id: str = None
    name: str = None
    orderindex: int = None
    assignee: Optional[assignee.Asssignee]

class Checklist(BaseModel):
    id: Optional[str]
    task_id: str = None
    name: str = None
    orderindex: int = None
    resolved: int = None
    unresolved: int = None
    items: List[ChecklistItem] = None

    def add_item(self, client_instance, name: str, assignee:str = None):
        return client_instance.create_checklist_item(self.id, name = name, assignee = assignee)

class Checklists(BaseModel):
    checklist: Checklist

    def build_checklist(self):
        final_checklist = Checklists(**self)
        return final_checklist.checklist
