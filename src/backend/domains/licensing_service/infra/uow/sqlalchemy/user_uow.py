from typing import Self

from backend.core.infra.database.units_of_work import (
    SQLAlchemyAbstractUnitOfWork
)

from ...repos.sqlalchemy.user_repo import (
    SQLAlchemyUserRepository
)
from ....domain.services.uow.user_uow import (
    UserUnitOfWork
)
from ....domain.services.repos.user_repo import (
    UserRepository
)


class SQLAlchemyUserUnitOfWork(
    SQLAlchemyAbstractUnitOfWork, UserUnitOfWork
):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UserRepository = SQLAlchemyUserRepository(
            session=self._session
        )
        return uow
