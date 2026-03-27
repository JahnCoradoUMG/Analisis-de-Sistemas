from app.models.schemas import CheckIn, Client, Membership, Payment


class InMemoryStorage:
    def __init__(self) -> None:
        self.clients: dict[str, Client] = {}
        self.memberships: dict[str, Membership] = {}
        self.payments: dict[str, Payment] = {}
        self.checkins: dict[str, CheckIn] = {}


storage = InMemoryStorage()
