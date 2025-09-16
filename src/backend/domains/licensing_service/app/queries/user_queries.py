from typing import List
from uuid import UUID

# ---Core imports---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# ---Domain imports---
from ...domain.aggregates.entities.user import User

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.user_uow import SQLAlchemyUserUnitOfWork as UOW

# ---Application imports---
from ..commands.user_commands import UserCommandUseCase


class UserQuery:
    """
    Views related to users, which purpose is to return information
    upon read requests,
    due to the fact that write requests
    (represented by commands) are different from read requests.

    # TODO At current moment uses repositories pattern to retrieve data.
    # In future can be changed on raw SQL
    # TODO for speed-up purpose
    """

    def __init__(self) -> None:
        self._uow: UOW = UOW()

    async def get_user(self, user_id: UUID) -> User:
        async with self._uow as uow:
            user: User = await uow.users.get(id=user_id)
        return user

    async def get_all_users(self) -> List[User]:
        async with self._uow as uow:
            users: List[User] = await uow.users.list()
        return users

    async def get_or_create_user(
        self, user_id: UUID, messagebus_handler: GlobalMessageBusHandler
    ) -> User:
        user: User = await self.get_user(user_id=user_id)
        if user:
            return user
        user_commands = UserCommandUseCase(messagebus_handler=messagebus_handler)
        user_created: User = await user_commands.create_user(user_id=user_id)
        return user_created
