from pydantic_settings import BaseSettings


class BrokerConfig(BaseSettings):
    KAFKA_TOPICS: str
    KAFKA_SERVERS: str
    DEFAULT_KAFKA_TOPIC: str


broker_config: BrokerConfig = BrokerConfig()
