from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):

    KAFKA_SERVERS: str
    KAFKA_TOPICS: str
    TELEGRAM_BOT_TOKEN: str
    ADMIN_CHAT_ID: str
    KAFKA_TEST: str = "kafka-test"


main_config: MainConfig = MainConfig()
# print(MainConfig().model_dump())