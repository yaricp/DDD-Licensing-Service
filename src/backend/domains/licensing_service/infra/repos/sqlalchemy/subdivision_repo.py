from typing import Any, List, Optional, Sequence
from uuid import UUID

from sqlalchemy import Result, Row, RowMapping, delete, insert, select, update
from sqlalchemy.orm import selectinload

from backend.core.domain.entity import AbstractEntity
from backend.core.infra.database.repositories import SQLAlchemyAbstractRepository

from ....domain.aggregates.entities.license import License
from ....domain.aggregates.entities.stat_row import StatisticRow
from ....domain.aggregates.subdivision import Subdivision
from ....domain.services.repos.subdivision_repo import SubdivisionRepository


class SQLAlchemySubdivisionRepository(
    SQLAlchemyAbstractRepository, SubdivisionRepository
):

    async def add(self, model: AbstractEntity) -> Subdivision:
        print(f"model: {model}")
        for_save = await model.to_dict(
            exclude={"id", "licenses", "statistics", "_domain_events"}
        )
        result: Result = await self._session.execute(
            insert(Subdivision).values(**for_save).returning(Subdivision)
        )
        db_subdivision_id = result.scalar_one().id

        eager_result = await self._session.execute(
            select(Subdivision)
            .options(
                selectinload(Subdivision.licenses),
                selectinload(Subdivision.statistics),
            )
            .where(Subdivision.id == db_subdivision_id)
        )
        db_subdivision = eager_result.scalars().first()
        return db_subdivision

    async def update(self, id: UUID, model: AbstractEntity) -> Subdivision:
        print(f"model: {model}")
        result: Result = await self._session.execute(
            update(Subdivision)
            .options(
                selectinload(Subdivision.licenses),
                selectinload(Subdivision.statistics),
            )
            .filter_by(id=id)
            .values(
                **await model.to_dict(
                    exclude={"id", "licenses", "_domain_events", "statistics"}
                )
            )
            .returning(Subdivision)
        )
        return result.scalar_one()

    async def delete(self, id: UUID) -> Subdivision:
        result = await self._session.execute(
            delete(Subdivision).filter_by(id=id).returning(Subdivision)
        )
        return result.scalar_one()

    async def list(self) -> List[Subdivision]:
        """
        Returning result object instead of converting to new objects by
        [TenantModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal
        to fact return type.
        """

        result: Result = await self._session.execute(
            select(Subdivision).options(
                selectinload(Subdivision.licenses),
                selectinload(Subdivision.statistics),
            )
        )
        subdivisions: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(subdivisions, List)
        for subdivision in subdivisions:
            assert isinstance(subdivision, Subdivision)

        return subdivisions

    async def get(self, id: UUID) -> Optional[Subdivision]:
        subdivision_result: Result = await self._session.execute(
            select(Subdivision)
            .options(
                selectinload(Subdivision.licenses),
                selectinload(Subdivision.statistics),
            )
            .filter_by(id=id)
        )
        subdivision: Optional[Subdivision] = subdivision_result.scalar_one_or_none()
        if not subdivision:
            return None
        subdivision = Subdivision.make_from_persistence(
            id=subdivision.id,
            name=subdivision.name,
            location=subdivision.location,
            tenant_id=subdivision.tenant_id,
            work_status=subdivision.work_status,
            link_to_subdivision_processing_domain=(
                subdivision.link_to_subdivision_processing_domain
            ),
            licenses=subdivision.licenses,
            statistics=subdivision.statistics,
        )
        return subdivision

    async def get_license_by_id(self, license_id: UUID) -> Optional[License]:
        result: Result = await self._session.execute(
            select(License).filter_by(id=license_id)
        )
        return result.scalar_one_or_none()

    async def save_statistic_row(self, model: StatisticRow) -> Subdivision:
        print(f"model: {model}")
        for_save = await model.to_dict()
        result: Result = await self._session.execute(
            insert(StatisticRow).values(**for_save).returning(StatisticRow)
        )
        statistic_row = result.scalar_one()
        return statistic_row

    async def add_statistic_row(self, model: StatisticRow) -> StatisticRow:
        result: Result = await self._session.execute(
            insert(StatisticRow)
            .values(**await model.to_dict(exclude={"id"}))
            .returning(StatisticRow)
        )
        stats_row = result.scalar_one()
        print(f"stats_row: {stats_row}")
        return stats_row

    async def save(self, subdivision: Subdivision) -> Subdivision:
        print(f"subdivision: {subdivision}")
        new_sub = await self._session.merge(subdivision)
        print(f"new_sub: {new_sub}")
        return new_sub
