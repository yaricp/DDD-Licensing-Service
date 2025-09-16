from ....app.services.license_services import LicenseService
from ....app.services.subdivision_services import SubdivisionService
from ....domain.aggregates.entities.license import License
from ....domain.services.commands.license_commands import (
    CreateLicenseCommand,
    DeleteLicenseCommand,
    UpdateLicenseCommand,
)
from ....domain.services.handlers.license_handlers import LicenseCommandHandler


class CreateLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: CreateLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        print(f"await command.to_dict(): {await command.to_dict()}")
        subdivision = await subdivision_service.add_license(add_license_command=command)
        return subdivision


class UpdateLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: UpdateLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        subdivision = await subdivision_service.update_license(
            update_license_command=command
        )
        return subdivision


class DeleteLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: DeleteLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        subdivision = await subdivision_service.delete_license(
            delete_license_command=command
        )
        return subdivision
