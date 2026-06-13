"""Azure OpenAI client prepared for Phase 2 configuration."""

from typing import Any
from urllib.parse import quote

import httpx

from app.ai_clients.base_ai_client import AIProviderError, BaseAIClient
from app.utils.json_parser import parse_json_object


class AzureOpenAIClient(BaseAIClient):
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str,
        timeout: int,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.deployment = deployment
        self.api_version = api_version
        self.timeout = timeout

    def generate_json(self, prompt: str) -> dict[str, Any]:
        deployment = quote(self.deployment, safe="")
        url = (
            f"{self.endpoint}/openai/deployments/{deployment}/chat/completions"
        )
        try:
            response = httpx.post(
                url,
                params={"api-version": self.api_version},
                headers={
                    "api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return parse_json_object(content)
        except (httpx.HTTPError, IndexError, KeyError, TypeError, ValueError) as exc:
            raise AIProviderError(
                f"Azure OpenAI request failed: {exc}"
            ) from exc
