from uuid import UUID

# ---Core imports---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# ---Domain imports---
from ...domain.aggregates.tenant import Tenant
from ...domain.services.commands.tenant_commands import (
    CreateTenantCommand, UpdateTenantCommand,
    DeleteTenantCommand
)


class TenantCommandUseCase:

    def __init__(self, messagebus_handler: GlobalMessageBusHandler):
        self.messagebus_handler = messagebus_handler

    async def create_tenant(self, **kwargs) -> Tenant:
        await self.messagebus_handler.handle(
            CreateTenantCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def update_tenant(self, **kwargs) -> Tenant:
        del kwargs["users"]
        del kwargs["subdivisions"]
        await self.messagebus_handler.handle(
            UpdateTenantCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def delete_tenant(self, id: UUID) -> Tenant:
        await self.messagebus_handler.handle(DeleteTenantCommand(id=id))
        return self.messagebus_handler.command_result
