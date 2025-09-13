from abc import ABC, abstractmethod
from typing import Any

from backend.core.infra.units_of_work import AbstractUnitOfWork
from backend.core.infra.commands import AbstractCommand
from backend.core.infra.events import AbstractEvent
from backend.core.infra.eventbus import AbstractEventBus


class AbstractHandler(ABC):

    # @abstractmethod
    # def __init__(self, uow: AbstractUnitOfWork) -> None:
    #     raise NotImplementedError

    def __init__(
        self,
        domain_event_bus: AbstractEventBus,
        infra_event_bus: AbstractEventBus
    ) -> None:
        self.domain_event_bus = domain_event_bus
        self.infra_event_bus = infra_event_bus


class AbstractEventHandler(AbstractHandler, ABC):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    async def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class AbstractCommandHandler(AbstractHandler, ABC):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    async def __call__(self, command: AbstractCommand) -> Any:
        raise NotImplementedError

