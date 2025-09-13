from pydantic_settings import BaseSettings


class UvicornConfig(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    LOG_LEVEL: str = 'info'
    RELOAD: bool = True


class LinksConfig(BaseSettings):
    HTTP_PROTOCOL: str
    DOMAIN: str


uvicorn_config: UvicornConfig = UvicornConfig()