from uuid import UUID

# ---Domain imports---
from ...domain.aggregates.entities.user import User
from ...domain.services.domain_event_bus import DomainEventBus
from ...domain.services.events.user_events import (
    UserCreatedEvent, UserUpdatedEvent
)
from ...domain.services.uow.user_uow import UserUnitOfWork

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.user_uow import (
    SQLAlchemyUserUnitOfWork as UOW
)
from ...infra.adapters.user_domain_client import (
    Client as UserDomainClient
)


class UserService:
    """
    Service layer core according to DDD,
    which using a unit of work, will perform operations
    on the domain model.
    """

    def __init__(
        self,
        domain_event_bus: DomainEventBus | None = None,
        infra_event_bus: DomainEventBus | None = None
    ) -> None:
        self._domain_event_bus = domain_event_bus
        self._infra_event_bus = infra_event_bus
        self._uow: UserUnitOfWork = UOW()

    async def create_user(self, model: User) -> User:
        async with self._uow as uow:
            print(f"model: {model}")
            user = await uow.users.add(model=model)
            await uow.commit()
            event = UserCreatedEvent(user_id=user.user_id)
            print(f"Add event to infra bus: {event}")
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            print("Exit form create user")
            return user

    async def update_user(
        self, id: UUID, user: User
    ) -> User:
        async with self._uow as uow:
            user: User = await uow.users.update(
                id=id, model=user
            )
            await uow.commit()
            event = UserUpdatedEvent(**await user.to_dict())
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            return user

    async def first_update_user(self, user: User) -> User:
        user_domain_client = UserDomainClient()
        user_data_from_user_domain = user_domain_client.get(id=user.user_id)
        user_data = User(
            **user_data_from_user_domain
        )
        async with self._uow as uow:
            user: User = await uow.users.update(
                id=user_data.user_id, model=user_data
            )
            await uow.commit()
            event = UserUpdatedEvent(**await user.to_dict())
            if self._infra_event_bus:
                self._infra_event_bus.add_event(event)
            return user

    # async def get_all_users(self) -> List[User]:
    #     async with self._uow as uow:
    #         users: List[User] = await uow.users.list()
    #         return users

    # async def get_user(self, id: UUID) -> User:
    #     async with self._uow as uow:
    #         user: User = await uow.users.get(id=id)
    #         return user
        
    # async def delete_user(self, id: UUID) -> User:
    #     async with self._uow as uow:
    #         user: User = await uow.users.delete(id=id)
    #         await uow.commit()
    #         event = UserDeletedEvent(**await user.to_dict())
    #         self._infra_event_bus.add_event(event)
    #         return user

    # async def get_user_by_id(self, id: UUID) -> User:
    #     async with self._uow as uow:
    #         user: Optional[User] = await uow.users.get(id=id)
    #         if not user:
    #             raise UserNotFoundError

    #         return user
