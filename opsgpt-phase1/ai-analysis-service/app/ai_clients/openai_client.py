"""OpenAI API client."""

from typing import Any

import httpx

from app.ai_clients.base_ai_client import AIProviderError, BaseAIClient
from app.utils.json_parser import parse_json_object


class OpenAIClient(BaseAIClient):
    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate_json(self, prompt: str) -> dict[str, Any]:
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return parse_json_object(content)
        except (httpx.HTTPError, IndexError, KeyError, TypeError, ValueError) as exc:
            raise AIProviderError(f"OpenAI request failed: {exc}") from exc
