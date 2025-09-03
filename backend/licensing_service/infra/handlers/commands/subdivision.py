from ....domain.services.handlers.subdivision_handlers import (
    SubdivisionCommandHandler
)

from ....domain.services.commands.subdivision_commands import (
    ActivateSubdivisionLicenseCommand, AddStatisticRowCommand,
    CreateSubdivisionCommand, UpdateSubdivisionCommand, 
    DeleteSubdivisionCommand, DeactivateSubdivisionLicenseCommand
)

from ....domain.aggregates.subdivision import Subdivision

from ....app.services.subdivision_services import (
    SubdivisionService
)


class ActivateSubdivisionLicenseCommandHandler(SubdivisionCommandHandler):

    async def __call__(
        self, command: ActivateSubdivisionLicenseCommand
    ) -> Subdivision:
        """
        Handle ActivateSubdivisionLicenseCommand
        """
        service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )

        subdivision = await service.activate_subdivision_license(
            **await command.to_dict()
        )
        return subdivision


class DeactivateSubdivisionLicenseCommandHandler(SubdivisionCommandHandler):

    async def __call__(
        self, command: DeactivateSubdivisionLicenseCommand
    ) -> Subdivision:
        """
        Handle DeactivateSubdivisionLicenseCommand
        """
        service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )

        subdivision = await service.deactivate_subdivision_license(
            **await command.to_dict()
        )
        return subdivision


class AddStaticticRowSubdivisionCommandHandler(SubdivisionCommandHandler):
    async def __call__(
        self, command: AddStatisticRowCommand
    ) -> Subdivision:
        """
        AddStaticticRowSubdivisionCommandHandler
        """
        service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        subdivision = await service.add_subdivision_statistic_row(
            new_stats_command=command
        )
        return subdivision


class CreateSubdivisionCommandHandler(SubdivisionCommandHandler):

    async def __call__(
        self, command: CreateSubdivisionCommand
    ) -> Subdivision:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """

        Subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        # item_in: Subdivision = Subdivision(**await command.to_dict())
        subdivision = await Subdivision_service.create_subdivision(
            create_command=command
        )
        return subdivision


class UpdateSubdivisionCommandHandler(SubdivisionCommandHandler):

    async def __call__(
        self, command: UpdateSubdivisionCommand
    ) -> Subdivision:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        Subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        subdivision = await Subdivision_service.update_subdivision(
            update_command=command
        )
        return subdivision


class DeleteSubdivisionCommandHandler(SubdivisionCommandHandler):

    async def __call__(
        self, command: DeleteSubdivisionCommand
    ) -> Subdivision:
        """
        Delete subdivision by ID.
        """

        subdivision_service: SubdivisionService = SubdivisionService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        subdivision = await subdivision_service.delete_subdivision(
            id=command.id
        )
        return subdivision
