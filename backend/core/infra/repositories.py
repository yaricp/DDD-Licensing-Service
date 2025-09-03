from uuid import UUID
from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.entity import AbstractEntity


class AbstractRepository(ABC):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    async def add(self, model: AbstractEntity) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[AbstractEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, model: AbstractEntity) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> AbstractEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[AbstractEntity]:
        raise NotImplementedError
