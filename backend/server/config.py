from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str = "/api"

    # Auth grpc service settings
    AUTH_SERVICE_HOST: str
    AUTH_SERVICE_PORT: int

    # Realestate grpc service settings
    REALESTATE_SERVICE_HOST: str
    REALESTATE_SERVICE_PORT: int

    # Valuation grpc service settings
    VALUATION_SERVICE_HOST: str
    VALUATION_SERVICE_PORT: int

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=".env",
        extra="forbid",
    )


@lru_cache
def get_settings() -> AppConfig:
    return AppConfig()


settings: AppConfig = get_settings()
