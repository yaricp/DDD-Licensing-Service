from __future__ import annotations
from uuid import UUID, uuid4
from typing import List, Optional
from dataclasses import dataclass, field

from backend.core.domain.aggregate import AbstractAggregateRoot
from backend.core.infra.eventbus import AbstractEventBus

from .entities.license import License
from .entities.stat_row import StatisticRow
from ..exceptions.subdivision import SubdivisionInactiveError
from ..exceptions.license import (
    LicenseExpiredError, LicenseInactiveError, LicenseAlreadyInUseError,
    LicenseWrongTenantError, LicenseNotFoundError
)
from ..exceptions.statistic_row import (
    SubdivisionStatisticAlreadyExistsError
)
from ..value_objects.work_status import WorkStatus
from ..value_objects.license_status import LicenseStatus
from ..value_objects.license_type import LicenseType
from ..services.events.license_events import (
    LicenseActivatedEvent, LicenseDeactivatedEvent
)
from ..services.events.statistic_row_events import StatisticRowAddedEvent


@dataclass(eq=False, slots=True)
class Subdivision(AbstractAggregateRoot):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: Optional[str] = ""
    work_status: WorkStatus = WorkStatus.ACTIVE
    id: Optional[UUID] = None
    licenses: List[License] = field(default_factory=lambda: [])
    statistics: List[StatisticRow] = field(default_factory=lambda: [])

    def update(
        self, name: str, location: str,
        link_to_subdivision_processing_domain: str,
        work_status: WorkStatus
    ) -> None:
        self.name = name
        self.location = location
        self.link_to_subdivision_processing_domain = (
            link_to_subdivision_processing_domain
        )
        self.work_status = work_status

    def add_license(
        self, name: str, description: str, type: LicenseType,
        count_requests: int, subdivision_id: UUID
    ) -> License:
        new_license = License.make(
            name=name, description=description, type=type,
            subdivision_id=subdivision_id, count_requests=count_requests
        )
        self.licenses.append(new_license)
        return new_license

    def update_license(
        self, id: UUID, name: str,
        description: str,
        type: LicenseType = LicenseType.BYTIME,
        count_requests: int = 0
    ) -> None:
        filtered_licenses = list(filter(
            lambda x: x.id == id, self.licenses
        ))
        if not filtered_licenses:
            raise LicenseNotFoundError

        new_license = filtered_licenses[0]
        new_license.name = name
        new_license.description = description
        new_license.type = type
        new_license.count_requests = count_requests

    def delete_license(self, id: UUID) -> None:
        filtered_licenses: List[License] = list(filter(
            lambda x: x.id == id, self.licenses
        ))
        if not filtered_licenses:
            raise LicenseNotFoundError
        current_license = filtered_licenses[0]
        if current_license.is_active:
            current_license.deactivate()
            self.deactivate()
        self.licenses.remove(current_license)

    def activate(self):
        self.work_status = WorkStatus.ACTIVE

    def deactivate(self):
        self.work_status = WorkStatus.INACTIVE

    @property
    def active_license(self) -> License | None:
        for license in self.licenses:
            if license.is_active:
                return license
        return None

    @property
    def total_count_requests(self) -> int:
        if not self.active_license:
            return 0
        if not self.statistics:
            return 0
        for strow in self.statistics:
            print(f"strow: {strow}")
        return sum(
            r.count_requests for r in filter(
                lambda x: x.created > self.active_license.activated,
                self.statistics
            )
        )

    def check_license(self):
        if self.active_license:
            self.active_license.check(
                self.total_count_requests
            )

    async def activate_license(
        self, license_id: UUID, eventbus: AbstractEventBus | None
    ) -> None:
        print("Activate_license started")
        print(f"self.licenses: {self.licenses}")
        print(f"license_id: {license_id}")
        filtered_license: Optional[License] = list(filter(
            lambda x: x.id == license_id,
            self.licenses
        ))
        print(f"filtered_license: {filtered_license}")
        if not filtered_license:
            raise LicenseNotFoundError
        license = filtered_license[0]
        license.activate()
        license.check(self.total_count_requests)
        if license.is_active:
            self.activate()
        if eventbus:
            eventbus.add_event(
                LicenseActivatedEvent(
                    **await license.to_dict()
                )
            )

    async def deactivate_license(
        self, license_id: UUID, eventbus: AbstractEventBus | None
    ) -> None:
        print("deactivate_license started")
        filtered_license: Optional[License] = list(filter(
            lambda x: x.id == license_id,
            self.licenses
        ))
        if not filtered_license:
            raise LicenseNotFoundError
        license = filtered_license[0]
        license.deactivate()
        self.deactivate()
        if eventbus:
            eventbus.add_event(
                LicenseDeactivatedEvent(
                    **await license.to_dict()
                )
            )

    async def save_day_statistic(
        self, stat_row: StatisticRow,
        eventbus: AbstractEventBus | None
    ):
        print(f"stat_row: {stat_row}")
        if not self.is_active:
            raise SubdivisionInactiveError
        if not self.active_license:
            raise LicenseInactiveError
        if stat_row in self.statistics:
            raise SubdivisionStatisticAlreadyExistsError
        print(f"type(stat_row): {type(stat_row)}")
        if (
            stat_row.count_requests + self.total_count_requests
        ) >= self.active_license.count_requests:
            deactivated_license = self.active_license
            self.active_license.deactivate()
            self.deactivate()
            if eventbus:
                eventbus.add_event(
                    LicenseDeactivatedEvent(
                        **await deactivated_license.to_dict()
                    )
                )
        self.statistics.append(stat_row)
        if eventbus:
            eventbus.add_event(
                StatisticRowAddedEvent(
                    **await stat_row.to_dict()
                )
            )

    @property
    def is_active(self) -> bool:
        return self.work_status == WorkStatus.ACTIVE

    @classmethod
    def make(
        cls, name: str, location: str, tenant_id: UUID
    ) -> Subdivision:
        return cls(
            id=uuid4(),
            name=name, location=location, tenant_id=tenant_id,
            licenses=[],
            statistics=[],
            work_status=WorkStatus.INACTIVE
        )

    @classmethod
    def make_from_persistence(
        cls, id: UUID, name: str, location: str, tenant_id: UUID,
        work_status: WorkStatus, link_to_subdivision_processing_domain: str,
        licenses: list, statistics: list
    ) -> Subdivision:
        return cls(
            id=id, name=name, location=location,
            tenant_id=tenant_id, work_status=work_status,
            link_to_subdivision_processing_domain=(
                link_to_subdivision_processing_domain
            ), licenses=licenses, statistics=statistics
        )
