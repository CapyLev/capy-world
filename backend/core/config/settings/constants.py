from pydantic import Field
from pydantic_settings import BaseSettings


class BaseEnvSettings(BaseSettings):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


class ServerSettings(BaseEnvSettings):
    SECRET_KEY: str = Field(default='123waewdqdpk)(UE)(@Y(HDihadiansdo9*UY()Q')
    DEBUG: bool = Field(default=True)
    ALLOWED_HOSTS: list[str] = Field(default=['*'])


class DatabaseSettings(BaseEnvSettings):
    ENGINE: str = Field(default='django.db.backends.postgresql')
    DB_NAME: str = Field(default='core-capybara-name')
    DB_USER: str = Field(default='core-capybara-master')
    DB_PASSWORD: str = Field(default='core-capybara-king')
    DB_HOST: str = Field(default='core-capybara-database')
    DB_PORT: int = Field(default=5432)


class ApplicationConsts:
    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()


application_consts: ApplicationConsts = ApplicationConsts()
