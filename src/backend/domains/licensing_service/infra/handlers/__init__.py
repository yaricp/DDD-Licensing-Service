from typing import Dict, List, Type

from backend.core.domain.aggregate import AbstractAggregateRoot
from backend.core.infra.commands import AbstractCommand
from backend.core.infra.events import AbstractEvent
from backend.core.infra.handlers import AbstractCommandHandler, AbstractEventHandler

from ...domain.services.commands.license_commands import (
    CreateLicenseCommand,
    DeleteLicenseCommand,
    UpdateLicenseCommand,
)
from ...domain.services.commands.subdivision_commands import (
    ActivateSubdivisionLicenseCommand,
    AddStatisticRowCommand,
    CreateSubdivisionCommand,
    DeactivateSubdivisionLicenseCommand,
    DeleteSubdivisionCommand,
    UpdateSubdivisionCommand,
)
from ...domain.services.commands.tenant_commands import (
    CreateTenantCommand,
    DeleteTenantCommand,
    UpdateTenantCommand,
)
from ...domain.services.commands.user_commands import CreateUserCommand
from ...domain.services.events.license_events import (
    LicenseActivatedEvent,
    LicenseCreatedEvent,
    LicenseDeactivatedEvent,
    LicenseDeletedEvent,
)
from ...domain.services.events.statistic_row_events import StatisticRowAddedEvent
from ...domain.services.events.subdivision_events import (
    SubdivisionCreatedEvent,
    SubdivisionDeletedEvent,
    SubdivisionLicenseExpiredEvent,
    SubdivisionUpdatedEvent,
)
from ...domain.services.events.tenant_events import (
    TenantCreatedEvent,
    TenantDeletedEvent,
    TenantUpdatedEvent,
)
from ...domain.services.events.user_events import UserCreatedEvent, UserUpdatedEvent
from .commands.license import (
    CreateLicenseCommandHandler,
    DeleteLicenseCommandHandler,
    UpdateLicenseCommandHandler,
)
from .commands.subdivision import (
    ActivateSubdivisionLicenseCommandHandler,
    AddStaticticRowSubdivisionCommandHandler,
    CreateSubdivisionCommandHandler,
    DeactivateSubdivisionLicenseCommandHandler,
    DeleteSubdivisionCommandHandler,
    UpdateSubdivisionCommandHandler,
)
from .commands.tenant import (
    CreateTenantCommandHandler,
    DeleteTenantCommandHandler,
    UpdateTenantCommandHandler,
)
from .commands.user import CreateUserCommandHandler
from .events.license_event_handlers import (
    LicenseActivatedEventHandler,
    LicenseDeactivatedEventHandler,
)
from .events.outside_broker_event_handlers import ExternalMessageBusSender
from .events.tenant_event_handlers import TenantCreatedEventHandler
from .events.user_event_handlers import UserCreatedEventHandler


def aggregates_event_handler_scanner(
    events_handlers_for_injection: dict, class_aggregates: List[AbstractAggregateRoot]
):
    """Check all aggregates if they have trigger methods"""
    for cls_aggregate in class_aggregates:
        for method in dir(cls_aggregate):
            print(method)


EVENTS_HANDLERS_FOR_INJECTION: Dict[
    Type[AbstractEvent], List[Type[AbstractEventHandler]]
] = {
    UserCreatedEvent: [ExternalMessageBusSender, UserCreatedEventHandler],
    UserUpdatedEvent: [
        ExternalMessageBusSender,
    ],
    LicenseActivatedEvent: [ExternalMessageBusSender, LicenseActivatedEventHandler],
    LicenseDeactivatedEvent: [ExternalMessageBusSender, LicenseDeactivatedEventHandler],
    LicenseCreatedEvent: [ExternalMessageBusSender],
    LicenseDeletedEvent: [ExternalMessageBusSender],
    TenantCreatedEvent: [ExternalMessageBusSender],
    TenantUpdatedEvent: [ExternalMessageBusSender],
    TenantDeletedEvent: [ExternalMessageBusSender],
    SubdivisionCreatedEvent: [ExternalMessageBusSender],
    SubdivisionUpdatedEvent: [ExternalMessageBusSender],
    SubdivisionDeletedEvent: [ExternalMessageBusSender],
    StatisticRowAddedEvent: [ExternalMessageBusSender],
    SubdivisionLicenseExpiredEvent: [ExternalMessageBusSender],
}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[
    Type[AbstractCommand], Type[AbstractCommandHandler]
] = {
    CreateUserCommand: CreateUserCommandHandler,
    CreateTenantCommand: CreateTenantCommandHandler,
    UpdateTenantCommand: UpdateTenantCommandHandler,
    DeleteTenantCommand: DeleteTenantCommandHandler,
    CreateSubdivisionCommand: CreateSubdivisionCommandHandler,
    UpdateSubdivisionCommand: UpdateSubdivisionCommandHandler,
    DeleteSubdivisionCommand: DeleteSubdivisionCommandHandler,
    CreateLicenseCommand: CreateLicenseCommandHandler,
    UpdateLicenseCommand: UpdateLicenseCommandHandler,
    DeleteLicenseCommand: DeleteLicenseCommandHandler,
    AddStatisticRowCommand: AddStaticticRowSubdivisionCommandHandler,
    ActivateSubdivisionLicenseCommand: (ActivateSubdivisionLicenseCommandHandler),
    DeactivateSubdivisionLicenseCommand: (DeactivateSubdivisionLicenseCommandHandler),
}
