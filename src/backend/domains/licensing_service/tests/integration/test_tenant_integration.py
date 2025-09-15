# tests/integration/test_tenant_service.py
import pytest
from uuid import uuid4

from  backend.core.infra.eventbus import AbstractEventBus
from backend.domains.licensing_service.domain.services.commands.tenant_commands import (
    CreateTenantCommand, UpdateTenantCommand
)
from backend.domains.licensing_service.domain.services.events.tenant_events import (
    TenantCreatedEvent, TenantUpdatedEvent, TenantDeletedEvent
)
from backend.domains.licensing_service.app.services.tenant_services import TenantService
from backend.domains.licensing_service.domain.exceptions.tenant import TenantNotFoundError


class MockEventBus(AbstractEventBus):
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)


@pytest.mark.asyncio
async def test_create_and_get_tenant(db_session):
    """
    Integration test for TenantService:
    - create tenant
    - fetch tenant by id
    - check event bus
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789"
    )

    tenant = await service.create_tenant(create_cmd)

    assert tenant.id is not None
    assert tenant.name == "Tenant 1"
    assert len(tenant.users) == 1

    assert len(infra_event_bus.events) == 1
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 1"

    fetched_tenant = await service.get_tenant_by_id(tenant.id)
    assert fetched_tenant.id == tenant.id
    assert fetched_tenant.name == "Tenant 1"


@pytest.mark.asyncio
async def test_update_tenant(db_session):
    """Test updating tenant on app layer"""

    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 2",
        address="456 Main St",
        email="tenant2@example.com",
        phone="+987654321"
    )
    tenant = await service.create_tenant(create_cmd)

    update_cmd = UpdateTenantCommand(
        id=tenant.id,
        name="Tenant 2 Updated",
        address="789 Main St",
        email="updated2@example.com",
        phone="+1122334455"
    )

    updated_tenant = await service.update_tenant(update_cmd)
    assert updated_tenant.name == "Tenant 2 Updated"
    assert updated_tenant.address == "789 Main St"
    assert updated_tenant.email == "updated2@example.com"

    assert len(infra_event_bus.events) == 2
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 2"
    assert infra_event_bus.events[0].address == "456 Main St"
    assert isinstance(infra_event_bus.events[1], TenantUpdatedEvent)
    assert infra_event_bus.events[1].name == "Tenant 2 Updated"
    assert infra_event_bus.events[1].address == "789 Main St"


@pytest.mark.asyncio
async def test_get_all_tenants(db_session):
    """
    Test use case for get all tenants on app layer
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session
    )
    count = 5
    for i in range(count):
        create_cmd = CreateTenantCommand(
            user_id=uuid4(),
            name=f"Tenant {i}",
            address=f"123 Main St{i}",
            email=f"tenant{i}@example.com",
            phone=f"+123456789{i}"
        )

        await service.create_tenant(create_cmd)

    assert len(infra_event_bus.events) == count
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 0"

    fetched_tenants = await service.get_all_tenants()
    assert len(fetched_tenants) == count
    fetched_tenants.sort(key=lambda x: x.name)
    for i in range(count):
        assert fetched_tenants[i].name == f"Tenant {i}"


@pytest.mark.asyncio
async def test_delete_tenant(db_session):
    """
    Integration test for TenantService:
    - create tenant
    - delete tenant
    - check if the tenant doesn't exists
    """
    infra_event_bus = MockEventBus()
    domain_event_bus = MockEventBus()

    service = TenantService(
        domain_event_bus=domain_event_bus,
        infra_event_bus=infra_event_bus,
        db_session_factory=db_session
    )
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789"
    )

    tenant = await service.create_tenant(create_cmd)

    assert tenant.id is not None
    assert tenant.name == "Tenant 1"
    assert len(tenant.users) == 1

    assert len(infra_event_bus.events) == 1
    assert isinstance(infra_event_bus.events[0], TenantCreatedEvent)
    assert infra_event_bus.events[0].name == "Tenant 1"

    deleted_tenant = await service.delete_tenant(tenant.id)
    assert deleted_tenant.id == tenant.id
    assert deleted_tenant.name == "Tenant 1"

    with pytest.raises(TenantNotFoundError) as exc_info:
        await service.get_tenant_by_id(tenant.id)
    assert str(exc_info.value) == "404: Tenant with provided credentials not found"
