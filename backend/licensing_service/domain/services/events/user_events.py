from uuid import UUID
from enum import IntEnum
from typing import Optional
from dataclasses import dataclass

from backend.core.infra.events import AbstractEvent


class UserEventAction(IntEnum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2


@dataclass(frozen=True)
class UserCreatedEvent(AbstractEvent):
    user_id: UUID
    email: Optional[str] = None
    tg_id: Optional[str] = None
    action: UserEventAction = UserEventAction.CREATED


@dataclass(frozen=True)
class UserUpdatedEvent(AbstractEvent):
    user_id: UUID
    email: str
    tg_id: str
    superadmin: bool = False
    tenant_id: Optional[UUID] = None
    subdivision_id: Optional[UUID] = None
    action: UserEventAction = UserEventAction.UPDATED
