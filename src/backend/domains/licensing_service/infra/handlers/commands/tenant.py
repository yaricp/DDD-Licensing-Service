from ....app.services.tenant_services import TenantService
from ....domain.aggregates.tenant import Tenant
from ....domain.services.commands.tenant_commands import (
    CreateTenantCommand,
    DeleteTenantCommand,
    UpdateTenantCommand,
)
from ....domain.services.handlers.tenant_handlers import TenantCommandHandler


class CreateTenantCommandHandler(TenantCommandHandler):

    async def __call__(self, command: CreateTenantCommand) -> Tenant:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        tenant_service: TenantService = TenantService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        # tenant: Tenant = Tenant(**await command.to_dict())
        tenant = await tenant_service.create_tenant(create_command=command)
        return tenant


class UpdateTenantCommandHandler(TenantCommandHandler):

    async def __call__(self, command: UpdateTenantCommand) -> Tenant:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        tenant_service: TenantService = TenantService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        tenant = await tenant_service.update_tenant(update_command=command)
        return tenant


class DeleteTenantCommandHandler(TenantCommandHandler):

    async def __call__(self, command: DeleteTenantCommand) -> Tenant:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        tenant_service: TenantService = TenantService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        tenant = await tenant_service.delete_tenant(id=command.id)
        return tenant
