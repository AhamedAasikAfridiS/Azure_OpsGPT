from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db"
    core_api_url: str = "http://core-api-service:8001"
    internal_api_key: str = "change-me-internal-key"
    correlation_window_minutes: int = 10
    ai_provider: str = "foundry"
    foundry_endpoint: str = ""
    foundry_api_key: str = ""
    foundry_model_deployment: str = ""
    foundry_api_version: str = "2024-02-15-preview"
    foundry_timeout_seconds: int = 60
    foundry_max_retries: int = 2
    app_env: str = "development"
    cors_origins: str = "*"
    db_init_max_attempts: int = 30
    db_init_delay_seconds: int = 2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
