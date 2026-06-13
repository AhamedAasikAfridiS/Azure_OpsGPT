"""Configured AI provider client factory."""

from app.ai_clients.azure_openai_client import AzureOpenAIClient
from app.ai_clients.base_ai_client import BaseAIClient
from app.ai_clients.gemini_client import GeminiClient
from app.ai_clients.ollama_client import OllamaClient
from app.ai_clients.openai_client import OpenAIClient
from app.core.config import Settings, get_settings


def create_ai_client(settings: Settings | None = None) -> BaseAIClient:
    config = settings or get_settings()

    if config.ai_provider == "ollama":
        return OllamaClient(
            config.ollama_base_url,
            config.ollama_model,
            config.request_timeout_seconds,
        )
    if config.ai_provider == "gemini":
        return GeminiClient(
            config.gemini_api_key,
            config.gemini_model,
            config.request_timeout_seconds,
        )
    if config.ai_provider == "openai":
        return OpenAIClient(
            config.openai_api_key,
            config.openai_model,
            config.request_timeout_seconds,
        )
    if config.ai_provider == "azure_openai":
        return AzureOpenAIClient(
            config.azure_openai_endpoint,
            config.azure_openai_api_key,
            config.azure_openai_deployment,
            config.azure_openai_api_version,
            config.request_timeout_seconds,
        )

    raise ValueError(f"Unsupported AI provider: {config.ai_provider}")
