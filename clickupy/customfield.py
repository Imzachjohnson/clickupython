
from uuid import UUID
from typing import Optional, List, Any

class CustomField:
    id: UUID
    name: str
    type: str
    type_config: TypeConfig
    date_created: str
    hide_from_guests: bool
    value: Optional[str]
    required: bool

    def __init__(self, id: UUID, name: str, type: str, type_config: TypeConfig, date_created: str, hide_from_guests: bool, value: Optional[str], required: bool) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.type_config = type_config
        self.date_created = date_created
        self.hide_from_guests = hide_from_guests
        self.value = value
        self.required = required