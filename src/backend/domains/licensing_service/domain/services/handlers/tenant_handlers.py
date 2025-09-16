from abc import ABC

from backend.core.infra.handlers import (
    AbstractCommandHandler, AbstractEventHandler
)

from ..uow.tenant_uow import TenantUnitOfWork


class TenantEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class, from which every users event handler
    should be inherited from.
    """

    def __init__(self) -> None:
        self._uow: TenantUnitOfWork


class TenantCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class, from which every users command handler
    should be inherited from.
    """

    ...
