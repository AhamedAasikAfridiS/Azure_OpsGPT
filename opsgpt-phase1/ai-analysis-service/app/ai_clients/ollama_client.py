"""Ollama local-model client."""

from typing import Any

import httpx

from app.ai_clients.base_ai_client import AIProviderError, BaseAIClient
from app.utils.json_parser import parse_json_object


class OllamaClient(BaseAIClient):
    def __init__(self, base_url: str, model: str, timeout: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_json(self, prompt: str) -> dict[str, Any]:
        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "stream": False,
                    "format": "json",
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["message"]["content"]
            return parse_json_object(content)
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise AIProviderError(f"Ollama request failed: {exc}") from exc
