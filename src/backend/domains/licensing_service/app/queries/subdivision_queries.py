from uuid import UUID
from typing import Optional, List

# ---Domain imports---
from ...domain.services.uow.subdivision_uow import SubdivisionUnitOfWork
from ...domain.aggregates.subdivision import Subdivision
from ...domain.exceptions.subdivision import SubdivisionNotFoundError

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.subdivision_uow import (
    SQLAlchemySubdivisionUnitOfWork
)

# ---Application imports---
from ..services.subdivision_services import SubdivisionService


class SubdivisionQuery:
    """
    Query class use for read info about Subdivision aggregate.
    It's in CQRS paradigme
    """

    def __init__(self) -> None:
        self._uow: SubdivisionUnitOfWork = SQLAlchemySubdivisionUnitOfWork()

    async def get_subdivision_by_id(
        self, id: UUID
    ) -> Subdivision:
        async with self._uow as uow:
            subdivision: Optional[
                Subdivision
            ] = await uow.subdivisions.get(id=id)
            if not subdivision:
                raise SubdivisionNotFoundError
        return subdivision

    async def get_subdivision(self, subdivision_id: UUID) -> Subdivision:
        subdivisions_service: SubdivisionService = SubdivisionService()
        subdivision: Subdivision = await subdivisions_service.get_subdivision_by_id(
            id=subdivision_id
        )
        return subdivision

    async def get_all_subdivisions(self) -> List[Subdivision]:
        subdivisions_service: SubdivisionService = SubdivisionService()
        subdivisions: List[
            Subdivision
        ] = await subdivisions_service.get_all_subdivisions()
        return subdivisions
