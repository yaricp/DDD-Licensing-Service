from typing import Dict, List, Type, Any
from queue import Queue

from .exceptions import MessageBusMessageError
from backend.core.infra.commands import AbstractCommand
from backend.core.infra.events import AbstractEvent
from backend.core.infra.eventbus import AbstractEventBus
from backend.core.infra.handlers import AbstractEventHandler, AbstractCommandHandler
from backend.core.infra.messages import Message

# class MessageBus:


class GlobalMessageBusHandler:

    def __init__(
        self,
        domain_event_bus: AbstractEventBus,
        infra_event_bus: AbstractEventBus,
        event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]],
        command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler],
    ) -> None:

        self._domain_event_bus = domain_event_bus
        self._infra_event_bus = infra_event_bus
        self._event_handlers: Dict[
            Type[AbstractEvent], List[AbstractEventHandler]
        ] = event_handlers
        self._command_handlers: Dict[
            Type[AbstractCommand], AbstractCommandHandler
        ] = command_handlers
        self._queue: Queue = Queue()
        self._command_result: Any = None

    async def handle(self, message: Message) -> None:
        self._queue.put(message)
        while not self._queue.empty():
            message = self._queue.get()
            if isinstance(message, AbstractEvent):
                await self._handle_event(event=message)
            elif isinstance(message, AbstractCommand):
                await self._handle_command(command=message)
            else:
                raise MessageBusMessageError

    async def _handle_event(self, event: AbstractEvent) -> None:
        handler: AbstractEventHandler
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._domain_event_bus.get_events():
                self._queue.put_nowait(event)
            for event in self._infra_event_bus.get_events():
                self._queue.put_nowait(event)

    async def _handle_command(self, command: AbstractCommand) -> None:
        handler: AbstractCommandHandler = self._command_handlers[type(command)]
        self._command_result = await handler(command)
        for event in self._domain_event_bus.get_events():
            self._queue.put_nowait(event)
        for event in self._infra_event_bus.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result
