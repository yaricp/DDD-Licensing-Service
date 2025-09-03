from __future__ import annotations

from uuid import UUID
from typing import Optional, List
from dataclasses import dataclass, field

from backend.core.domain.aggregate import AbstractAggregateRoot

# from ..exceptions.tenant import (
#     TenantAlreadyExistsError,
#     TenantNotFoundError
# )

from .subdivision import Subdivision
from .entities.user import User

from ..services.commands.user_commands import CreateUserCommand


@dataclass(eq=False, slots=True)
class Tenant(AbstractAggregateRoot):
    name: str
    address: str
    email: str
    phone: str
    id: Optional[UUID] = None
    users: List[User] = field(default_factory=lambda: [])
    subdivisions: List[Subdivision] = field(default_factory=lambda: [])
    _domain_events: List[object] = field(default_factory=list, repr=False)

    def update(
        self, name: str, address: str, email: str, phone: str
    ) -> None:
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone

    def __post_init__(self):
        if not hasattr(self, "_domain_events"):
            self._domain_events = []

    def pull_events(self) -> List[object]:
        events = self._domain_events
        self._domain_events = []
        return events

    @classmethod
    def make(
        cls, name: str, address: str, email: str, phone: str
    ) -> Tenant:
        print("Factory method")
        return cls(
            name=name, address=address, email=email, phone=phone,
            users=[], subdivisions=[], _domain_events=[]
        )

    @classmethod
    def make_from_persistence(
        cls, id: UUID, name: str, address: str, email: str,
        phone: str, users: list, subdivisions: list
    ) -> Tenant:
        print("Make aggregate form DB method")
        return cls(
            id=id, name=name, address=address, email=email, phone=phone,
            users=users, subdivisions=subdivisions, _domain_events=[]
        )

    def add_user(self, user: CreateUserCommand) -> None:
        "Adding user for current Tenant"
        self._domain_events.append(user)
