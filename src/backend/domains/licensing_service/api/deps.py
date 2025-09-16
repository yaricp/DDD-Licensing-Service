from backend.core.bootstrap import Bootstrap
from backend.core.messagebus_handler import GlobalMessageBusHandler

from ..app import DomainEventBus
from ..infra.handlers import (
    COMMANDS_HANDLERS_FOR_INJECTION,
    EVENTS_HANDLERS_FOR_INJECTION,
)


def get_messagebus_handler():
    bootstrap: Bootstrap = Bootstrap(
        domain_event_bus=DomainEventBus(),
        infra_event_bus=DomainEventBus(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
    )
    messagebus_handler: GlobalMessageBusHandler = bootstrap.get_messagebus()
    return messagebus_handler


# def get_message_bus() -> MessageBus:
#     bootstrap: Bootstrap = Bootstrap(
#         domain_event_bus=,
#         events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
#         commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
#     )
#     print("get message bus")
#     messagebus: MessageBus = bootstrap.get_messagebus()
#     print(f"messbus: {messagebus}")
#     return messagebus


# messagebus = get_message_bus()
