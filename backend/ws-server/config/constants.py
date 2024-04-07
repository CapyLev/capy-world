from multiprocessing import cpu_count
from typing import Any, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    NAME: str = "ws-server"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = "6968"
    WORKERS: int = cpu_count() * 2 - 1 if not DEBUG else 1
    VERSION: str = "0.0.1"
    SECRET: str = "some ultra secret secret c:"
    TOKEN_LIFETIME: int = 86400
    LOG_LEVEL: str = "debug"
    ORIGINS: list[str] = ["*"]

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "openapi_prefix": "",
            "redoc_url": None,
            "docs_url": None if self.ENV_MODE != "dev" else "/docs",
            "openapi_url": None if self.ENV_MODE != "dev" else "/openapi.json",
            "openapi_tags": None
            if self.ENV_MODE != "dev"
            else [{"name": "monitor", "description": "uptime monitor endpoints"}],
        }


class RabbitMQSettings(BaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    @property
    def RABBITMQ_URL(self):
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_LOCAL_HOST_NAME}:{self.RABBITMQ_LOCAL_PORT}/'


class Constants(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    server: ServerSettings = ServerSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()


constants = Constants()
