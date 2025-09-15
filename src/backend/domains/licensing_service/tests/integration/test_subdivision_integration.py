# tests/integration/test_tenant_service.py
from datetime import datetime
from uuid import uuid4

import pytest

from backend.core.infra.eventbus import AbstractEventBus
from backend.domains.licensing_service.app.services.subdivision_services import (
    SubdivisionService,
)
from backend.domains.licensing_service.app.services.tenant_services import TenantService
from backend.domains.licensing_service.domain.exceptions.license import (
    LicenseInactiveError,
)
from backend.domains.licensing_service.domain.exceptions.subdivision import (
    SubdivisionAlreadyExistsError,
    SubdivisionInactiveError,
    SubdivisionNotFoundError,
)
from backend.domains.licensing_service.domain.services.commands.license_commands import (
    CreateLicenseCommand,
    DeleteLicenseCommand,
    UpdateLicenseCommand,
)
from backend.domains.licensing_service.domain.services.commands.subdivision_commands import (
    AddStatisticRowCommand,
    CreateSubdivisionCommand,
    UpdateSubdivisionCommand,
)
from backend.domains.licensing_service.domain.services.commands.tenant_commands import (
    CreateTenantCommand,
)
from backend.domains.licensing_service.domain.services.events.license_events import (
    LicenseActivatedEvent,
    LicenseCreatedEvent,
)
from backend.domains.licensing_service.domain.services.events.statistic_row_events import (
    StatisticRowAddedEvent,
)
from backend.domains.licensing_service.domain.services.events.subdivision_events import (
    SubdivisionCreatedEvent,
    SubdivisionDeletedEvent,
    SubdivisionLicenseExpiredEvent,
    SubdivisionUpdatedEvent,
)
from backend.domains.licensing_service.domain.services.events.tenant_events import (
    TenantCreatedEvent,
)
from backend.domains.licensing_service.domain.value_objects.license_type import (
    LicenseType,
)
from backend.domains.licensing_service.domain.value_objects.work_status import (
    WorkStatus,
)


class MockEventBus(AbstractEventBus):
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)


@pytest.mark.asyncio
async def test_create_subdivision(db_session):
    """
    Integration test for SubdivisionService:
    - create tenant
    - create subdivision for created tenant
    - fetch subdivision by id
    - check event bus
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service_tenant = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789",
    )

    tenant = await service_tenant.create_tenant(create_cmd)

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateSubdivisionCommand(
        name="Subdivision 1", location="City 1", tenant_id=tenant.id
    )

    subdivision = await service.create_subdivision(create_cmd)

    assert subdivision.id is not None
    assert subdivision.name == "Subdivision 1"
    assert subdivision.tenant_id == tenant.id

    assert len(infra_event_bus.events) == 2
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert isinstance(infra_event_bus.events[1], SubdivisionCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 1"
    assert infra_event_bus.events[1].name == "Subdivision 1"

    fetched_subdivision = await service.get_subdivision_by_id(subdivision.id)
    assert fetched_subdivision.id == subdivision.id
    assert fetched_subdivision.name == "Subdivision 1"


@pytest.mark.asyncio
async def test_update_tenant(db_session):
    """
    Integration test for SubdivisionService:
    - create tenant
    - create subdivision for created tenant
    - fetch subdivision by id
    - update subdivision
    - check event bus
    """

    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 2",
        address="456 Main St",
        email="tenant2@example.com",
        phone="+987654321",
    )
    tenant = await service.create_tenant(create_cmd)

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateSubdivisionCommand(
        name="Subdivision 1", location="City 1", tenant_id=tenant.id
    )

    subdivision = await service.create_subdivision(create_cmd)

    update_cmd = UpdateSubdivisionCommand(
        id=subdivision.id,
        name="Subdivision 1 Updated",
        location="City 1 Updated",
        work_status=WorkStatus.ACTIVE,
        link_to_subdivision_processing_domain="Updated link",
    )

    updated_subdivision = await service.update_subdivision(update_cmd)
    assert updated_subdivision.name == "Subdivision 1 Updated"
    assert updated_subdivision.location == "City 1 Updated"
    assert updated_subdivision.work_status == WorkStatus.ACTIVE

    assert len(infra_event_bus.events) == 3
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 2"
    assert infra_event_bus.events[0].address == "456 Main St"
    assert isinstance(infra_event_bus.events[1], SubdivisionCreatedEvent)
    assert infra_event_bus.events[1].name == "Subdivision 1"
    assert infra_event_bus.events[1].location == "City 1"
    assert isinstance(infra_event_bus.events[2], SubdivisionUpdatedEvent)
    assert infra_event_bus.events[2].name == "Subdivision 1 Updated"
    assert infra_event_bus.events[2].location == "City 1 Updated"


@pytest.mark.asyncio
async def test_get_all_tenants(db_session):
    """
    Integration test for SubdivisionService:
    - create tenant
    - create numbers of subdivision for created tenant
    - get all subdivisions
    - check names of all subdivisions
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789",
    )
    tenant = await tenant_service.create_tenant(create_cmd)
    count = 5
    for i in range(count):
        create_cmd = CreateSubdivisionCommand(
            name=f"Subdivision {i}", location=f"City {i}", tenant_id=tenant.id
        )
        await subdivision_service.create_subdivision(create_cmd)

    assert len(infra_event_bus.events) == count + 1
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 1"
    assert isinstance(infra_event_bus.events[1], SubdivisionCreatedEvent)
    assert infra_event_bus.events[1].name == "Subdivision 0"

    fetched_subdivisions = await subdivision_service.get_all_subdivisions()
    assert len(fetched_subdivisions) == count
    fetched_subdivisions.sort(key=lambda x: x.name)
    for i in range(count):
        assert fetched_subdivisions[i].name == f"Subdivision {i}"


