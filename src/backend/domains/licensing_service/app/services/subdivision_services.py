from typing import Any, List, Optional
from uuid import UUID

from ...domain.aggregates.entities.license import License
from ...domain.aggregates.entities.stat_row import StatisticRow

# ---Domain imports---
from ...domain.aggregates.subdivision import Subdivision
from ...domain.exceptions.subdivision import SubdivisionNotFoundError
from ...domain.services.commands.license_commands import (
    CreateLicenseCommand,
    DeleteLicenseCommand,
    UpdateLicenseCommand,
)
from ...domain.services.commands.subdivision_commands import (
    AddStatisticRowCommand,
    CreateSubdivisionCommand,
    UpdateSubdivisionCommand,
)
from ...domain.services.domain_event_bus import DomainEventBus
from ...domain.services.events.license_events import (
    LicenseActivatedEvent,
    LicenseCreatedEvent,
    LicenseDeactivatedEvent,
    LicenseDeletedEvent,
)
from ...domain.services.events.statistic_row_events import StatisticRowAddedEvent
from ...domain.services.events.subdivision_events import (
    SubdivisionCreatedEvent,
    SubdivisionDeletedEvent,
    SubdivisionLicenseExpiredEvent,
    SubdivisionUpdatedEvent,
)
from ...domain.services.uow.subdivision_uow import SubdivisionUnitOfWork

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.subdivision_uow import (
    SQLAlchemySubdivisionUnitOfWork as UOW,
)


