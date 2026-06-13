"""Google Gemini API client."""

from typing import Any

import httpx

from app.ai_clients.base_ai_client import AIProviderError, BaseAIClient
from app.utils.json_parser import parse_json_object


class GeminiClient(BaseAIClient):
    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate_json(self, prompt: str) -> dict[str, Any]:
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        try:
            response = httpx.post(
                endpoint,
                params={"key": self.api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    },
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["candidates"][0]["content"]["parts"][0][
                "text"
            ]
            return parse_json_object(content)
        except (httpx.HTTPError, IndexError, KeyError, TypeError, ValueError) as exc:
            raise AIProviderError(f"Gemini request failed: {exc}") from exc
