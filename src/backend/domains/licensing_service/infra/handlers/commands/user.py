from ....app.services.user_services import UserService
from ....domain.aggregates.entities.user import User
from ....domain.services.commands.user_commands import CreateUserCommand
from ....domain.services.handlers.user_handlers import UserCommandHandler


class CreateUserCommandHandler(UserCommandHandler):

    async def __call__(self, command: CreateUserCommand) -> User:
        """
        Registers a new user, if user with provided credentials doesn't exist,
        and creates event signaling that
        operation was successfully executed.
        """
        users_service: UserService = UserService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        user_new: User = User(**await command.to_dict())
        user = await users_service.create_user(model=user_new)
        return user
