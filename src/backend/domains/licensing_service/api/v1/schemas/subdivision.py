from enum import StrEnum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .license import License
from .statictic_row import StatisticRow


class WorkStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SubdivisionBase(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    tenant_id: Optional[UUID] = None
    link_to_subdivision_processing_domain: Optional[str] = None
    work_status: Optional[WorkStatus] = None
    id: Optional[UUID] = None
    licenses: List[License] = []
    statistics: List[StatisticRow] = []


class SubdivisionCreate(BaseModel):
    name: str
    location: str
    tenant_id: UUID


class SubdivisionUpdate(BaseModel):
    id: UUID
    name: str
    location: str
    link_to_subdivision_processing_domain: str
    work_status: str


class Subdivision(SubdivisionBase):
    pass
