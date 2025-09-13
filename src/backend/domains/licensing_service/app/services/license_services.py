from uuid import UUID
from typing import Optional

# ---Domain imports---
from ...domain.aggregates.entities.license import License
from ...domain.aggregates.subdivision import Subdivision
from ...domain.services.domain_event_bus import DomainEventBus
from ...domain.services.uow.license_uow import LicenseUnitOfWork
from ...domain.services.events.license_events import LicenseCreatedEvent
from ...domain.services.commands.license_commands import (
    CreateLicenseCommand, UpdateLicenseCommand, DeleteLicenseCommand
)
from ...domain.exceptions.license import LicenseNotFoundError

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.license_uow import (
    SQLAlchemyLicenseUnitOfWork as UOW
)

from ..services.subdivision_services import SubdivisionService


class LicenseService:
    """
    Service layer core according to DDD,
    which using a unit of work, will perform operations
    on the domain model.
    """

    def __init__(
        self,
        domain_event_bus: DomainEventBus | None = None,
        infra_event_bus: DomainEventBus | None = None
    ) -> None:
        self._domain_event_bus = domain_event_bus
        self._infra_event_bus = infra_event_bus
        self._uow: LicenseUnitOfWork = UOW()

    async def create_license(
        self, create_command: CreateLicenseCommand
    ) -> License:
        async with self._uow as uow:
            subdivision_service = SubdivisionService(
                domain_event_bus=self._domain_event_bus,
                infra_event_bus=self._infra_event_bus
            )
            subdivision = subdivision_service.get_subdivision_by_id(
                id=create_command.id
            )
            subdivision.add_license(
                name=create_command.name,
                description=create_command.description,
                type=create_command.type,
                count_requests=create_command.count_requests
            )
            event = LicenseCreatedEvent(**await license.to_dict())
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            return license

    async def get_license_by_id(self, id: UUID) -> License:
        async with self._uow as uow:
            license: Optional[License] = await uow.licenses.get(id=id)
            if not license:
                raise LicenseNotFoundError
        return license

    async def update_license(
        self, id: UUID, license: License
    ) -> License:
        async with self._uow as uow:
            found_license = await uow.licenses.get(id=id)
            if not found_license:
                raise LicenseNotFoundError
            license.tenant_id = found_license.tenant_id
            updated_license = await uow.licenses.update(
                id=id, model=license
            )
            await uow.commit()
            return updated_license

    async def delete_license(self, id: UUID) -> License:
        async with self._uow as uow:
            result: License = await uow.licenses.delete(id=id)
            await uow.commit()
            return result
