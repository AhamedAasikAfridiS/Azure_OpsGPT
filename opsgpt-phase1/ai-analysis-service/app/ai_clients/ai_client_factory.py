from app.ai_clients.base_ai_client import BaseAIClient
from app.ai_clients.foundry_ai_client import FoundryAIClient
from app.core.config import Settings


def create_ai_client(settings: Settings) -> BaseAIClient:
    return FoundryAIClient(
        endpoint=settings.foundry_endpoint,
        api_key=settings.foundry_api_key,
        deployment=settings.foundry_model_deployment,
        api_version=settings.foundry_api_version,
        chat_completions_path=settings.foundry_chat_completions_path,
        timeout_seconds=settings.foundry_timeout_seconds,
        max_retries=settings.foundry_max_retries,
    )
