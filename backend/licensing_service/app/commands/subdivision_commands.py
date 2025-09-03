from uuid import UUID
from datetime import datetime

# ---Core imports---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# ---Domain imports---
from ...domain.aggregates.subdivision import Subdivision
from ...domain.services.commands.subdivision_commands import (
    AddStatisticRowCommand,
    CreateSubdivisionCommand,
    UpdateSubdivisionCommand,
    DeleteSubdivisionCommand,
    ActivateSubdivisionLicenseCommand,
    DeactivateSubdivisionLicenseCommand
)
from ...domain.services.commands.license_commands import (
    CreateLicenseCommand, UpdateLicenseCommand, DeleteLicenseCommand
)


class SubdivisionCommandUseCase:

    def __init__(self, messagebus_handler: GlobalMessageBusHandler):
        self.messagebus_handler = messagebus_handler

    async def subdivision_add_stat_row(
        self,
        created: datetime,
        subdivision_id: UUID,
        count_requests: int
    ) -> Subdivision:
        command = AddStatisticRowCommand(
            created=created,
            subdivision_id=subdivision_id,
            count_requests=count_requests
        )
        await self.messagebus_handler.handle(
            message=command
        )
        return self.messagebus_handler.command_result

    async def active_subdivision_license(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            ActivateSubdivisionLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def deactive_subdivision_license(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            DeactivateSubdivisionLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def create_subdivision(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            CreateSubdivisionCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def update_subdivision(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            UpdateSubdivisionCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def delete_subdivision(self, id: UUID) -> Subdivision:
        await self.messagebus_handler.handle(DeleteSubdivisionCommand(id=id))
        return self.messagebus_handler.command_result

    async def subdivision_create_license(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            CreateLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def subdivision_update_license(self, **kwargs) -> Subdivision:
        await self.messagebus_handler.handle(
            UpdateLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result
