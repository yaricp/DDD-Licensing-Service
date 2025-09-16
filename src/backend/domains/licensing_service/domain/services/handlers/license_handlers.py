from abc import ABC

from backend.core.infra.handlers import AbstractCommandHandler, AbstractEventHandler


class LicenseEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class,
    from which every licenses event handler should be inherited
    from.
    """

    ...


class LicenseCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class,
    from which every licenses command handler should be inherited from.
    """

    ...
