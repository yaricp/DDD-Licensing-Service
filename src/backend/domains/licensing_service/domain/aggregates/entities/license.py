from __future__ import annotations
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from backend.core.domain.entity import AbstractEntity

from ...value_objects.license_type import LicenseType
from ...value_objects.license_status import LicenseStatus


@dataclass
class License(AbstractEntity):
    name: str
    description: str
    type: Optional[LicenseType] = LicenseType.BYCOUNT
    subdivision_id: Optional[UUID] = None
    status: Optional[LicenseStatus] = LicenseStatus.ACTIVE
    count_requests: int = 0
    activated: Optional[datetime] = None
    expirated: Optional[datetime] = None
    created: Optional[datetime] = datetime.now()
    expiration: datetime = datetime.now() + timedelta(days=30)
    id: Optional[UUID] = None

    def check(self, count_requests: int) -> None:
        if self.type == LicenseType.BYCOUNT:
            if self.count_requests <= count_requests:
                self.status = LicenseStatus.INACTIVE
                self.expirated = datetime.now()
        elif self.type == LicenseType.BYTIME:
            if self.expiration <= datetime.now():
                self.status = LicenseStatus.INACTIVE
                self.expirated = datetime.now()

    @property
    def is_active(self) -> bool:
        return self.status == LicenseStatus.ACTIVE

    @property
    def is_type_by_count(self) -> bool:
        return self.type == LicenseType.BYCOUNT

    def activate(self) -> None:
        self.status = LicenseStatus.ACTIVE
        self.activated = datetime.now()

    def deactivate(self) -> None:
        self.status = LicenseStatus.INACTIVE
        self.expirated = datetime.now()

    @classmethod
    def make(
        cls, name: str, description: str, type: LicenseType,
        subdivision_id: UUID, count_requests: int
    ) -> License:
        return cls(
            id=uuid4(),
            name=name, description=description,
            type=type, subdivision_id=subdivision_id,
            count_requests=count_requests,
            status=LicenseStatus.INACTIVE,
            created=datetime.now()
        )

    @classmethod
    def make_from_persistence(
        cls, name: str, description: str, type: LicenseType,
        subdivision_id: UUID, count_requests: int, id: UUID,
        status: LicenseStatus, activated: datetime, expirated: datetime,
        created: datetime, expiration: datetime
    ) -> License:
        return cls(
            name=name, description=description,
            type=type, subdivision_id=subdivision_id,
            count_requests=count_requests, status=status,
            created=created, activated=activated,
            expiration=expiration, id=id, expirated=expirated
        )