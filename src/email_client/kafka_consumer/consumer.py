import sys
import six
import time
from loguru import logger

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from google.protobuf.json_format import MessageToDict

from protobuf_types.UserEvents_pb2 import UserEvent
from protobuf_types.TypeMessage_pb2 import TypeMessage
from protobuf_types.PartnerEvents_pb2 import PartnerEvent
from protobuf_types.AttractionEvents_pb2 import AttractionEvent
from protobuf_types.LicenseEvents_pb2 import LicenseEvent
from protobuf_types.StatisticRowEvents_pb2 import StatisticRowEvent

from email_sender.client import MailMessage
from settings import main_config
from template_renderer import TemplateRenderer


protobuf_types = {
    "UserEvent": UserEvent,
    "PartnerEvent": PartnerEvent,
    "LicenseEvent": LicenseEvent,
    "AttractionEvent": AttractionEvent,
    "StatisticRowEvent": StatisticRowEvent
}


class EmailKafkaConsumer:

    def __init__(self):
        self.logger = logger
        self.__email_client = MailMessage()
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
            self.logger.info(f"event_obj: {event_obj}")
            event_obj_dict = MessageToDict(
                event_obj, preserving_proto_field_name=True
            )
            if "action" not in event_obj_dict:
                event_obj_dict.update({"action": "CREATED"})
        except Exception as err:
            self.logger.error(f"Error: {err}")
        return event_obj_dict

    def prepare_message(
        self, event_obj: dict, template: str = 'default_mail.html'
    ) -> tuple:
        
        email = event_obj["email"] if "email" in event_obj else ""
        action = event_obj["action"] if "action" in event_obj else ""
        self.logger.info(f"Action: {action}")
        template_vars = {
            "type_name": event_obj["type_name"],
            "action": action,
            "items": [
                {"key": k, "value": v} for k, v in event_obj.items()
            ]
        }
        subject = f"{event_obj['type_name']}-{action}"
        message = TemplateRenderer(
            template=template,
            template_vars=template_vars
        ).render()
        return subject, message, email

    def send_email(
        self,
        subject: str,
        text_message: str,
        email: str = ""
    ) -> None:
        self.logger.info(f"Start sending {subject} {text_message}")
        if email:
            self.__email_client.send(
                email=email,
                subject=subject,
                message=text_message
            )
        self.__email_client.send(
            email=main_config.MASTER_EMAIL,
            subject=subject,
            message=text_message
        )
        self.logger.info("After all email sending")
        return

    def on_kafka_event(self, event: bytes):
        event_obj = self.parse_protobuf_event(event)
        subject, message, email = self.prepare_message(event_obj)
        self.send_email(
            subject=subject, text_message=message, email=email
        )

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
        time.sleep(30)
        self.get_kafka_consumer()
        self.subscribe()
