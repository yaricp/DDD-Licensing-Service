# tests/test_license.py

from datetime import datetime, timedelta
from uuid import uuid4

from backend.domains.licensing_service.domain.aggregates.entities.license import License
from backend.domains.licensing_service.domain.value_objects.license_status import (
    LicenseStatus,
)
from backend.domains.licensing_service.domain.value_objects.license_type import (
    LicenseType,
)


def test_make_creates_inactive_license():
    subdivision_id = uuid4()
    license = License.make(
        name="Test License",
        description="Test description",
        type=LicenseType.BYCOUNT,
        subdivision_id=subdivision_id,
        count_requests=10,
    )

    assert license.name == "Test License"
    assert license.description == "Test description"
    assert license.type == LicenseType.BYCOUNT
    assert license.subdivision_id == subdivision_id
    assert license.count_requests == 10
    assert license.status == LicenseStatus.INACTIVE
    assert license.activated is None
    assert license.expirated is None
    assert license.created is not None
    assert license.expiration > datetime.now()


def test_make_from_persistence_restores_license():
    now = datetime.now()
    license_id = uuid4()
    subdivision_id = uuid4()
    license = License.make_from_persistence(
        name="Persisted License",
        description="Persisted description",
        type=LicenseType.BYTIME,
        subdivision_id=subdivision_id,
        count_requests=5,
        id=license_id,
        status=LicenseStatus.ACTIVE,
        activated=now,
        expirated=None,
        created=now,
        expiration=now + timedelta(days=30),
    )

    assert license.id == license_id
    assert license.name == "Persisted License"
    assert license.status == LicenseStatus.ACTIVE
    assert license.activated == now
    assert license.expiration == now + timedelta(days=30)


def test_activate_and_deactivate():
    subdivision_id = uuid4()
    license = License.make(
        name="Test License",
        description="Test description",
        type=LicenseType.BYCOUNT,
        subdivision_id=subdivision_id,
        count_requests=10,
    )

    license.activate()
    assert license.status == LicenseStatus.ACTIVE
    assert license.activated is not None

    license.deactivate()
    assert license.status == LicenseStatus.INACTIVE
    assert license.expirated is not None


def test_check_by_count_deactivates_if_limit_reached():
    subdivision_id = uuid4()
    license = License.make(
        name="Count License",
        description="Count description",
        type=LicenseType.BYCOUNT,
        subdivision_id=subdivision_id,
        count_requests=5,
    )

    license.check(count_requests=10)
    assert license.status == LicenseStatus.INACTIVE
    assert license.expirated is not None


def test_check_by_time_deactivates_if_expired():
    subdivision_id = uuid4()
    past = datetime.now() - timedelta(days=1)
    license = License(
        name="Time License",
        description="Time description",
        type=LicenseType.BYTIME,
        subdivision_id=subdivision_id,
        count_requests=5,
        status=LicenseStatus.ACTIVE,
        expiration=past,
    )

    license.check(count_requests=0)
    assert license.status == LicenseStatus.INACTIVE
    assert license.expirated is not None
