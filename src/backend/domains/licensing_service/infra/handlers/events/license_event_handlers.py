from ....app.services.tenant_services import TenantService
from ....domain.services.events.license_events import LicenseActivatedEvent
from ....domain.services.handlers.license_handlers import LicenseEventHandler


class LicenseActivatedEventHandler(LicenseEventHandler):

    async def __call__(self, event: LicenseActivatedEvent) -> None:
        # send_vote_notification_message.delay(**await event.to_dict())
        print(f"event handler event: {event}")
        tenant_services = TenantService(
            domain_event_bus=self.domain_event_bus, infra_event_bus=self.infra_event_bus
        )
        result = await tenant_services.update_list_all_active_licenses(event)
        return result


class LicenseDeactivatedEventHandler(LicenseEventHandler):

    async def __call__(self, event: LicenseActivatedEvent) -> None:
        # send_vote_notification_message.delay(**await event.to_dict())
        # print(f"event handler event: {event}")
        # tenant_services = TenantService(
        #     domain_event_bus=self.domain_event_bus,
        #     infra_event_bus=self.infra_event_bus
        # )
        # result = await tenant_services.update_list_all_active_licenses(event)
        # return result
        pass
