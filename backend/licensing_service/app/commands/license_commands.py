from uuid import UUID
from typing import Optional

# ---Core imports---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# ---Domain imports---
from ...domain.aggregates.entities.license import License
from ...domain.services.commands.license_commands import (
    CreateLicenseCommand, UpdateLicenseCommand,
    DeleteLicenseCommand
)


class LicenseCommandUseCase:

    def __init__(self, messagebus_handler: GlobalMessageBusHandler):
        self.messagebus_handler = messagebus_handler

    async def create_license(self, **kwargs) -> Optional[License]:
        await self.messagebus_handler.handle(
            CreateLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def update_license(self, **kwargs) -> License:
        await self.messagebus_handler.handle(
            UpdateLicenseCommand(**kwargs)
        )
        return self.messagebus_handler.command_result

    async def delete_license(self, id: UUID) -> License:
        await self.messagebus_handler.handle(DeleteLicenseCommand(id=id))
        return self.messagebus_handler.command_result
