from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = (
        "postgresql://opsgpt_analysis:opsgpt_analysis_password@analysis-db:5432/opsgpt_analysis_db"
    )
    core_api_url: str = "http://core-api-service:8001"
    internal_api_key: str = "change-me-internal-key"
    correlation_window_minutes: int = 10
    request_timeout_seconds: int = 15

    ai_provider: str = "foundry"
    foundry_endpoint: str = ""
    foundry_api_key: str = ""
    foundry_model_deployment: str = ""
    foundry_api_version: str = "2024-02-15-preview"
    foundry_timeout_seconds: int = Field(default=60, ge=1, le=600)
    foundry_max_retries: int = Field(default=2, ge=0, le=5)
    foundry_chat_completions_path: str = (
        "/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    )

    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("ai_provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized != "foundry":
            raise ValueError("AI_PROVIDER must be 'foundry' for OpsGPT Phase 1")
        return normalized

    @field_validator("foundry_endpoint", "foundry_api_key", "foundry_model_deployment")
    @classmethod
    def validate_foundry_required(cls, value: str, info):
        if not value:
            raise ValueError(f"{info.field_name.upper()} is required when AI_PROVIDER=foundry")
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins or self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
