from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db"
    auth_provider: str = "local"
    allow_local_auth: bool = True
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_api_audience: str = ""
    azure_issuer: str = ""
    azure_jwks_url: str = ""
    entra_role_admin: str = "OpsGPT.Admin"
    entra_role_senior: str = "OpsGPT.Senior"
    entra_role_junior: str = "OpsGPT.Junior"
    internal_api_key: str = "change-me-internal-key"
    notification_service_url: str = "http://notification-service:8004"
    enable_notifications: bool = True
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

    @property
    def uses_entra_auth(self) -> bool:
        return self.auth_provider.strip().lower() == "entra"

    @property
    def resolved_azure_issuer(self) -> str:
        if self.azure_issuer.strip():
            return self.azure_issuer.strip()
        if self.azure_tenant_id.strip():
            return f"https://login.microsoftonline.com/{self.azure_tenant_id.strip()}/v2.0"
        return ""

    @property
    def resolved_azure_jwks_url(self) -> str:
        if self.azure_jwks_url.strip():
            return self.azure_jwks_url.strip()
        if self.azure_tenant_id.strip():
            return f"https://login.microsoftonline.com/{self.azure_tenant_id.strip()}/discovery/v2.0/keys"
        return ""


settings = Settings()
