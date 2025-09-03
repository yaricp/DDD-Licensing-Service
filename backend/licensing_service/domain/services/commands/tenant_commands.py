from uuid import UUID
from dataclasses import dataclass

from backend.core.infra.commands import AbstractCommand


@dataclass(frozen=True)
class CreateTenantCommand(AbstractCommand):
    user_id: str
    name: str
    address: str
    email: str
    phone: str


@dataclass(frozen=True)
class UpdateTenantCommand(AbstractCommand):
    id: UUID
    name: str
    address: str
    email: str
    phone: str


@dataclass(frozen=True)
class DeleteTenantCommand(AbstractCommand):
    id: UUID
