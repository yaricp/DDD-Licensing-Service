from ....domain.services.handlers.license_handlers import (
    LicenseCommandHandler
)
from ....domain.services.commands.license_commands import (
    CreateLicenseCommand, UpdateLicenseCommand, DeleteLicenseCommand
)
from ....domain.aggregates.entities.license import License

from ....app.services.license_services import (
    LicenseService
)
from ....app.services.subdivision_services import (
    SubdivisionService
)


class CreateLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: CreateLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        # licenses_service: LicenseService = LicenseService(
        #     domain_event_bus=self.domain_event_bus,
        #     infra_event_bus=self.infra_event_bus
        # )
        subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        print(f"await command.to_dict(): {await command.to_dict()}")
        # license_in: License = License(**await command.to_dict())
        license = await subdivision_service.add_license(
            add_license_command=command
        )
        return license


class UpdateLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: UpdateLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        licenses_service: LicenseService = LicenseService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        license_in: License = License(**await command.to_dict())
        license = await licenses_service.update_license(
            id=license_in.id, license=license_in
        )
        return license


class DeleteLicenseCommandHandler(LicenseCommandHandler):

    async def __call__(self, command: DeleteLicenseCommand) -> License:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        licenses_service: LicenseService = LicenseService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        license = await licenses_service.delete_license(id=command.id)
        return license
