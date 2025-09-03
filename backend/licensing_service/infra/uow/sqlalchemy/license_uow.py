from typing import Self

from backend.core.infra.database.units_of_work import (
    SQLAlchemyAbstractUnitOfWork
)

from ....domain.services.repos.license_repo import (
    LicenseRepository
)
from ....domain.services.uow.license_uow import (
    LicenseUnitOfWork
)
from ...repos.sqlalchemy.license_repo import (
    SQLAlchemyLicenseRepository
    # SQLAlchemyUserStatisticsRepository,
    # SQLAlchemyUserVotesRepository
)


class SQLAlchemyLicenseUnitOfWork(
    SQLAlchemyAbstractUnitOfWork, LicenseUnitOfWork
):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.licenses: LicenseRepository = SQLAlchemyLicenseRepository(
            session=self._session
        )
        # self.users_statistics: UsersStatisticsRepository = SQLAlchemyUsersStatisticsRepository(session=self._session)
        # self.users_votes: UsersVotesRepository = SQLAlchemyUsersVotesRepository(session=self._session)
        return uow
