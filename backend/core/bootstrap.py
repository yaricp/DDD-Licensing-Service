import inspect
from types import MappingProxyType
from typing import Union, Type, Dict, Any, List, Optional

from backend.core.infra import (
    AbstractCommand,
    AbstractEvent,
    AbstractEventHandler,
    AbstractCommandHandler
)
from .messagebus_handler import GlobalMessageBusHandler
from .infra.eventbus import AbstractEventBus

# MessageBus


class Bootstrap:
    """
    Bootstrap class for Dependencies Injection purposes.
    """
    # uow: AbstractUnitOfWork,
    def __init__(
        self, domain_event_bus: AbstractEventBus,
        infra_event_bus: AbstractEventBus,
        events_handlers_for_injection: Dict[
            Type[AbstractEvent], List[Type[AbstractEventHandler]]
        ] = None,
        commands_handlers_for_injection: Dict[
            Type[AbstractCommand], Type[AbstractCommandHandler]
        ] = None,
        dependencies: Optional[Dict[str, Any]] = None
    ) -> None:

        # self._uow: AbstractUnitOfWork = uow
        # {'uow': self._uow}
        self.domain_event_bus = domain_event_bus
        self.infra_event_bus = infra_event_bus
        self._dependencies: Dict[str, Any] = {
            "domain_event_bus": self.domain_event_bus,
            "infra_event_bus": self.infra_event_bus
        }
        self._events_handlers_for_injection: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = (
            events_handlers_for_injection
        )
        self._commands_handlers_for_injection: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = (
            commands_handlers_for_injection
        )

        if dependencies:
            self._dependencies.update(dependencies)

    def get_messagebus(self) -> GlobalMessageBusHandler:
        """
        Makes necessary injections to commands handlers
        and events handlers for creating appropriate messagebus,
        after which returns messagebus instance.
        """

        injected_event_handlers: Dict[
            Type[AbstractEvent], List[AbstractEventHandler]
        ] = {
            event_type: [
                self._inject_dependencies(handler=handler)
                for handler in event_handlers
            ]
            for event_type, event_handlers in self._events_handlers_for_injection.items()
        }

        injected_command_handlers: Dict[
            Type[AbstractCommand], AbstractCommandHandler
        ] = {
            command_type: self._inject_dependencies(handler=handler)
            for command_type, handler in self._commands_handlers_for_injection.items()
        }

        # uow=self._uow,
        return GlobalMessageBusHandler(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus,
            event_handlers=injected_event_handlers,
            command_handlers=injected_command_handlers,
        )

    # async 
    def _inject_dependencies(
        self,
        handler: Union[Type[AbstractEventHandler], Type[AbstractCommandHandler]]
    ) -> Union[AbstractEventHandler, AbstractCommandHandler]:

        """
        Inspecting handler to know its signature and init params,
        after which only necessary dependencies will be
        injected to the handler.
        """

        params: MappingProxyType[str, inspect.Parameter] = inspect.signature(
            handler
        ).parameters
        handler_dependencies: Dict[str, Any] = {
            name: dependency
            for name, dependency in self._dependencies.items()
            if name in params
        }
        return handler(**handler_dependencies)
