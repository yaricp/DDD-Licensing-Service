from dataclasses import dataclass
from enum import IntEnum
from uuid import UUID

from backend.core.infra.events import AbstractEvent


class SubdivisionEventAction(IntEnum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    LICENSE_ADDED = 3
    LICENSE_EXPIRED = 4


@dataclass(frozen=True)
class SubdivisionCreatedEvent(AbstractEvent):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: str
    work_status: str
    id: UUID
    action: SubdivisionEventAction = SubdivisionEventAction.CREATED


@dataclass(frozen=True)
class SubdivisionUpdatedEvent(AbstractEvent):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: str
    work_status: str
    id: UUID
    action: SubdivisionEventAction = SubdivisionEventAction.UPDATED


@dataclass(frozen=True)
class SubdivisionDeletedEvent(AbstractEvent):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: str
    work_status: str
    id: UUID
    action: SubdivisionEventAction = SubdivisionEventAction.DELETED


@dataclass(frozen=True)
class SubdivisionLicenseExpiredEvent(AbstractEvent):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: str
    work_status: str
    id: UUID
    action: SubdivisionEventAction = SubdivisionEventAction.LICENSE_EXPIRED
