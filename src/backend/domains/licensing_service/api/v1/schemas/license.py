from datetime import datetime, timedelta
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class LicenseType(StrEnum):
    BYTIME = "by_time"
    BYCOUNT = "by_count"


class LicenseStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class LicenseBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[LicenseType] = None
    subdivision_id: Optional[UUID] = None
    status: Optional[LicenseStatus] = None
    count_requests: Optional[int] = None
    activated: Optional[datetime] = None
    expirated: Optional[datetime] = None
    created: Optional[datetime] = None
    expiration: Optional[datetime] = None

    class Config:
        from_attributes = True


class LicenseCreate(BaseModel):
    name: str
    description: str
    type: LicenseType
    count_requests: int
    subdivision_id: UUID


class LicenseUpdate(BaseModel):
    id: UUID
    name: str
    description: str
    subdivision_id: Optional[UUID] = None


class License(LicenseBase):
    pass
