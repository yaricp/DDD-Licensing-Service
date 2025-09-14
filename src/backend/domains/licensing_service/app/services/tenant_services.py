from uuid import UUID
from typing import Optional, List, Any

# ---Domain imports---
from ...domain.aggregates.tenant import Tenant
from ...domain.aggregates.entities.user import User
from ...domain.services.domain_event_bus import DomainEventBus
from ...domain.services.events.tenant_events import (
    TenantCreatedEvent, TenantUpdatedEvent, TenantDeletedEvent
)
from ...domain.services.commands.tenant_commands import (
    CreateTenantCommand, UpdateTenantCommand
)
from ...domain.services.commands.user_commands import CreateUserCommand
from ...domain.services.uow.tenant_uow import TenantUnitOfWork
from ...domain.exceptions.tenant import TenantNotFoundError


# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.tenant_uow import (
    SQLAlchemyTenantUnitOfWork as UOW
)


class TenantService:
    """
    Service layer core according to DDD,
    which using a unit of work, will perform operations
    on the domain model.
    """

    def __init__(
        self,
        domain_event_bus: DomainEventBus | None = None,
        infra_event_bus: DomainEventBus | None = None,
        db_session_factory: Any | None = None
    ) -> None:
        self._domain_event_bus = domain_event_bus
        self._infra_event_bus = infra_event_bus
        if db_session_factory:
            self._uow: TenantUnitOfWork = UOW(
                session_factory=db_session_factory
            )
        else:
            self._uow: TenantUnitOfWork = UOW()

    async def create_tenant(
        self, create_command: CreateTenantCommand
    ) -> Optional[Tenant]:
        async with self._uow as uow:
            tenant = Tenant.make(
                user_id=create_command.user_id,
                name=create_command.name, email=create_command.email,
                address=create_command.address, phone=create_command.phone
            )
            created_tenant = await uow.tenants.save(
                tenant=tenant
            )
            await uow.commit()
            tenant = await self.get_tenant_by_id(
                id=created_tenant.id
            )
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    TenantCreatedEvent(
                        id=tenant.id,
                        name=tenant.name,
                        address=tenant.address,
                        email=tenant.email,
                        phone=tenant.phone
                    )
                )
            return tenant

    async def get_all_tenants(self) -> List[Tenant]:
        async with self._uow as uow:
            tenants: List[Tenant] = await uow.tenants.list()
            return tenants

    async def get_tenant_by_id(self, id: UUID | None) -> Tenant:
        async with self._uow as uow:
            tenant: Optional[Tenant] = await uow.tenants.get(id=id)
            if not tenant:
                raise TenantNotFoundError
            return tenant

    async def update_tenant(
        self, update_command: UpdateTenantCommand
    ) -> Tenant:
        async with self._uow as uow:
            tenant = await self.get_tenant_by_id(update_command.id)
            if not tenant:
                raise TenantNotFoundError
            tenant.update(
                update_command.name, update_command.address, 
                update_command.email, update_command.phone
            )
            tenant: Tenant = await uow.tenants.update(
                id=tenant.id, model=tenant
            )
            await uow.commit()
            event = TenantUpdatedEvent(
                id=tenant.id,
                name=tenant.name,
                address=tenant.address,
                email=tenant.email,
                phone=tenant.phone
            )
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            return tenant

    async def delete_tenant(self, id: UUID) -> Tenant:
        async with self._uow as uow:
            tenant: Tenant = await uow.tenants.delete(id=id)
            await uow.commit()
            if not tenant:
                raise TenantNotFoundError
            event = TenantDeletedEvent(
                id=tenant.id,
                name=tenant.name,
                address=tenant.address,
                email=tenant.email,
                phone=tenant.phone
            )
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            return tenant

    async def update_list_all_active_licenses(self, license) -> None:
        print("Update list all active license in tenant entity")
        print(f"Update license: {license}")
        # async with self._uow as uow:
        #     tenant = await uow.tenants.get(
        #         id=license.tenant_id
        #     )
        #     tenant.update_list_all_active_licenses(
        #         license, self._domain_event_bus
        #     )
        #     await uow.commit()
