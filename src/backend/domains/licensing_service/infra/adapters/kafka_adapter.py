import sys
from datetime import datetime
from uuid import uuid4

import six
from sqlalchemy import UUID as ALCH_UUID

if sys.version_info >= (3, 12, 0):
    sys.modules["kafka.vendor.six.moves"] = six.moves

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError

from backend.core.infra.events import AbstractEvent
from backend.core.infra.outside_broker.connection import (
    DEFAULT_KAFKA_TOPIC,
    KAFKA_SERVERS,
    KAFKA_TOPICS,
)

from ...domain.services.events.license_events import (
    LicenseActivatedEvent,
    LicenseCreatedEvent,
)
from ...domain.services.events.statistic_row_events import StatisticRowAddedEvent
from ...domain.services.events.subdivision_events import (
    SubdivisionCreatedEvent,
    SubdivisionDeletedEvent,
    SubdivisionLicenseExpiredEvent,
    SubdivisionUpdatedEvent,
)
from ...domain.services.events.tenant_events import (
    TenantCreatedEvent,
    TenantDeletedEvent,
    TenantUpdatedEvent,
)
from ...domain.services.events.user_events import UserCreatedEvent, UserUpdatedEvent
from ..protobuf_types.LicenseEvents_pb2 import LicenseEvent
from ..protobuf_types.StatisticRowEvents_pb2 import StatisticRowEvent
from ..protobuf_types.SubdivisionEvents_pb2 import SubdivisionEvent
from ..protobuf_types.TenantEvents_pb2 import TenantEvent
from ..protobuf_types.UserEvents_pb2 import UserEvent

protobuf_types = {
    UserCreatedEvent: UserEvent,
    UserUpdatedEvent: UserEvent,
    TenantCreatedEvent: TenantEvent,
    TenantUpdatedEvent: TenantEvent,
    TenantDeletedEvent: TenantEvent,
    LicenseCreatedEvent: LicenseEvent,
    LicenseActivatedEvent: LicenseEvent,
    SubdivisionCreatedEvent: SubdivisionEvent,
    SubdivisionUpdatedEvent: SubdivisionEvent,
    SubdivisionDeletedEvent: SubdivisionEvent,
    SubdivisionLicenseExpiredEvent: SubdivisionEvent,
    StatisticRowAddedEvent: StatisticRowEvent,
}


def create_topics(
    kafka_servers: list = KAFKA_SERVERS, topics: list = KAFKA_TOPICS
) -> None:
    print(f"kafka_servers: {kafka_servers}")
    print(f"topics: {topics}")

    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_servers, api_version=(1, 0, 0)
    )
    consumer = KafkaConsumer(
        bootstrap_servers=kafka_servers,
    )

    existing_topic_list = consumer.topics()
    print(existing_topic_list)
    topic_list = []
    for topic in topics:
        if topic not in existing_topic_list:
            print("Topic : {} added ".format(topic))
            topic_list.append(
                NewTopic(name=topic, num_partitions=1, replication_factor=1)
            )
        else:
            print("Topic : {topic} already exist ")
    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("Topic Created Successfully")
        else:
            print("Topic Exist")
    except TopicAlreadyExistsError as e:
        print(f"Topic Already Exist: {e}")
    except Exception as e:
        print(f"Error: {e}")


class KafkaAdapter:

    def __init__(
        self, topic: str = DEFAULT_KAFKA_TOPIC, kafka_servers: list = KAFKA_SERVERS
    ) -> None:
        try:
            self.topic = topic
            self.__producer = KafkaProducer(bootstrap_servers=kafka_servers)
        except Exception as err:
            print(f"Error: {err}")

    async def prepare_message(self, event: AbstractEvent) -> str:
        print(f"Prepare_message event: {event}")
        protobuf_type = protobuf_types[type(event)]
        message = protobuf_type()
        print(f"type protobuf: {type(message).__name__}")
        type_message = type(message).__name__

        dict_event = await event.to_dict()
        dict_event["type_name"] = type_message
        for key, value in dict_event.items():
            if str(type(value)).find("UUID") != -1:
                value = str(value)
            try:
                setattr(message, key, value)
            except Exception as err:
                print(f"{message},{key},{value}")
                print(f"Error: {err}")
        if "action" in dict_event:
            print(f"dict_event.action: {dict_event['action']}")
            message.action = int(dict_event["action"])
            print(f"message.action: {message.action}")

        print(f"message: {message}")
        return message.SerializeToString()

    async def send_event_to_kafka(self, event: AbstractEvent) -> None:
        """
        Sends message to kafka broker
        """
        try:
            kafka_mess = await self.prepare_message(event)
            print(f"kafka_mess: {kafka_mess}")
            self.__producer.send(self.topic, key=uuid4().bytes, value=kafka_mess)
            self.__producer.flush()
            print("Message sent to Kafka")
        except Exception as e:
            print(f"Error: {e}")
