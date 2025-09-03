from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

from backend.core.infra.commands import AbstractCommand


@dataclass(frozen=True)
class AddStatisticRowCommand(AbstractCommand):
    subdivision_id: UUID
    created: datetime
    count_requests: int


@dataclass(frozen=True)
class ActivateSubdivisionLicenseCommand(AbstractCommand):
    subdivision_id: UUID
    license_id: UUID


@dataclass(frozen=True)
class DeactivateSubdivisionLicenseCommand(AbstractCommand):
    subdivision_id: UUID
    license_id: UUID


@dataclass(frozen=True)
class CreateSubdivisionCommand(AbstractCommand):
    name: str
    location: str
    tenant_id: UUID


@dataclass(frozen=True)
class UpdateSubdivisionCommand(AbstractCommand):
    id: UUID
    name: str
    location: str
    work_status: str
    link_to_subdivision_processing_domain: str


@dataclass(frozen=True)
class DeleteSubdivisionCommand(AbstractCommand):
    id: UUID
