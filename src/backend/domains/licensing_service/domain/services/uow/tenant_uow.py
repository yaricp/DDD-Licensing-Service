from abc import ABC

from backend.core.infra.units_of_work import AbstractUnitOfWork

from ..repos.tenant_repo import TenantRepository
from ..repos.user_repo import UserRepository


class TenantUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with subdivisions,
    that is used by service layer of subdivisions module.
    The main goal is that implementations of this
    interface can be easily replaced in the service layer
    using dependency injection without disrupting its
    functionality.
    """

    tenants: TenantRepository
    users: UserRepository
