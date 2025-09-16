from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from backend.core.domain.aggregate import AbstractAggregateRoot

from .entities.user import User
from .subdivision import Subdivision


@dataclass(eq=False, slots=True)
class Tenant(AbstractAggregateRoot):
    name: str
    address: str
    email: str
    phone: str
    id: Optional[UUID] = None
    users: List[User] = field(default_factory=lambda: [])
    subdivisions: List[Subdivision] = field(default_factory=lambda: [])

    def update(self, name: str, address: str, email: str, phone: str) -> None:
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone

    @classmethod
    def make(
        cls, user_id: UUID, name: str, address: str, email: str, phone: str
    ) -> Tenant:
        print("Factory method")
        user = User.make(user_id)
        return cls(
            name=name,
            address=address,
            email=email,
            phone=phone,
            users=[user],
            subdivisions=[],
        )

    @classmethod
    def make_from_persistence(
        cls,
        id: UUID,
        name: str,
        address: str,
        email: str,
        phone: str,
        users: list,
        subdivisions: list,
    ) -> Tenant:
        print("Make aggregate form DB method")
        return cls(
            id=id,
            name=name,
            address=address,
            email=email,
            phone=phone,
            users=users,
            subdivisions=subdivisions,
        )
