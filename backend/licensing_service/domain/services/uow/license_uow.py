from abc import ABC

from ..repos.license_repo import (
    LicenseRepository
)
from backend.core.infra.units_of_work import AbstractUnitOfWork


class LicenseUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with users, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    licenses: LicenseRepository