@pytest.mark.asyncio
async def test_delete_tenant(db_session):
    """
    Integration test for SubdivisionService:
    - create tenant
    - create subdivision for created tenant
    - delete created subdivision
    - check if subdivision doesn't exists
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789",
    )

    tenant = await tenant_service.create_tenant(create_cmd)

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    create_cmd = CreateSubdivisionCommand(
        name="Subdivision 1", location="City 1", tenant_id=tenant.id
    )

    sundivision = await service.create_subdivision(create_cmd)

    assert len(infra_event_bus.events) == 2
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 1"
    assert isinstance(infra_event_bus.events[1], SubdivisionCreatedEvent)
    assert infra_event_bus.events[1].name == "Subdivision 1"

    deleted_sundivision = await service.delete_subdivision(sundivision.id)
    assert deleted_sundivision.id == sundivision.id
    assert deleted_sundivision.name == "Subdivision 1"

    assert len(infra_event_bus.events) == 3
    assert isinstance(infra_event_bus.events[2], SubdivisionDeletedEvent)
    assert infra_event_bus.events[2].name == "Subdivision 1"

    with pytest.raises(SubdivisionNotFoundError) as exc_info:
        await service.get_subdivision_by_id(tenant.id)
    assert str(exc_info.value) == "404: Subdivision with provided credentials not found"


@pytest.mark.asyncio
async def test_subdivision_not_found_error(db_session):
    """
    Test error handling when trying to get non-existent subdivision
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )

    non_existent_id = uuid4()

    with pytest.raises(SubdivisionNotFoundError) as exc_info:
        await service.get_subdivision_by_id(non_existent_id)

    assert str(exc_info.value) == "404: Subdivision with provided credentials not found"


