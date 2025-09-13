from abc import ABC

from backend.core.infra.handlers import (
    AbstractEventHandler, AbstractCommandHandler
)

from ..uow.subdivision_uow import (
    SubdivisionUnitOfWork
)


class SubdivisionEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class, from which every users event
    handler should be inherited from.
    """

    def __init__(self) -> None:
        self._uow: SubdivisionUnitOfWork


class SubdivisionCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class, from which every users
    command handler should be inherited from.
    """

    ...
