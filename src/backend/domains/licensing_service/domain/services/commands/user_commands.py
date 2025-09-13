from uuid import UUID

from dataclasses import dataclass

from backend.core.infra.commands import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    user_id: UUID