@pytest.mark.asyncio
async def test_add_license_to_subdivision(db_session):
    """
    Integration test for adding license to subdivision:
    - create tenant and subdivision
    - add license to subdivision
    - verify license was added
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Create tenant
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="License Test Tenant",
        address="123 License St",
        email="license@example.com",
        phone="+111111111",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    # Create subdivision
    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="License Test Subdivision", location="License City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add license
    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=100,
        name="Test License",
        description="Test License Description",
        subdivision_id=subdivision.id,
    )

    updated_subdivision = await subdivision_service.add_license(license_cmd)

    assert updated_subdivision is not None
    assert len(updated_subdivision.licenses) == 1
    assert updated_subdivision.licenses[0].name == "Test License"
    assert updated_subdivision.licenses[0].description == "Test License Description"


@pytest.mark.asyncio
async def test_update_license_in_subdivision(db_session):
    """
    Integration test for updating license in subdivision:
    - create tenant, subdivision and license
    - update license
    - verify license was updated
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup tenant and subdivision with license
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Update License Tenant",
        address="456 Update St",
        email="update@example.com",
        phone="+222222222",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Update License Subdivision", location="Update City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add initial license
    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=100,
        name="Initial License",
        description="Initial Description",
        subdivision_id=subdivision.id,
    )
    subdivision_with_license = await subdivision_service.add_license(license_cmd)
    license_id = subdivision_with_license.licenses[0].id

    # Update license
    update_license_cmd = UpdateLicenseCommand(
        id=license_id,
        name="Updated License",
        description="Updated Description",
        subdivision_id=subdivision.id,
    )

    updated_subdivision = await subdivision_service.update_license(
        update_license_cmd
    )

    assert updated_subdivision is not None
    assert len(updated_subdivision.licenses) == 1
    assert updated_subdivision.licenses[0].name == "Updated License"
    assert updated_subdivision.licenses[0].description == "Updated Description"


@pytest.mark.asyncio
async def test_delete_license_from_subdivision(db_session):
    """
    Integration test for deleting license from subdivision:
    - create tenant, subdivision and license
    - delete license
    - verify license was removed
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Delete License Tenant",
        address="789 Delete St",
        email="delete@example.com",
        phone="+333333333",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Delete License Subdivision", location="Delete City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add license to delete
    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=100,
        name="License to Delete",
        description="Will be deleted",
        subdivision_id=subdivision.id,
    )
    subdivision_with_license = await subdivision_service.add_license(license_cmd)
    license_id = subdivision_with_license.licenses[0].id

    # Delete license
    delete_license_cmd = DeleteLicenseCommand(
        id=license_id, subdivision_id=subdivision.id
    )

    updated_subdivision = await subdivision_service.delete_license(delete_license_cmd)

    assert updated_subdivision is not None
    assert len(updated_subdivision.licenses) == 0


@pytest.mark.asyncio
async def test_activate_subdivision_license(db_session):
    """
    Integration test for activating subdivision license:
    - create tenant, subdivision and license
    - activate license
    - verify license is activated
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Activate License Tenant",
        address="101 Activate St",
        email="activate@example.com",
        phone="+444444444",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Activate License Subdivision",
        location="Activate City",
        tenant_id=tenant.id,
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add license
    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=50,
        name="License to Activate",
        description="Will be activated",
        subdivision_id=subdivision.id,
    )
    subdivision_with_license = await subdivision_service.add_license(license_cmd)
    license_id = subdivision_with_license.licenses[0].id

    # Activate license
    activated_subdivision = await subdivision_service.activate_subdivision_license(
        subdivision_id=subdivision.id, license_id=license_id
    )

    assert activated_subdivision is not None
    # Здесь нужно будет проверить статус лицензии в зависимости от реализации


