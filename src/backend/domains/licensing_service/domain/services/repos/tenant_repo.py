from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from backend.core.domain.entity import AbstractEntity
from backend.core.infra.repositories import AbstractRepository

from ...aggregates.tenant import Tenant


class TenantRepository(AbstractRepository, ABC):
    """
    An interface for work with users, that is used by users unit of work.
    The main goal is that implementations of this interface can be easily
    replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def add(self, model: AbstractEntity) -> Tenant:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Tenant]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, model: AbstractEntity) -> Tenant:
        raise NotImplementedError

    @abstractmethod
    async def save(self, tenant: AbstractEntity) -> Tenant:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Tenant]:
        raise NotImplementedError
