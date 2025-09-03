from typing import Self

from backend.core.infra.database.units_of_work import (
    SQLAlchemyAbstractUnitOfWork
)

from ....domain.services.repos.subdivision_repo import (
    SubdivisionRepository
)

from ....domain.services.uow.subdivision_uow import (
    SubdivisionUnitOfWork
)
from ...repos.sqlalchemy.subdivision_repo import (
    SQLAlchemySubdivisionRepository
)


class SQLAlchemySubdivisionUnitOfWork(
    SQLAlchemyAbstractUnitOfWork, SubdivisionUnitOfWork
):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.subdivisions: SubdivisionRepository = (
            SQLAlchemySubdivisionRepository(
                session=self._session
            )
        )
        return uow
