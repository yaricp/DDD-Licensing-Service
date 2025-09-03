from pydantic_settings import BaseSettings


class RestAPIConfig(BaseSettings):
    API_PREFIX: str = "licensing_service"


rest_api_config: RestAPIConfig = RestAPIConfig()
