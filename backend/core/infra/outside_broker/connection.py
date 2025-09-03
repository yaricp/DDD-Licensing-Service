from .config import broker_config


DEFAULT_KAFKA_TOPIC = broker_config.DEFAULT_KAFKA_TOPIC
KAFKA_TOPICS = broker_config.KAFKA_TOPICS.replace(" ", "").split(",")
KAFKA_SERVERS = broker_config.KAFKA_SERVERS.replace(" ", "").split(",")
