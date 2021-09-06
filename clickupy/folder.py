from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator
from clickupy.list import SingleList
from clickupy import client


class Space(BaseModel):
    id: int = None
    name: str = None
    access: bool = None


class Folder(BaseModel):
    id: str = None
    name: str = None
    orderindex: int = None
    override_statuses: bool = None
    hidden: bool = None
    space: Optional[Space] = None
    task_count: int = None
    lists: List[SingleList] = []

    def build_folder(self):
        return Folder(**self)

    def delete(self, client_instance: client):
        model = "folder/"
        deleted_folder_status = client_instance._delete_request(
            model, self.id)


class Folders(BaseModel):
    folders: List[Folder] = None

    def build_folders(self):
        return Folders(**self)
