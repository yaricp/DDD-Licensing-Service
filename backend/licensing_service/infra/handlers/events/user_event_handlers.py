from ....domain.services.handlers.user_handlers import UserEventHandler
from ....domain.services.events.user_events import UserCreatedEvent

from ....app.services.user_services import UserService


class UserCreatedEventHandler(UserEventHandler):

    async def __call__(self, event: UserCreatedEvent) -> None:
        print("UserCreatedEventHandler call")
        users_service = UserService(
            domain_event_bus=self.domain_event_bus,
            infra_event_bus=self.infra_event_bus
        )
        result = await users_service.first_update_user(event)
        return result
