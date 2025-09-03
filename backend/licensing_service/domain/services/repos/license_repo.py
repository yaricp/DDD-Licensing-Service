from uuid import UUID
from typing import Optional, List
from abc import ABC, abstractmethod

from backend.core.infra.repositories import AbstractRepository
from backend.core.domain.entity import AbstractEntity

from ...aggregates.entities.license import License


class LicenseRepository(AbstractRepository, ABC):
    """
    An interface for work with licenses, that is used by licenses unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_status(self, status: str) -> Optional[License]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_type(self, type: str) -> Optional[License]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractEntity) -> License:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[License]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, model: AbstractEntity) -> License:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: UUID) -> License:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[License]:
        raise NotImplementedError
