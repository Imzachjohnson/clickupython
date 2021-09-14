from typing import Optional, List
from pydantic import BaseModel


class Checklist(BaseModel):
    id: Optional[str]
    task_id: str = None
    name: str = None
    orderindex: int = None
    resolved: int = None
    unresolved: int = None
    items: List[str] = None


class Checklists(BaseModel):
    checklist: Checklist

    def build_checklist(self):
        final_checklist = Checklists(**self)
        return final_checklist.checklist
