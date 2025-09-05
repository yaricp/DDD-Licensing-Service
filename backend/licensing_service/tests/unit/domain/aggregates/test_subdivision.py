from uuid import uuid4

from backend.core.infra.eventbus import AbstractEventBus, AbstractEvent

from backend.licensing_service.domain.aggregates.subdivision import Subdivision
from backend.licensing_service.domain.aggregates.entities.license import License
from backend.licensing_service.domain.aggregates.entities.stat_row import StatisticRow
from backend.licensing_service.domain.value_objects.license_type import LicenseType


class FakeEventBus(AbstractEventBus):
    """Fake Event bus for tests"""
    def add_event(self, event: AbstractEvent):
        print(f"Event addded: {event}")


def test_license_deactivation_when_limit_reached():
    subdivision = Subdivision.make(
        name="Test",
        location="Somewhere",
        tenant_id=uuid4()
    )
    license = License.make(
        count_requests=10,
        name="TestLicense1",
        type=LicenseType.BYCOUNT,
        subdivision_id=subdivision.id,
        description="Test License1 test123"
    )
    subdivision.activate_license(license, FakeEventBus())

    subdivision.save_day_statistic(
        StatisticRow.make(
            count_requests=15, subdivision_id=subdivision.id
        ),
        eventbus=FakeEventBus()
    )

    assert not subdivision.is_active
    assert not license.is_active
