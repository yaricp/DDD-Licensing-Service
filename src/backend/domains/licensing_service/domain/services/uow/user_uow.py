from abc import ABC

from backend.core.infra.units_of_work import AbstractUnitOfWork

from ..repos.user_repo import UserRepository


class UserUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with users, that is used
    by service layer of users module.
    The main goal is that implementations of this interface
    can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    users: UserRepository
