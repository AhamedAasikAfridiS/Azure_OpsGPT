"""Core API client for project webhook token validation."""

from dataclasses import dataclass

import httpx

from app.core.config import get_settings


@dataclass(frozen=True)
class ValidatedMonitoringSource:
    project_id: str
    source_type: str
    source_id: str


class ProjectWebhookValidationError(RuntimeError):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


def validate_project_webhook(
    project_id: str,
    webhook_token: str,
) -> ValidatedMonitoringSource:
    settings = get_settings()
    endpoint = (
        f"{settings.core_api_url.rstrip('/')}/internal/projects/"
        f"{project_id}/monitoring-sources/validate"
    )
    try:
        response = httpx.get(
            endpoint,
            params={"token": webhook_token},
            headers={"X-Internal-API-Key": settings.internal_api_key},
            timeout=10,
        )
        if response.status_code in {401, 403, 404}:
            raise ProjectWebhookValidationError(
                "Invalid or inactive project webhook",
                status_code=response.status_code,
            )
        response.raise_for_status()
        payload = response.json()
        return ValidatedMonitoringSource(
            project_id=payload["project_id"],
            source_type=payload["source_type"],
            source_id=payload["source_id"],
        )
    except ProjectWebhookValidationError:
        raise
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
        raise ProjectWebhookValidationError(
            f"Project webhook validation failed: {exc}"
        ) from exc
