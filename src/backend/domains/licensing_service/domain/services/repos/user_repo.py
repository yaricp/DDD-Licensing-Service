from uuid import UUID
from typing import Optional, List
from abc import ABC, abstractmethod

from backend.core.infra.repositories import AbstractRepository
from backend.core.domain.entity import AbstractEntity

from ....domain.aggregates.entities.user import User


class UserRepository(AbstractRepository, ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily 
    replaced in users unit of work.
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def add(self, model: AbstractEntity) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, model: AbstractEntity) -> User:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[User]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_list_for_tenant(tenant_id: UUID) -> List[User]:
        raise NotImplementedError

    # @abstractmethod
    # async def get_by_email(self, email: str) -> Optional[User]:
    #     raise NotImplementedError

    # @abstractmethod
    # async def get_by_username(self, username: str) -> Optional[User]:
    #     raise NotImplementedError