@pytest.mark.asyncio
async def test_deactivate_subdivision_license(db_session):
    """
    Integration test for deactivating subdivision license:
    - create tenant, subdivision and license
    - activate then deactivate license
    - verify license is deactivated
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Deactivate License Tenant",
        address="202 Deactivate St",
        email="deactivate@example.com",
        phone="+555555555",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Deactivate License Subdivision",
        location="Deactivate City",
        tenant_id=tenant.id,
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add and activate license
    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=50,
        name="License to Deactivate",
        description="Will be deactivated",
        subdivision_id=subdivision.id,
    )
    subdivision_with_license = await subdivision_service.add_license(license_cmd)
    license_id = subdivision_with_license.licenses[0].id

    await subdivision_service.activate_subdivision_license(
        subdivision_id=subdivision.id, license_id=license_id
    )

    # Deactivate license
    deactivated_subdivision = await subdivision_service.deactivate_subdivision_license(
        subdivision_id=subdivision.id, license_id=license_id
    )

    assert deactivated_subdivision is not None


@pytest.mark.asyncio
async def test_add_statistic_row_to_subdivision_without_license(db_session):
    """
    Integration test for adding statistic row to subdivision:
    - create tenant and subdivision
    - add statistic row
    - verify statistics and events
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Stats Tenant",
        address="303 Stats St",
        email="stats@example.com",
        phone="+666666666",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Stats Subdivision", location="Stats City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Add statistic row
    stats_cmd = AddStatisticRowCommand(
        created=datetime.now(), count_requests=100, subdivision_id=subdivision.id
    )
    with pytest.raises(SubdivisionInactiveError):
        await subdivision_service.add_subdivision_statistic_row(stats_cmd)

    # assert updated_subdivision is not None
    # assert len(updated_subdivision.statistics) == 1
    # assert updated_subdivision.statistics[0].count_requests == 100

    # # Check events
    # assert len(infra_event_bus.events) == 3  # TenantCreated + SubdivisionCreated + StatisticRowAdded
    # assert isinstance(infra_event_bus.events[2], StatisticRowAddedEvent)


@pytest.mark.asyncio
async def test_subdivision_operations_with_nonexistent_subdivision_id(db_session):
    """
    Test error handling when performing operations on non-existent subdivision
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )

    non_existent_id = uuid4()
    count_requests = 50
    license_cmd = CreateLicenseCommand(
        name="Test License",
        description="Test Description",
        type=LicenseType.BYCOUNT,
        count_requests=count_requests,
        subdivision_id=non_existent_id,
    )

    with pytest.raises(SubdivisionNotFoundError):
        await service.add_license(license_cmd)

    # Test statistic operations
    stats_cmd = AddStatisticRowCommand(
        created=datetime.now(),
        count_requests=count_requests,
        subdivision_id=non_existent_id,
    )

    with pytest.raises(SubdivisionNotFoundError):
        await service.add_subdivision_statistic_row(stats_cmd)


@pytest.mark.asyncio
async def test_update_subdivision_with_all_fields(db_session):
    """
    Test updating subdivision with all possible fields
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Full Update Tenant",
        address="404 Full St",
        email="full@example.com",
        phone="+777777777",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Original Subdivision", location="Original City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    # Update with all fields
    update_cmd = UpdateSubdivisionCommand(
        id=subdivision.id,
        name="Completely Updated Subdivision",
        location="New Amazing City",
        work_status=WorkStatus.INACTIVE,
        link_to_subdivision_processing_domain="https://new-link.example.com",
    )

    updated_subdivision = await subdivision_service.update_subdivision(update_cmd)

    assert updated_subdivision.name == "Completely Updated Subdivision"
    assert updated_subdivision.location == "New Amazing City"
    assert updated_subdivision.work_status == WorkStatus.INACTIVE
    assert (
        updated_subdivision.link_to_subdivision_processing_domain
        == "https://new-link.example.com"
    )

    # Verify event was published
    update_events = [
        e for e in infra_event_bus.events if isinstance(e, SubdivisionUpdatedEvent)
    ]
    assert len(update_events) == 1
    assert update_events[0].name == "Completely Updated Subdivision"


