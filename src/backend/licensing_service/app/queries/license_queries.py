from uuid import UUID
from typing import Optional, List

# ---Domain imports---
from ...domain.aggregates.entities.license import License
from ...domain.exceptions.license import LicenseNotFoundError

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.license_uow import (
    SQLAlchemyLicenseUnitOfWork as UOW
)


class LicenseQuery:
    """
    Query class use for read info about License.
    It's in CQRS paradigme
    """

    def __init__(self) -> None:
        self._uow: UOW = UOW()

    async def get_license(self, id: UUID) -> License:
        async with self._uow as uow:
            license: Optional[License] = await uow.licenses.get(id=id)
            if not license:
                raise LicenseNotFoundError
        return license

    async def get_all_licenses(self) -> List[License]:
        async with self._uow as uow:
            licenses: List[License] = await uow.licenses.list()
            return licenses

    async def get_license_by_status(self, status: str) -> License:
        async with self._uow as uow:
            license: Optional[
                License
            ] = await uow.licenses.get_by_status(status=status)
            if not license:
                raise LicenseNotFoundError
            return license
