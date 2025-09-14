# tests/integration/test_tenant_service.py
import pytest
from uuid import uuid4

from backend.domains.licensing_service.domain.aggregates.tenant import Tenant
from backend.domains.licensing_service.domain.services.commands.tenant_commands import (
    CreateTenantCommand, UpdateTenantCommand
)
from backend.domains.licensing_service.domain.services.events.tenant_events import (
    TenantCreatedEvent
)
from backend.domains.licensing_service.app.services.tenant_services import TenantService


# фикстура для моканого event bus
class MockEventBus:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)


@pytest.mark.asyncio
async def test_create_and_get_tenant(async_session):
    """
    Integration test for TenantService:
    - create tenant
    - fetch tenant by id
    - check event bus
    """
    event_bus = MockEventBus()
    service = TenantService(
        domain_event_bus=event_bus, infra_event_bus=event_bus,
        db_session_factory=async_session
    )

    # Команда для создания Tenant
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="+123456789"
    )

    # Создаем tenant через сервис
    tenant = await service.create_tenant(create_cmd)

    assert tenant.id is not None
    assert tenant.name == "Tenant 1"
    assert len(tenant.users) == 1

    # Проверяем, что событие создалось
    assert len(event_bus.events) == 1
    assert isinstance(event_bus.events[0], TenantCreatedEvent)
    assert event_bus.events[0].name == "Tenant 1"

    # Получаем tenant по id через сервис
    fetched_tenant = await service.get_tenant_by_id(tenant.id)
    assert fetched_tenant.id == tenant.id
    assert fetched_tenant.name == "Tenant 1"


@pytest.mark.asyncio
async def test_update_tenant(async_session):
    event_bus = MockEventBus()
    service = TenantService(
        domain_event_bus=event_bus, infra_event_bus=event_bus,
        db_session_factory=async_session
    )

    # Сначала создаем tenant
    create_cmd = CreateTenantCommand(
        user_id=uuid4(),
        name="Tenant 2",
        address="456 Main St",
        email="tenant2@example.com",
        phone="+987654321"
    )
    tenant = await service.create_tenant(create_cmd)

    # Обновляем tenant
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
