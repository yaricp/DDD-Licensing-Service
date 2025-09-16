from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from uuid import UUID

from backend.core.infra.events import AbstractEvent


class LicenseEventAction(IntEnum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ACTIVATED = 3
    DEACTIVATED = 4


@dataclass(frozen=True)
class LicenseActivatedEvent(AbstractEvent):
    name: str
    description: str
    type: str
    subdivision_id: UUID
    status: str
    count_requests: int
    activated: datetime
    expirated: datetime
    created: datetime
    expiration: datetime
    id: UUID
    action: LicenseEventAction = LicenseEventAction.ACTIVATED


@dataclass(frozen=True)
class LicenseDeactivatedEvent(AbstractEvent):
    name: str
    description: str
    type: str
    subdivision_id: UUID
    status: str
    count_requests: int
    activated: datetime
    expirated: datetime
    created: datetime
    expiration: datetime
    id: UUID
    action: LicenseEventAction = LicenseEventAction.DEACTIVATED


@dataclass(frozen=True)
class LicenseCreatedEvent(AbstractEvent):
    name: str
    description: str
    type: str
    subdivision_id: UUID
    status: str
    count_requests: int
    activated: datetime
    expirated: datetime
    created: datetime
    expiration: datetime
    id: UUID
    action: LicenseEventAction = LicenseEventAction.CREATED


@dataclass(frozen=True)
class LicenseDeletedEvent(AbstractEvent):
    name: str
    description: str
    type: str
    subdivision_id: UUID
    status: str
    count_requests: int
    activated: datetime
    expirated: datetime
    created: datetime
    expiration: datetime
    id: UUID
    action: LicenseEventAction = LicenseEventAction.DELETED
