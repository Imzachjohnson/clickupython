class Creator:
    id: int
    username: str
    color: str
    profile_picture: str

    def __init__(self, id: int, username: str, color: str, profile_picture: str) -> None:
        self.id = id
        self.username = username
        self.color = color
        self.profile_picture = profile_picture