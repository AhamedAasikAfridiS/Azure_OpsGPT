"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpsGPT Alert Ingestion Service"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8002

    database_url: str = (
        "postgresql://opsgpt_alerts:opsgpt_alerts_password@alert-db:5432/"
        "opsgpt_alerts_db"
    )
    ai_analysis_service_url: str = "http://ai-analysis-service:8003"
    core_api_url: str = "http://core-api-service:8001"
    internal_api_key: str = "change-me-internal-key"
    enable_analysis_forwarding: bool = False
    analysis_forward_timeout_seconds: int = 15
    cors_origins: str = "*"

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
