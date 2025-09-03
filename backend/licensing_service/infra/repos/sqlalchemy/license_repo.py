from uuid import UUID
from typing import List, Optional, Sequence, Any
from sqlalchemy import insert, select, delete, update, Result, RowMapping, Row

from backend.core.domain.entity import AbstractEntity

from backend.core.infra.database.repositories import (
    SQLAlchemyAbstractRepository
)

from ....domain.aggregates.entities.license import License
from ....domain.services.repos.license_repo import LicenseRepository


class SQLAlchemyLicenseRepository(
    SQLAlchemyAbstractRepository, LicenseRepository
):

    async def get(self, id: UUID) -> Optional[License]:
        result: Result = await self._session.execute(
            select(License).filter_by(id=id)
        )
        return result.scalar_one_or_none()

    async def get_by_type(self, type: str) -> Optional[License]:
        result: Result = await self._session.execute(
            select(License).filter_by(type=type)
        )
        return result.scalar_one_or_none()

    async def get_by_status(self, status: str) -> Optional[License]:
        result: Result = await self._session.execute(
            select(License).filter_by(status=status)
        )
        return result.scalar_one_or_none()

    async def add(self, model: AbstractEntity) -> License:
        result: Result = await self._session.execute(
            insert(License).values(
                **await model.to_dict(exclude={'id'})
            ).returning(License)
        )

        return result.scalar_one()

    async def update(self, id: UUID, model: AbstractEntity) -> License:
        # result_get_license: Result = await self._session.execute(
        #     select(License).filter_by(id=id)
        # )
        # license = result_get_license.scalar_one()
        # model.tenant_id = license.tenant_id
        result: Result = await self._session.execute(
            update(License).filter_by(id=id).values(
                **await model.to_dict(
                    exclude={
                        "type", "count_requests",
                        "status", "datetime_created"
                    }
                )
            ).returning(License)
        )

        return result.scalar_one()

    async def delete(self, id: UUID) -> License:
        result = await self._session.execute(
            delete(License).filter_by(id=id).returning(
                License
            )
        )
        return result.scalar_one()

    async def list(self) -> List[License]:
        """
        Returning result object instead of converting to new objects by
        [TenantModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal 
        to fact return type.
        """

        result: Result = await self._session.execute(select(License))
        licenses: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(licenses, List)
        for license in licenses:
            assert isinstance(license, License)

        return licenses
