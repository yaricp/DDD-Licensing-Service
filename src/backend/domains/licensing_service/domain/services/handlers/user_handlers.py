from abc import ABC

from backend.core.infra.handlers import AbstractCommandHandler, AbstractEventHandler


class UserEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class,
    from which every users event handler should
    be inherited from.
    """

    ...


class UserCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class,
    from which every users command handler should
    be inherited from.
    """

    ...
