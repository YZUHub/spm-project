from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str = "/api"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        extra="forbid",
    )


@lru_cache
def get_settings() -> AppConfig:
    return AppConfig()


settings: AppConfig = get_settings()
