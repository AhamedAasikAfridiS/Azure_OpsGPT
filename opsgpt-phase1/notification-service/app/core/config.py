"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SUPPORTED_CHANNELS = {"slack", "console"}


class Settings(BaseSettings):
    app_name: str = "OpsGPT Notification Service"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8004

    database_url: str = (
        "postgresql://opsgpt_notifications:opsgpt_notifications_password@"
        "notification-db:5432/opsgpt_notifications_db"
    )
    notification_channel: str = "console"
    slack_webhook_url: str = ""
    notification_retry_count: int = Field(default=3, ge=1, le=10)
    notification_timeout_seconds: int = Field(default=10, ge=1, le=120)
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @model_validator(mode="after")
    def validate_channel(self) -> "Settings":
        self.notification_channel = self.notification_channel.strip().lower()
        if self.notification_channel not in SUPPORTED_CHANNELS:
            allowed = ", ".join(sorted(SUPPORTED_CHANNELS))
            raise ValueError(
                f"NOTIFICATION_CHANNEL must be one of: {allowed}"
            )
        if (
            self.notification_channel == "slack"
            and not self.slack_webhook_url.strip()
        ):
            raise ValueError(
                "SLACK_WEBHOOK_URL is required when "
                "NOTIFICATION_CHANNEL=slack"
            )
        return self

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
