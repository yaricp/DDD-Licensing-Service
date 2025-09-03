from backend.core.infra.events import AbstractEvent
from backend.core.infra.handlers import AbstractEventHandler

from ...adapters.kafka_adapter import KafkaAdapter


class ExternalMessageBusSender(AbstractEventHandler):

    async def __call__(self, event: AbstractEvent) -> None:
        print("Start sending to Kafka")
        kafka_adapter = KafkaAdapter()
        await kafka_adapter.send_event_to_kafka(event)
        print("send message to outside broker")
