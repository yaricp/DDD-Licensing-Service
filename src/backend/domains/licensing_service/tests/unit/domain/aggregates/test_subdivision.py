import pytest
from uuid import uuid4

from backend.core.infra.eventbus import AbstractEventBus, AbstractEvent

from backend.domains.licensing_service.domain.aggregates.subdivision import Subdivision
from backend.domains.licensing_service.domain.aggregates.entities.license import License
from backend.domains.licensing_service.domain.aggregates.entities.stat_row import StatisticRow
from backend.domains.licensing_service.domain.value_objects.license_type import LicenseType
from backend.domains.licensing_service.domain.services.events.license_events import (
    LicenseActivatedEvent, LicenseDeactivatedEvent
)
from backend.domains.licensing_service.domain.services.events.statistic_row_events import (
    StatisticRowAddedEvent
)
from backend.domains.licensing_service.domain.value_objects.work_status import (
    WorkStatus
)
from backend.domains.licensing_service.domain.exceptions.license import (
    LicenseNotFoundError, LicenseInactiveError
)
from backend.domains.licensing_service.domain.exceptions.subdivision import (
    SubdivisionInactiveError
)
from backend.domains.licensing_service.domain.exceptions.statistic_row import (
    SubdivisionStatisticAlreadyExistsError
)


class FakeEventBus(AbstractEventBus):
    """Fake Event bus for tests"""
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)


@pytest.mark.asyncio
async def test_make_subdivision():
    """
    Test make subdivision
    """
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    assert subdivision.licenses == []
    assert subdivision.statistics == []
    assert subdivision.work_status == WorkStatus.INACTIVE


@pytest.mark.asyncio
async def test_update_subdivision():
    """
    Test update subdivision
    """
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    subdivision.update(
        name="Test Updated", location="Somewhere Updated",
        link_to_subdivision_processing_domain="Link Updated",
        work_status=WorkStatus.ACTIVE
    )
    assert subdivision.name == "Test Updated"
    assert subdivision.location == "Somewhere Updated"
    assert subdivision.link_to_subdivision_processing_domain == "Link Updated"
    assert subdivision.work_status == WorkStatus.ACTIVE


@pytest.mark.asyncio
async def test_add_license_subdivision():
    """
    Test add_license to subdivision
    """
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )

    assert subdivision.licenses[0] == license
    assert subdivision.licenses[0].id == license.id


@pytest.mark.asyncio
async def test_update_license_subdivision():
    """
    Test update_license in subdivision
    """
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )
    subdivision.update_license(
        id=license.id,
        name="TestLicense1 Updated",
        description="Test License1  Updated",
        type=LicenseType.BYCOUNT,
        count_requests=20
    )

    assert subdivision.licenses[0].name == "TestLicense1 Updated"
    assert subdivision.licenses[0].description == "Test License1  Updated"
    assert subdivision.licenses[0].type == LicenseType.BYCOUNT
    assert subdivision.licenses[0].count_requests == 20
    assert subdivision.licenses[0].id == license.id

    with pytest.raises(LicenseNotFoundError):
        subdivision.update_license(
            id=123456,
            name="TestLicense1 Updated",
            description="Test License1  Updated",
            type=LicenseType.BYCOUNT,
            count_requests=20
        )


@pytest.mark.asyncio
async def test_delete_license_subdivision():
    """
    Test delete_license in subdivision
    """
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )

    with pytest.raises(LicenseNotFoundError):
        subdivision.delete_license(id=123456)

    subdivision.delete_license(id=license.id)

    assert len(subdivision.licenses) == 0


@pytest.mark.asyncio
async def test_activate_license_subdivision():
    """
    Test activate_license in subdivision
    - create subdivision
    - add license
    - activate license
    - check if subdivision active
    """
    domain_event_bus = FakeEventBus()
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )
    with pytest.raises(LicenseNotFoundError):
        await subdivision.activate_license(
            license_id=100000, eventbus=domain_event_bus
        )
    await subdivision.activate_license(
        license_id=license.id, eventbus=domain_event_bus
    )

    assert subdivision.is_active
    assert isinstance(domain_event_bus.events[-1], LicenseActivatedEvent)


