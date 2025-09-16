from ....domain.services.events.tenant_events import TenantCreatedEvent
from ....domain.services.handlers.tenant_handlers import TenantEventHandler


class TenantCreatedEventHandler(TenantEventHandler):

    async def __call__(self, event: TenantCreatedEvent) -> None:
        # send_vote_notification_message.delay(**await event.to_dict())
        print("Tenant event!!!")
