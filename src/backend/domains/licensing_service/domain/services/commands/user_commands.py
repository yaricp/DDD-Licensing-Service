from dataclasses import dataclass
from uuid import UUID

from backend.core.infra.commands import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    user_id: UUID
