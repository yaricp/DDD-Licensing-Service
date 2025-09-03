from __future__ import annotations
from uuid import UUID
from typing import List, Optional
from dataclasses import dataclass, field

from backend.core.domain.aggregate import AbstractAggregateRoot
from backend.core.infra.eventbus import AbstractEventBus

from .entities.license import License
from .entities.stat_row import StatisticRow
from ..exceptions.subdivision import SubdivisionInactiveError
from ..exceptions.license import (
    LicenseExpiredError, LicenseInactiveError, LicenseAlreadyInUseError,
    LicenseWrongTenantError
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


@dataclass(eq=False, slots=True)
class Subdivision(AbstractAggregateRoot):
    name: str
    location: str
    tenant_id: UUID
    link_to_subdivision_processing_domain: Optional[str] = ""
    work_status: WorkStatus = WorkStatus.ACTIVE
    id: Optional[UUID] = None
    _domain_events: List[object] = field(
        default_factory=list, repr=False
    )
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
            subdivision_id=self.id, count_requests=count_requests
        )
        self.licenses.append(new_license)

    def update_license(
        self, name: str, description: str
    ) -> License:
        filtered_licenses = list(filter(
            lambda x: x.id == id, self.licenses
        ))
        if not filtered_licenses:
            raise LicenseWrongTenantError

        new_license = filtered_licenses[0]
        new_license.name = name
        new_license.description = description

    def delete_license(self, id: UUID) -> License:
        filtered_licenses: List[License] = list(filter(
            lambda x: x.id == id, self.licenses
        ))
        if not filtered_licenses:
            raise LicenseWrongTenantError
        current_license = filtered_licenses[0]
        if current_license.is_active:
            current_license.deactivate()
            self.deactivate()
        self.licenses.remove(current_license)

    def pull_events(self) -> List[object]:
        events = self._domain_events
        self._domain_events = []
        return events

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
        self, license_id: UUID, eventbus: AbstractEventBus
    ) -> None:
        print("activate_license started")
        filtered_license: Optional[License] = list(filter(
            lambda x: x.id == license_id,
            self.licenses
        ))
        if not filtered_license:
            raise FileNotFoundError
        license = filtered_license[0]
        license.activate()
        license.check(self.total_count_requests)
        if license.is_active:
            self.activate()
        eventbus.add_event(
            LicenseActivatedEvent(
                **await license.to_dict()
            )
        )

    async def deactivate_license(
        self, license_id: UUID, eventbus: AbstractEventBus
    ) -> None:
        print("deactivate_license started")
        filtered_license: Optional[License] = list(filter(
            lambda x: x.id == license_id,
            self.licenses
        ))
        if not filtered_license:
            raise FileNotFoundError
        license = filtered_license[0]
        license.deactivate()
        self.deactivate()
        eventbus.add_event(
            LicenseDeactivatedEvent(
                **await license.to_dict()
            )
        )

    def save_day_statistic(self, stat_row: StatisticRow):
        print(f"stat_row: {stat_row}")
        if not self.active_license:
            raise LicenseInactiveError
        if not self.is_active:
            raise SubdivisionInactiveError
        if stat_row in self.statistics:
            raise SubdivisionStatisticAlreadyExistsError
        print(f"type(stat_row): {type(stat_row)}")
        if (
            stat_row.count_requests + self.total_count_requests
        ) >= self.active_license.count_requests:
            # self.domain_buss.event(SaveStatRowCommand)
            self.deactivate_license()
        self.statistics.append(stat_row)

    @property
    def is_active(self) -> bool:
        return self.work_status == WorkStatus.ACTIVE

    @classmethod
    def make(
        cls, name: str, location: str, tenant_id: UUID
    ) -> Subdivision:
        print("Make a new aggregate")
        return cls(
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
        print("from DB")
        return cls(
            id=id, name=name, location=location,
            tenant_id=tenant_id, work_status=work_status,
            link_to_subdivision_processing_domain=(
                link_to_subdivision_processing_domain
            ), licenses=licenses, statistics=statistics,
            _domain_events=[]
        )
