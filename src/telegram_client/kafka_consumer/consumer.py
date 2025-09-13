import sys
import six
import time
from loguru import logger

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from google.protobuf.json_format import MessageToDict

from telegram.telegram_bot import TelegramBot

from protobuf_types.UserEvents_pb2 import UserEvent
from protobuf_types.TypeMessage_pb2 import TypeMessage
from protobuf_types.TenantEvents_pb2 import TenantEvent
from protobuf_types.LicenseEvents_pb2 import LicenseEvent
from protobuf_types.SubdivisionEvents_pb2 import SubdivisionEvent
from protobuf_types.StatisticRowEvents_pb2 import StatisticRowEvent
from settings import main_config


protobuf_types = {
    "UserEvent": UserEvent,
    "TenantEvent": TenantEvent,
    "LicenseEvent": LicenseEvent,
    "SubdivisionEvent": SubdivisionEvent,
    "StatisticRowEvent": StatisticRowEvent
}


class TelegramKafkaConsumer:

    def __init__(self, tg_bot: TelegramBot):
        self.logger = logger
        self.__tg_bot = tg_bot
        self.__servers = main_config.KAFKA_SERVERS
        self.__topic_name = main_config.KAFKA_TOPICS
        self.__consumer = None

    def parse_protobuf_event(self, event: bytes) -> dict:
        self.logger.info(f"event: {str(event)}")
        try:
            message = TypeMessage()
            message.ParseFromString(event)
            self.logger.info(f"message: {message}")
            protobuf_type = protobuf_types[message.type_name]
            self.logger.info(f"protobuf_type: {protobuf_type}")
            event_obj = protobuf_type()
            event_obj.ParseFromString(event)
            self.logger.info(f"event_obj.action: {event_obj.action}")
            self.logger.info(f"event_obj: {event_obj}")
            event_obj_dict = MessageToDict(
                event_obj, preserving_proto_field_name=True
            )
            self.logger.info(f"event_obj_dict: {event_obj_dict}")
            if "action" not in event_obj_dict:
                event_obj_dict.update({"action": "CREATED"})

        except Exception as err:
            self.logger.error(f"Error: {err}")
        return event_obj_dict

    def render_text(self, event_obj: dict) -> str:
        result_text = f"event: {event_obj}"
        return result_text

    def on_kafka_event(self, event: bytes):
        event_obj = self.parse_protobuf_event(event)
        text = self.render_text(event_obj)
        self.__tg_bot.send_message(text)

    def subscribe(self):
        self.logger.info(f"{self.__consumer.subscription()}")
        try:
            while True:
                for message in self.__consumer:
                    if message is not None:
                        self.logger.info(
                            f"offset: {message.offset}, message: {message.value}"
                        )
                        self.on_kafka_event(message.value)
        finally:
            self.__consumer.close()

    def get_kafka_consumer(self):
        self.logger.info("start get_kafka_consumer")
        self.logger.info(f"servers: {self.__servers}")
        try:
            self.__consumer = KafkaConsumer(
                self.__topic_name,
                auto_offset_reset="earliest",
                bootstrap_servers=self.__servers
            )
            # consumer_timeout_ms=10
        except Exception as ex:
            self.logger.error("Exception while connecting Kafka")
            self.logger.error(str(ex))
        finally:
            return self.__consumer

    def start(self):
        time.sleep(20)
        self.get_kafka_consumer()
        self.subscribe()
