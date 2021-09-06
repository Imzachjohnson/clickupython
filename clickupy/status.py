class Status:
    status: str
    color: str
    orderindex: int
    type: str

    def __init__(self, status: str, color: str, orderindex: int, type: str) -> None:
        self.status = status
        self.color = color
        self.orderindex = orderindex
        self.type = type