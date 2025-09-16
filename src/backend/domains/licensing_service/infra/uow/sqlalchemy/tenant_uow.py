from typing import Self

from backend.core.infra.database.units_of_work import SQLAlchemyAbstractUnitOfWork

from ....domain.services.repos.subdivision_repo import SubdivisionRepository
from ....domain.services.repos.tenant_repo import TenantRepository
from ....domain.services.repos.user_repo import UserRepository
from ....domain.services.uow.tenant_uow import TenantUnitOfWork
from ...repos.sqlalchemy.subdivision_repo import SQLAlchemySubdivisionRepository
from ...repos.sqlalchemy.tenant_repo import SQLAlchemyTenantRepository
from ...repos.sqlalchemy.user_repo import SQLAlchemyUserRepository


class SQLAlchemyTenantUnitOfWork(SQLAlchemyAbstractUnitOfWork, TenantUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.subdivisions: SubdivisionRepository = SQLAlchemySubdivisionRepository(
            session=self._session
        )
        self.tenants: TenantRepository = SQLAlchemyTenantRepository(
            session=self._session
        )
        self.users: UserRepository = SQLAlchemyUserRepository(session=self._session)
        return uow
