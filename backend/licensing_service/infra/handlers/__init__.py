from typing import List, Dict, Type

from backend.core.domain.aggregate import AbstractAggregateRoot
from backend.core.infra.events import AbstractEvent
from backend.core.infra.commands import AbstractCommand
from backend.core.infra.handlers import (
    AbstractEventHandler, AbstractCommandHandler
)

from ...domain.services.events.user_events import (
    UserCreatedEvent, UserUpdatedEvent
)
from ...domain.services.events.tenant_events import (
    TenantCreatedEvent, TenantUpdatedEvent, TenantDeletedEvent
)
from ...domain.services.events.license_events import (
    LicenseActivatedEvent, LicenseCreatedEvent
)
from ...domain.services.events.subdivision_events import (
    SubdivisionCreatedEvent, SubdivisionUpdatedEvent,
    SubdivisionDeletedEvent, SubdivisionLicenseExpiredEvent
)
from ...domain.services.events.tenant_events import (
    TenantCreatedEvent, TenantUpdatedEvent, TenantDeletedEvent
)
from ...domain.services.events.license_events import (
    LicenseCreatedEvent, LicenseActivatedEvent, LicenseDeletedEvent,
    LicenseDeactivatedEvent
)
from ...domain.services.events.statistic_row_events import (
    StatisticRowAddedEvent
)
from ...domain.services.commands.user_commands import (
    CreateUserCommand
)
from ...domain.services.commands.tenant_commands import (
    CreateTenantCommand, UpdateTenantCommand, DeleteTenantCommand
)
from ...domain.services.commands.subdivision_commands import (
    CreateSubdivisionCommand, UpdateSubdivisionCommand,
    DeleteSubdivisionCommand
)
from ...domain.services.commands.license_commands import (
    CreateLicenseCommand, UpdateLicenseCommand, DeleteLicenseCommand
)
from ...domain.services.commands.subdivision_commands import (
    AddStatisticRowCommand,
    ActivateSubdivisionLicenseCommand,
    DeactivateSubdivisionLicenseCommand,
)

from .events.user_event_handlers import (
    UserCreatedEventHandler
)
from .events.tenant_event_handlers import (
    TenantCreatedEventHandler
)
from .events.license_event_handlers import (
    LicenseActivatedEventHandler, LicenseDeactivatedEventHandler
)
from .events.outside_broker_event_handlers import (
    ExternalMessageBusSender
)
from .commands.user import CreateUserCommandHandler
from .commands.subdivision import (
    CreateSubdivisionCommandHandler, UpdateSubdivisionCommandHandler,
    DeleteSubdivisionCommandHandler
)
from .commands.tenant import (
    CreateTenantCommandHandler, UpdateTenantCommandHandler,
    DeleteTenantCommandHandler
)
from .commands.license import (
    CreateLicenseCommandHandler, UpdateLicenseCommandHandler,
    DeleteLicenseCommandHandler
)
from .commands.subdivision import (
    ActivateSubdivisionLicenseCommandHandler,
    AddStaticticRowSubdivisionCommandHandler,
    DeactivateSubdivisionLicenseCommandHandler,
)


def aggregates_event_handler_scanner(
    events_handlers_for_injection: dict,
    class_aggregates: List[AbstractAggregateRoot]
):
    """ Check all aggregates if they have trigger methods"""
    for cls_aggregate in class_aggregates:
        for method in dir(cls_aggregate):
            print(method)


EVENTS_HANDLERS_FOR_INJECTION: Dict[
    Type[AbstractEvent], List[Type[AbstractEventHandler]]
] = {
    UserCreatedEvent: [
        ExternalMessageBusSender,
        UserCreatedEventHandler
    ],
    UserUpdatedEvent: [
        ExternalMessageBusSender,
    ],
    LicenseActivatedEvent: [
        ExternalMessageBusSender,
        LicenseActivatedEventHandler
    ],
    LicenseDeactivatedEvent: [
        ExternalMessageBusSender,
        LicenseDeactivatedEventHandler
    ],
    LicenseCreatedEvent: [
        ExternalMessageBusSender
    ],
    LicenseDeletedEvent: [
        ExternalMessageBusSender
    ],
    TenantCreatedEvent: [
        ExternalMessageBusSender
    ],
    TenantUpdatedEvent: [
        ExternalMessageBusSender
    ],
    TenantDeletedEvent: [
        ExternalMessageBusSender
    ],
    SubdivisionCreatedEvent: [
        ExternalMessageBusSender
    ],
    SubdivisionUpdatedEvent: [
        ExternalMessageBusSender
    ],
    SubdivisionDeletedEvent: [
        ExternalMessageBusSender
    ],
    StatisticRowAddedEvent: [
        ExternalMessageBusSender
    ],
    SubdivisionLicenseExpiredEvent: [
        ExternalMessageBusSender
    ]
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
    ActivateSubdivisionLicenseCommand: (
        ActivateSubdivisionLicenseCommandHandler
    ),
    DeactivateSubdivisionLicenseCommand: (
        DeactivateSubdivisionLicenseCommandHandler
    )
}
