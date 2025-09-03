from uuid import UUID
from typing import List, Optional, Sequence, Any
from sqlalchemy import (
    insert, select, delete, update,
    Result, RowMapping, Row
)
from sqlalchemy.orm import selectinload

from backend.core.domain.entity import AbstractEntity
from backend.core.infra.database.repositories import (
    SQLAlchemyAbstractRepository
)

from ....domain.aggregates.tenant import Tenant
from ....domain.aggregates.subdivision import Subdivision
# from ....domain.aggregates.entities.user import User
from ....domain.services.repos.tenant_repo import TenantRepository


class SQLAlchemyTenantRepository(
    SQLAlchemyAbstractRepository, TenantRepository
):

    async def get(self, id: UUID) -> Optional[Tenant]:
        result: Result = await self._session.execute(
            select(Tenant).options(
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.licenses
                ),
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.statistics
                ),
                selectinload(Tenant.subdivisions),
                selectinload(Tenant.users)
            ).filter_by(id=id)
        )
        tenant = result.scalar_one_or_none()
        if not tenant:
            return None
        tenant = Tenant.make_from_persistence(
            name=tenant.name, address=tenant.address, email=tenant.email,
            phone=tenant.phone, users=tenant.users,
            subdivisions=tenant.subdivisions, id=tenant.id
        )
        assert isinstance(tenant, Tenant)
        return tenant

    async def add(self, model: AbstractEntity) -> Tenant:
        result: Result = await self._session.execute(
            insert(Tenant).values(
                **await model.to_dict(
                    exclude={
                        'id', 'user_id', 'users',
                        'admins', 'subdivisions'
                    }
                )
            ).returning(Tenant)
        )
        created_tenant = result.scalar_one()
        print(f"created_tenant: {created_tenant}")
        tenant = await self.get(id=created_tenant.id)
        tenant = Tenant.make_from_persistence(
            name=tenant.name, address=tenant.address, email=tenant.email,
            phone=tenant.phone, users=tenant.users,
            subdivisions=tenant.subdivisions, id=tenant.id
        )
        return tenant

    async def update(self, id: UUID, model: AbstractEntity) -> Tenant:
        to_save = await model.to_dict(
            exclude={"id", "users", "subdivisions", "_domain_events"}
        )
        result: Result = await self._session.execute(
            update(Tenant).filter_by(id=id).values(
                **to_save
            ).returning(Tenant)
        )
        tenant = result.scalar_one()
        tenant = Tenant.make_from_persistence(
            name=tenant.name, address=tenant.address, email=tenant.email,
            phone=tenant.phone, users=tenant.users,
            subdivisions=tenant.subdivisions, id=tenant.id
        )
        return tenant

    async def delete(self, id: UUID) -> Tenant:
        result = await self._session.execute(
            delete(Tenant).options(
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.licenses
                ),
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.statistics
                ),
                selectinload(Tenant.subdivisions),
                selectinload(Tenant.users)
            ).filter_by(id=id).returning(Tenant)
        )
        return result.scalar_one()

    async def list(self) -> List[Tenant]:
        """
        Returning result object instead of converting to new objects by
        [TenantModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal 
        to fact return type.
        """
        db_result: Result = await self._session.execute(
            select(Tenant).options(
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.licenses
                ),
                selectinload(Tenant.subdivisions).selectinload(
                    Subdivision.statistics
                ),
                selectinload(Tenant.subdivisions),
                selectinload(Tenant.users)
            )
        )
        db_tenants: Sequence[Row | RowMapping | Any] = db_result.scalars().all()
        assert isinstance(db_tenants, List)
        tenant_list = []
        for db_tenant in db_tenants:
            assert isinstance(db_tenant, Tenant)
            tenant = Tenant.make_from_persistence(
                id=db_tenant.id, name=db_tenant.name, address=db_tenant.address,
                email=db_tenant.email, phone=db_tenant.phone,
                users=db_tenant.users, subdivisions=db_tenant.subdivisions
            )
            tenant_list.append(tenant)
        return tenant_list