@pytest.mark.asyncio
async def test_deactivate_license_subdivision():
    """
    Test deactivate_license in subdivision
    - create subdivision
    - add license
    - activate license
    - deactivate license
    - check if subdivision active
    """
    domain_event_bus = FakeEventBus()
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )
    with pytest.raises(LicenseNotFoundError):
        await subdivision.activate_license(
            license_id=100000, eventbus=domain_event_bus
        )
    await subdivision.activate_license(
        license_id=license.id, eventbus=domain_event_bus
    )

    assert subdivision.is_active
    assert isinstance(domain_event_bus.events[-1], LicenseActivatedEvent)

    with pytest.raises(LicenseNotFoundError):
        await subdivision.deactivate_license(
            license_id=100000, eventbus=domain_event_bus
        )
    await subdivision.deactivate_license(
        license_id=license.id, eventbus=domain_event_bus
    )

    assert not subdivision.is_active
    assert isinstance(domain_event_bus.events[-1], LicenseDeactivatedEvent)


@pytest.mark.asyncio
async def test_save_day_statistic_subdivision():
    """
    Test save_day_statistic in subdivision
    - create subdivision
    - add statistic row
    - check if adding statistic row raise error
    - add license
    - activate license
    - add statistic row
    - check if adding statistic row raise error
    """
    domain_event_bus = FakeEventBus()
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    with pytest.raises(SubdivisionInactiveError):
        await subdivision.save_day_statistic(
            StatisticRow.make(
                count_requests=15, subdivision_id=subdivision.id
            ),
            eventbus=domain_event_bus
        )

    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=100
    )

    subdivision.activate()

    with pytest.raises(LicenseInactiveError):
        await subdivision.save_day_statistic(
            StatisticRow.make(
                count_requests=15, subdivision_id=subdivision.id
            ),
            eventbus=domain_event_bus
        )

    await subdivision.activate_license(
        license_id=license.id, eventbus=domain_event_bus
    )

    assert subdivision.is_active
    assert subdivision.licenses[0].is_active
    assert isinstance(domain_event_bus.events[-1], LicenseActivatedEvent)

    await subdivision.save_day_statistic(
        StatisticRow.make(
            count_requests=15, subdivision_id=subdivision.id
        ),
        eventbus=domain_event_bus
    )
    statistic_row = subdivision.statistics[0]

    assert subdivision.is_active

    assert isinstance(domain_event_bus.events[-1], StatisticRowAddedEvent)

    with pytest.raises(SubdivisionStatisticAlreadyExistsError):
        await subdivision.save_day_statistic(
            statistic_row, eventbus=domain_event_bus
        )


@pytest.mark.asyncio
async def test_license_deactivation_when_limit_reached():
    """
    Test for Subdivision
    - create subdivision
    - add license
    - activate license
    - add daily statictics row
    - check if subdivision active
    - check domain event bus
    """
    domain_event_bus = FakeEventBus()
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )

    license = subdivision.add_license(
        subdivision_id=subdivision.id,
        name="TestLicense1",
        description="Test License1 test123",
        type=LicenseType.BYCOUNT,
        count_requests=10
    )

    assert subdivision.licenses[0] == license
    assert subdivision.licenses[0].id == license.id

    await subdivision.activate_license(license.id, domain_event_bus)

    assert license.is_active
    assert isinstance(domain_event_bus.events[-1], LicenseActivatedEvent)

    await subdivision.save_day_statistic(
        StatisticRow.make(
            count_requests=15, subdivision_id=subdivision.id
        ),
        eventbus=domain_event_bus
    )

    assert not subdivision.is_active
    assert not license.is_active
    assert isinstance(domain_event_bus.events[-2], LicenseDeactivatedEvent)
    assert isinstance(domain_event_bus.events[-1], StatisticRowAddedEvent)
    assert len(domain_event_bus.events) == 3
