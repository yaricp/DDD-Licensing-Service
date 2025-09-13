from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):
    KAFKA_TEST: str = "kafka-test"
    KAFKA_SERVERS: str
    KAFKA_TOPICS: str
    SMTP_SERVER: str
    SMTP_SERVER_PORT: int
    MASTER_EMAIL: str
    SMTP_SERVER_PASSWORD: str
    SMTP_TIMEOUT: int


main_config: MainConfig = MainConfig()
