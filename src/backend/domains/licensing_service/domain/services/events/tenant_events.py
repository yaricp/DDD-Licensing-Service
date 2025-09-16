from dataclasses import dataclass
from enum import IntEnum
from uuid import UUID

from backend.core.infra.events import AbstractEvent


class TenantEventAction(IntEnum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    SUBDIVISION_ADDED = 3
    LICENSE_ADDED = 4


@dataclass(frozen=True)
class TenantCreatedEvent(AbstractEvent):
    id: UUID
    name: str
    address: str
    email: str
    phone: str
    action: TenantEventAction = TenantEventAction.CREATED


@dataclass(frozen=True)
class TenantUpdatedEvent(AbstractEvent):
    id: UUID
    name: str
    address: str
    email: str
    phone: str
    action: TenantEventAction = TenantEventAction.UPDATED


@dataclass(frozen=True)
class TenantDeletedEvent(AbstractEvent):
    id: UUID
    name: str
    address: str
    email: str
    phone: str
    action: TenantEventAction = TenantEventAction.DELETED
