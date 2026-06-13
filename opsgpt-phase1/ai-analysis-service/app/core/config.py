"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SUPPORTED_AI_PROVIDERS = {"ollama", "gemini", "openai", "azure_openai"}


class Settings(BaseSettings):
    app_name: str = "OpsGPT AI Analysis Service"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8003

    database_url: str = (
        "postgresql://opsgpt_analysis:opsgpt_analysis_password@analysis-db:"
        "5432/opsgpt_analysis_db"
    )
    core_api_url: str = "http://core-api-service:8001"
    internal_api_key: str = "change-me-internal-key"
    correlation_window_minutes: int = Field(default=10, ge=1, le=1440)
    request_timeout_seconds: int = Field(default=60, ge=1, le=600)

    ai_provider: str

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = ""

    gemini_api_key: str = ""
    gemini_model: str = ""

    openai_api_key: str = ""
    openai_model: str = ""

    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = ""
    azure_openai_api_version: str = ""

    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @model_validator(mode="after")
    def validate_selected_provider(self) -> "Settings":
        self.ai_provider = self.ai_provider.strip().lower()
        if self.ai_provider not in SUPPORTED_AI_PROVIDERS:
            allowed = ", ".join(sorted(SUPPORTED_AI_PROVIDERS))
            raise ValueError(
                f"AI_PROVIDER must be one of: {allowed}"
            )

        required_by_provider = {
            "ollama": {
                "OLLAMA_BASE_URL": self.ollama_base_url,
                "OLLAMA_MODEL": self.ollama_model,
            },
            "gemini": {
                "GEMINI_API_KEY": self.gemini_api_key,
                "GEMINI_MODEL": self.gemini_model,
            },
            "openai": {
                "OPENAI_API_KEY": self.openai_api_key,
                "OPENAI_MODEL": self.openai_model,
            },
            "azure_openai": {
                "AZURE_OPENAI_ENDPOINT": self.azure_openai_endpoint,
                "AZURE_OPENAI_API_KEY": self.azure_openai_api_key,
                "AZURE_OPENAI_DEPLOYMENT": self.azure_openai_deployment,
                "AZURE_OPENAI_API_VERSION": self.azure_openai_api_version,
            },
        }
        missing = [
            name
            for name, value in required_by_provider[self.ai_provider].items()
            if not value.strip()
        ]
        if missing:
            raise ValueError(
                f"Missing configuration for AI_PROVIDER={self.ai_provider}: "
                + ", ".join(missing)
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