@pytest.mark.asyncio
async def test_empty_subdivisions_list(db_session):
    """
    Test getting all subdivisions when no subdivisions exist
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )

    subdivisions = await service.get_all_subdivisions()
    assert subdivisions == []


@pytest.mark.asyncio
async def test_add_statistic_row_to_subdivision_with_license(db_session):
    """
    Integration test for adding statistic row to subdivision:
    - create tenant and subdivision
    - create license
    - add license to the subdivision
    - activate the license
    - add statistic row to the subdivision
    - verify statistics and events
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Stats Tenant",
        address="303 Stats St",
        email="stats@example.com",
        phone="+666666666",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    assert isinstance(infra_event_bus.events[-1], TenantCreatedEvent)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Stats Subdivision", location="Stats City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    assert isinstance(infra_event_bus.events[-1], SubdivisionCreatedEvent)

    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=100,
        name="Test License",
        description="Test License Description",
        subdivision_id=subdivision.id,
    )

    updated_subdivision = await subdivision_service.add_license(license_cmd)

    assert updated_subdivision is not None
    assert len(updated_subdivision.licenses) == 1
    assert isinstance(infra_event_bus.events[-1], LicenseCreatedEvent)

    license = updated_subdivision.licenses[0]

    activated_subdivision = await subdivision_service.activate_subdivision_license(
        subdivision_id=subdivision.id, license_id=license.id
    )

    assert activated_subdivision is not None
    assert isinstance(infra_event_bus.events[-1], LicenseActivatedEvent)

    # Add statistic row
    stats_cmd = AddStatisticRowCommand(
        created=datetime.now(), count_requests=50, subdivision_id=subdivision.id
    )
    stat_added_subdivision = await subdivision_service.add_subdivision_statistic_row(
        stats_cmd
    )

    assert stat_added_subdivision is not None
    assert len(stat_added_subdivision.statistics) == 1
    assert stat_added_subdivision.statistics[0].count_requests == 50

    # Check events
    print(infra_event_bus.events)
    assert len(infra_event_bus.events) == 5
    assert isinstance(infra_event_bus.events[-1], StatisticRowAddedEvent)


@pytest.mark.asyncio
async def test_add_statistic_row_deactivate_subdivision(db_session):
    """
    Integration test for adding statistic rows to subdivision more then
    count_requests in a license:
    - create tenant and subdivision
    - create license
    - add license to the subdivision
    - activate the license
    - add statistic rows to the subdivision
    - verify statistics and events
    - verify is subdivision deactived
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    # Setup
    tenant_service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    tenant_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Stats Tenant",
        address="303 Stats St",
        email="stats@example.com",
        phone="+666666666",
    )
    tenant = await tenant_service.create_tenant(tenant_cmd)

    subdivision_service = SubdivisionService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session,
    )
    subdivision_cmd = CreateSubdivisionCommand(
        name="Stats Subdivision", location="Stats City", tenant_id=tenant.id
    )
    subdivision = await subdivision_service.create_subdivision(subdivision_cmd)

    license_cmd = CreateLicenseCommand(
        type=LicenseType.BYCOUNT,
        count_requests=100,
        name="Test License",
        description="Test License Description",
        subdivision_id=subdivision.id,
    )

    updated_subdivision = await subdivision_service.add_license(license_cmd)

    assert updated_subdivision is not None
    assert len(updated_subdivision.licenses) == 1
    assert isinstance(infra_event_bus.events[-1], LicenseCreatedEvent)

    license = updated_subdivision.licenses[0]

    activated_subdivision = await subdivision_service.activate_subdivision_license(
        subdivision_id=subdivision.id, license_id=license.id
    )

    assert activated_subdivision is not None
    assert isinstance(infra_event_bus.events[-1], LicenseActivatedEvent)

    assert activated_subdivision.is_active

    # Add statistic rows
    stats_cmd = AddStatisticRowCommand(
        created=datetime.now(), count_requests=50, subdivision_id=subdivision.id
    )
    stat_added_subdivision = await subdivision_service.add_subdivision_statistic_row(
        stats_cmd
    )

    assert stat_added_subdivision.is_active
    assert isinstance(infra_event_bus.events[-1], StatisticRowAddedEvent)

    stats_cmd = AddStatisticRowCommand(
        created=datetime.now(), count_requests=51, subdivision_id=subdivision.id
    )
    stat_added_subdivision = await subdivision_service.add_subdivision_statistic_row(
        stats_cmd
    )

    assert stat_added_subdivision is not None
    assert len(stat_added_subdivision.statistics) == 2
    assert stat_added_subdivision.statistics[0].count_requests == 50
    assert stat_added_subdivision.statistics[1].count_requests == 51

    # Check events
    assert len(infra_event_bus.events) == 7
    assert isinstance(infra_event_bus.events[-2], StatisticRowAddedEvent)
    assert isinstance(infra_event_bus.events[-1], SubdivisionLicenseExpiredEvent)

    assert not stat_added_subdivision.is_active
