from multiprocessing import cpu_count
from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServerSettings(BaseSettings):
    NAME: str = Field(default="ws-server")
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=6969)
    WORKERS: int = Field(default=(cpu_count() * 2 - 1 if not DEBUG else 1))
    VERSION: str = Field(default="0.0.1")
    SECRET: str = Field(default="some ultra secret secret c:")
    TOKEN_LIFETIME: int = Field(default=86400)
    LOG_LEVEL: str = Field(default="debug")
    ORIGINS: list[str] = Field(default=["*"])

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "openapi_prefix": "",
            "redoc_url": None,
            "docs_url": None if self.DEBUG else "/docs",
            "openapi_url": None if self.DEBUG else "/openapi.json",
            "openapi_tags": None
            if self.DEBUG
            else [{"name": "monitor", "description": "uptime monitor endpoints"}],
        }


class RabbitMQSettings(BaseSettings):
    RABBITMQ_USER: str = Field(default='capy-ws-rabbitmq-user')
    RABBITMQ_PASS: str = Field(default='capy-ws-rabbitmq-pass')
    RABBITMQ_HOST: str = Field(default='capy-core-rabbitmq')
    RABBITMQ_VHOST: str = Field(default='capy-ws-rabbitmq')
    RABBITMQ_PORT: int = Field(default='5672')

    RABBITMQ_MSG_QUEUE_NAME: str = Field(default='message_queue')
    RABBITMQ_MSG_EXCHANGE_NAME: str = Field(default='message_exchange')

    @property
    def RABBITMQ_URL(self):
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}'


class MongoDBSettings(BaseSettings):
    NAME: str = Field("capy-ws-server-db", validation_alias="MONGO_DB_NAME")
    COLLECTION: str = Field("capy-ws-server-collection", validation_alias="MONGO_COLLECTION")
    HOST: str = Field("mongodb", validation_alias="MONGO_HOST")
    PORT: int = Field(27017, validation_alias="MONGO_PORT")

    @property
    def MONGO_URL(self) -> str:
        return f"mongodb://{self.HOST}:{self.PORT}"


class Constants(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    server: ServerSettings = ServerSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    mongodb: MongoDBSettings = MongoDBSettings()


constants = Constants()