class SubdivisionService:
    """
    Service layer core according to DDD,
    which using a unit of work, will perform operations
    on the domain model.
    """

    def __init__(
        self,
        domain_event_bus: DomainEventBus | None = None,
        infra_event_bus: DomainEventBus | None = None,
        db_session_factory: Any | None = None,
    ) -> None:
        self._domain_event_bus = domain_event_bus
        self._infra_event_bus = infra_event_bus
        if db_session_factory:
            self._uow: SubdivisionUnitOfWork = UOW(session_factory=db_session_factory)
        else:
            self._uow: SubdivisionUnitOfWork = UOW()

    async def activate_subdivision_license(
        self, subdivision_id: UUID, license_id: UUID
    ) -> Optional[Subdivision]:
        async with self._uow as uow:
            subdivision = await uow.subdivisions.get(id=subdivision_id)
            if subdivision:
                await subdivision.activate_license(license_id, self._domain_event_bus)
                await uow.subdivisions.save(subdivision)
                license = list(
                    filter(lambda x: x.id == license_id, subdivision.licenses)
                )[0]
            await uow.commit()

            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    LicenseActivatedEvent(**await license.to_dict())
                )
            return subdivision

    async def deactivate_subdivision_license(
        self, subdivision_id: UUID, license_id: UUID
    ) -> Optional[Subdivision]:
        async with self._uow as uow:
            subdivision = await uow.subdivisions.get(id=subdivision_id)
            if subdivision:
                await subdivision.deactivate_license(license_id, self._domain_event_bus)
                await uow.subdivisions.save(subdivision)
                license = list(
                    filter(lambda x: x.id == license_id, subdivision.licenses)
                )[0]
            await uow.commit()
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    LicenseDeactivatedEvent(**await license.to_dict())
                )
            return subdivision

    async def add_license(
        self, add_license_command: CreateLicenseCommand
    ) -> Optional[Subdivision]:
        async with self._uow as uow:
            subdivision = await self.get_subdivision_by_id(
                id=add_license_command.subdivision_id
            )
            if not subdivision:
                raise SubdivisionNotFoundError
            license = subdivision.add_license(**await add_license_command.to_dict())
            await uow.subdivisions.save(subdivision)
            await uow.commit()
            subdivision = await self.get_subdivision_by_id(
                id=add_license_command.subdivision_id
            )
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    LicenseCreatedEvent(**await license.to_dict())
                )
            return subdivision

    async def update_license(
        self, update_license_command: UpdateLicenseCommand
    ) -> Optional[Subdivision]:
        async with self._uow as uow:
            subdivision = await self.get_subdivision_by_id(
                id=update_license_command.subdivision_id
            )
            if not subdivision:
                raise SubdivisionNotFoundError
            subdivision.update_license(
                id=update_license_command.id,
                name=update_license_command.name,
                description=update_license_command.description,
            )
            new_sub = await uow.subdivisions.save(subdivision)
            await uow.commit()
            print(f"new_sub: {new_sub}")
            subdivision = await self.get_subdivision_by_id(
                id=update_license_command.subdivision_id
            )
            return subdivision

    async def delete_license(
        self, delete_license_command: DeleteLicenseCommand
    ) -> Optional[Subdivision]:
        async with self._uow as uow:
            subdivision = await self.get_subdivision_by_id(
                id=delete_license_command.subdivision_id
            )
            if not subdivision:
                raise SubdivisionNotFoundError
            subdivision.delete_license(id=delete_license_command.id)
            await uow.subdivisions.save(subdivision)
            await uow.commit()
            subdivision = await self.get_subdivision_by_id(
                id=delete_license_command.subdivision_id
            )
            return subdivision

    async def add_subdivision_statistic_row(
        self, new_stats_command: AddStatisticRowCommand
    ) -> Subdivision:
        subdivision_id = new_stats_command.subdivision_id
        async with self._uow as uow:
            print(f"new_stats_command: {new_stats_command}")
            license_expired = False
            # build subdivision aggregate from DB
            subdivision = await uow.subdivisions.get(id=subdivision_id)
            if not subdivision:
                raise SubdivisionNotFoundError
            new_stats_row = StatisticRow.make(
                count_requests=new_stats_command.count_requests,
                subdivision_id=new_stats_command.subdivision_id,
            )
            # Adding a new stats row
            await subdivision.save_day_statistic(
                stat_row=new_stats_row, eventbus=self._domain_event_bus
            )
            # Saving subdivision aggregate to DB
            await uow.subdivisions.save(subdivision)
            if not subdivision.is_active:
                license_expired = True

            await uow.commit()
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    StatisticRowAddedEvent(**await new_stats_row.to_dict())
                )
            if license_expired:
                if self._infra_event_bus:
                    self._infra_event_bus.add_event(
                        SubdivisionLicenseExpiredEvent(
                            **await subdivision.to_dict(
                                exclude={"licenses", "statistics"}
                            )
                        )
                    )
            return subdivision

    async def update_subdivision(
        self, update_command: UpdateSubdivisionCommand
    ) -> Subdivision:
        async with self._uow as uow:
            print(f"update_command: {update_command}")
            subdivision = await self.get_subdivision_by_id(id=update_command.id)
            if not subdivision:
                raise SubdivisionNotFoundError
            subdivision.update(
                name=update_command.name,
                location=update_command.location,
                work_status=update_command.work_status,
                link_to_subdivision_processing_domain=(
                    update_command.link_to_subdivision_processing_domain
                ),
            )
            print(f"subdivision: {subdivision}")
            subdivision = await uow.subdivisions.update(
                id=subdivision.id, model=subdivision
            )
            await uow.commit()
            print(f"Updated subdivision: {subdivision}")
            subdivision = await self.get_subdivision_by_id(id=subdivision.id)
            print(f"Last subdivision: {subdivision}")
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    SubdivisionUpdatedEvent(
                        id=subdivision.id,
                        name=subdivision.name,
                        location=subdivision.location,
                        work_status=subdivision.work_status,
                        tenant_id=subdivision.tenant_id,
                        link_to_subdivision_processing_domain=subdivision.link_to_subdivision_processing_domain,
                    )
                )
            return subdivision

    async def delete_subdivision(self, id: UUID) -> Subdivision:
        async with self._uow as uow:
            subdivision = await self.get_subdivision_by_id(id=id)
            if not subdivision:
                raise SubdivisionNotFoundError
            subdivision: Subdivision = await uow.subdivisions.delete(id=id)
            await uow.commit()
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    SubdivisionDeletedEvent(
                        id=subdivision.id,
                        name=subdivision.name,
                        location=subdivision.location,
                        work_status=subdivision.work_status,
                        tenant_id=subdivision.tenant_id,
                        link_to_subdivision_processing_domain=(
                            subdivision.link_to_subdivision_processing_domain
                        ),
                    )
                )
            return subdivision

    async def create_subdivision(
        self, create_command: CreateSubdivisionCommand
    ) -> Subdivision:
        async with self._uow as uow:
            subdivision = Subdivision.make(
                name=create_command.name,
                location=create_command.location,
                tenant_id=create_command.tenant_id,
            )
            subdivision = await uow.subdivisions.add(model=subdivision)
            await uow.commit()
            if self._infra_event_bus:
                self._infra_event_bus.add_event(
                    SubdivisionCreatedEvent(
                        id=subdivision.id,
                        name=subdivision.name,
                        work_status=subdivision.work_status,
                        location=subdivision.location,
                        tenant_id=subdivision.tenant_id,
                        link_to_subdivision_processing_domain=subdivision.link_to_subdivision_processing_domain,
                    )
                )
            return subdivision

    async def get_all_subdivisions(self) -> List[Subdivision]:
        async with self._uow as uow:
            subdivisions: List[Subdivision] = await uow.subdivisions.list()
            return subdivisions

    async def get_subdivision_by_id(self, id: UUID) -> Subdivision:
        async with self._uow as uow:
            subdivision: Optional[Subdivision] = await uow.subdivisions.get(id=id)
            if not subdivision:
                raise SubdivisionNotFoundError
        return subdivision
