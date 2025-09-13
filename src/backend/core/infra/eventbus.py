from abc import ABC
from typing import List, Generator

from .events import AbstractEvent


class AbstractEventBus(ABC):

    def __init__(self):
        self._events: List[AbstractEvent] = []

    def add_event(self, event: AbstractEvent) -> None:
        self._events.append(event)

    def get_events(self) -> Generator[AbstractEvent, None, None]:
        """
        Using generator to get elements only when they needed.
        Also can not use self._events directly, not to run events endlessly.
        """

        while self._events:
            yield self._events.pop(0)
