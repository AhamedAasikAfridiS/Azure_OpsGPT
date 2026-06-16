from typing import Any
from urllib.parse import quote

import httpx

from app.ai_clients.base_ai_client import AIProviderError, BaseAIClient
from app.utils.json_parser import parse_json_object


SYSTEM_MESSAGE = (
    "You are OpsGPT, an AI incident analysis assistant for DevOps, SRE, cloud, "
    "and operations teams. Analyze only the evidence provided. Do not invent "
    "unsupported root causes. Return JSON only."
)


class FoundryAIClient(BaseAIClient):
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str,
        chat_completions_path: str,
        timeout_seconds: int,
        max_retries: int,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.deployment = deployment
        self.api_version = api_version
        self.chat_completions_path = chat_completions_path
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def _url(self) -> str:
        path = self.chat_completions_path.format(
            deployment=quote(self.deployment, safe=""),
            api_version=quote(self.api_version, safe=""),
        )
        return f"{self.endpoint}{path if path.startswith('/') else '/' + path}"

    def _body(self, prompt: str, include_response_format: bool) -> dict[str, Any]:
        body: dict[str, Any] = {
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        if include_response_format:
            body["response_format"] = {"type": "json_object"}
        return body

    def _post(self, prompt: str, include_response_format: bool) -> httpx.Response:
        return httpx.post(
            self._url(),
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            json=self._body(prompt, include_response_format),
            timeout=self.timeout_seconds,
        )

    def generate_json(self, prompt: str) -> dict[str, Any]:
        raw_response: dict[str, Any] | str | None = None
        attempts = max(1, self.max_retries + 1)
        response_format_disabled = False

        for attempt in range(attempts):
            include_response_format = not response_format_disabled
            try:
                response = self._post(prompt, include_response_format=include_response_format)
                raw_response = response.text

                if response.status_code == 400 and include_response_format:
                    response_format_disabled = True
                    response = self._post(prompt, include_response_format=False)
                    raw_response = response.text

                response.raise_for_status()
                payload = response.json()
                raw_response = payload
                content = payload["choices"][0]["message"]["content"]
                return parse_json_object(content)
            except Exception as exc:
                if attempt >= attempts - 1:
                    raise AIProviderError(
                        f"Foundry AI call failed: {exc}",
                        raw_response=raw_response,
                    ) from exc

        raise AIProviderError("Foundry AI call failed without a response", raw_response=raw_response)
