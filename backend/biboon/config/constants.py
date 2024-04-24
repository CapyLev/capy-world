from multiprocessing import cpu_count

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    NAME: str = Field(default="biboon")
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=6900)
    WORKERS: int = Field(default=(cpu_count() * 2 - 1 if not DEBUG else 1))
    VERSION: str = Field(default="0.0.1")
    LOG_LEVEL: str = Field(default="debug")
    ORIGINS: list[str] = Field(default=["*"])
    HTTP_VERSION: int = Field(default=1)
    ADMIN_USER_ID: int = Field(default=0)


class RabbitMQSettings(BaseSettings):
    RABBITMQ_USER: str = Field(default="capy-biboon-rabbitmq-user")
    RABBITMQ_PASS: str = Field(default="capy-biboon-rabbitmq-pass")
    RABBITMQ_HOST: str = Field(default="capy-core-rabbitmq")
    RABBITMQ_VHOST: str = Field(default="capy-biboon-rabbitmq")
    RABBITMQ_PORT: int = Field(default=5672)

    RABBITMQ_MSG_QUEUE_NAME: str = Field(default="message_queue")
    RABBITMQ_MSG_EXCHANGE_NAME: str = Field(default="message_exchange")

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"


class MongoDBSettings(BaseSettings):
    MONGO_NAME: str = Field(default="capy-biboon-db")
    MONGO_COLLECTION: str = Field(default="capy-biboon-realm-collection")
    MONGO_HOST: str = Field(default="mongodb")
    MONGO_PORT: int = Field(default=27017)

    @property
    def MONGO_URL(self) -> str:
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_SINGLE_CONNECTION_CLIENT: bool = Field(default=False)
    AUTO_CLOSE_CONNECTION_POOL_CLIENT: bool = Field(default=False)

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class Constants(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    server: ServerSettings = ServerSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    mongodb: MongoDBSettings = MongoDBSettings()
    redis: RedisSettings = RedisSettings()


constants = Constants()
