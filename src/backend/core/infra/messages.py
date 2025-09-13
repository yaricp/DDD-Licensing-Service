from typing import Union

from backend.core.infra.events import AbstractEvent
from backend.core.infra.commands import AbstractCommand


Message = Union[AbstractEvent, AbstractCommand]