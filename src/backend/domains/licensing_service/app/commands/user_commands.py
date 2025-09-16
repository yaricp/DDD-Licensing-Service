# ---Core imports---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# ---Domain imports---
from ...domain.aggregates.entities.user import User
from ...domain.services.commands.user_commands import CreateUserCommand


class UserCommandUseCase:

    def __init__(self, messagebus_handler: GlobalMessageBusHandler):
        self.messagebus_handler = messagebus_handler

    async def create_user(self, **kwargs) -> User:
        await self.messagebus_handler.handle(CreateUserCommand(**kwargs))
        return self.messagebus_handler.command_result
