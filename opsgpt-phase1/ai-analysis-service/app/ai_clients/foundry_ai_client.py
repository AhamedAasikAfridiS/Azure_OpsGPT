import json
import logging
from typing import Any

import httpx

from app.ai_clients.base_ai_client import AIClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIConfigurationError(RuntimeError):
    pass


class InvalidAIResponseError(RuntimeError):
    def __init__(self, message: str, raw_response: str | None = None) -> None:
        super().__init__(message)
        self.raw_response = raw_response


def foundry_configured() -> bool:
    return bool(settings.foundry_endpoint and settings.foundry_api_key and settings.foundry_model_deployment)


def strip_code_fence(content: str) -> str:
    value = content.strip()
    if value.startswith("```"):
        value = value.split("\n", 1)[1] if "\n" in value else value
        if value.endswith("```"):
            value = value[:-3]
    if value.lower().startswith("json\n"):
        value = value.split("\n", 1)[1]
    return value.strip()


class FoundryAIClient(AIClient):
    async def analyze_incident(self, alerts: list[dict[str, Any]]) -> dict[str, Any]:
        if not foundry_configured():
            raise AIConfigurationError("Foundry configuration is incomplete")

        endpoint = settings.foundry_endpoint.rstrip("/")
        deployment = settings.foundry_model_deployment
        url = f"{endpoint}/openai/deployments/{deployment}/chat/completions"
        params = {"api-version": settings.foundry_api_version}
        headers = {"api-key": settings.foundry_api_key, "Content-Type": "application/json"}
        body = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are OpsGPT, an SRE incident first responder. Return only valid JSON with keys "
                        "incident_summary, root_cause, supporting_evidence, confidence_score, and recommended_fix. "
                        "Do not include markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze these Prometheus Alertmanager normalized alerts. Include alert_name, severity, "
                        "service_name, namespace, cluster, pod, deployment, instance, job, message, description, "
                        "labels, annotations, generator_url, and related alerts in your reasoning.\n\n"
                        f"{json.dumps(alerts, indent=2, default=str)}"
                    ),
                },
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        last_error: Exception | None = None
        for attempt in range(settings.foundry_max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=settings.foundry_timeout_seconds) as client:
                    response = await client.post(url, params=params, headers=headers, json=body)
                    response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                try:
                    parsed = json.loads(strip_code_fence(content))
                except json.JSONDecodeError as exc:
                    raise InvalidAIResponseError("AI response was not valid JSON", content) from exc
                self._validate_output(parsed)
                return parsed
            except InvalidAIResponseError:
                raise
            except Exception as exc:
                last_error = exc
                logger.warning("Foundry analysis attempt %s failed: %s", attempt + 1, exc.__class__.__name__)

        raise RuntimeError(f"Foundry analysis failed: {last_error.__class__.__name__ if last_error else 'unknown'}")

    @staticmethod
    def _validate_output(parsed: dict[str, Any]) -> None:
        required = {"incident_summary", "root_cause", "supporting_evidence", "confidence_score", "recommended_fix"}
        if not isinstance(parsed, dict) or not required.issubset(parsed.keys()):
            raise InvalidAIResponseError("AI response did not match the required JSON shape", json.dumps(parsed, default=str))
