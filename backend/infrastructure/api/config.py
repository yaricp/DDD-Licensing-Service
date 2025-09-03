from pydantic_settings import BaseSettings
from typing import List


class CORSConfig(BaseSettings):
    ALLOW_ORIGINS: List[str]
    ALLOW_HEADERS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]


cors_config: CORSConfig = CORSConfig()