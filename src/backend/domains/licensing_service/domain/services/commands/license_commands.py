from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from backend.core.infra.commands import AbstractCommand


@dataclass(frozen=True)
class CreateLicenseCommand(AbstractCommand):
    name: str
    description: str
    type: str
    subdivision_id: UUID
    count_requests: Optional[int]


@dataclass(frozen=True)
class UpdateLicenseCommand(AbstractCommand):
    id: UUID
    name: str
    description: str
    subdivision_id: UUID


@dataclass(frozen=True)
class DeleteLicenseCommand(AbstractCommand):
    id: UUID
    subdivision_id: UUID
