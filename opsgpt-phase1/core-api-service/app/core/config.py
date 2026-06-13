"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpsGPT Core API"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8001

    database_url: str = (
        "postgresql://opsgpt_core:opsgpt_core_password@core-db:5432/"
        "opsgpt_core_db"
    )

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    internal_api_key: str = "change-me-internal-key"

    notification_service_url: str = "http://notification-service:8004"
    enable_notifications: bool = False
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
