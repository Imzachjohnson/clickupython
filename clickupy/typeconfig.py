class TypeConfig:
    include_guests: Optional[bool]
    include_team_members: Optional[bool]

    def __init__(self, include_guests: Optional[bool], include_team_members: Optional[bool]) -> None:
        self.include_guests = include_guests
        self.include_team_members = include_team_members