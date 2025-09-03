from uuid import UUID
from typing import Optional, List
from abc import ABC, abstractmethod

from backend.core.domain.aggregate import AbstractAggregateRoot
from backend.core.infra.repositories import AbstractRepository
from backend.core.domain.entity import AbstractEntity

from ...aggregates.subdivision import Subdivision
from ...aggregates.entities.license import License
from ...aggregates.entities.stat_row import StatisticRow


class SubdivisionRepository(AbstractRepository, ABC):
    """
    An interface for work with subdivisions,
    that is used by subdivisions unit of work.
    The main goal is that implementations of this interface
    can be easily replaced in subdivisions unit of work
    using dependency injection without disrupting its functionality.
    """
    @abstractmethod
    async def add(
        self, model: AbstractEntity
    ) -> Subdivision:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> Optional[Subdivision]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: UUID, model: AbstractEntity
    ) -> Subdivision:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> Subdivision:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Subdivision]:
        raise NotImplementedError

    @abstractmethod
    async def get_license_by_id(self, id: UUID) -> Optional[License]:
        raise NotImplementedError

    @abstractmethod
    async def add_statistic_row(
        self, model: StatisticRow
    ) -> Optional[StatisticRow]:
        raise NotImplementedError

    # @abstractmethod
    # async def get_by_name(
    #     self, name: str
    # ) -> Optional[Subdivision]:
    #     raise NotImplementedError

    # @abstractmethod
    # async def get_by_location(
    #     self, location: str
    # ) -> Optional[Subdivision]:
    #     raise NotImplementedError

