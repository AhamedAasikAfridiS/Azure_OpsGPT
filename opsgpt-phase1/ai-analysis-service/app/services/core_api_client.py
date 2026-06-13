"""Internal REST client for the Core API Service."""

from typing import Any

import httpx

from app.core.config import get_settings


class CoreAPIError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    return {
        "X-Internal-API-Key": get_settings().internal_api_key,
        "Content-Type": "application/json",
    }


def create_core_incident(payload: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    try:
        response = httpx.post(
            f"{settings.core_api_url.rstrip('/')}/internal/incidents",
            headers=_headers(),
            json=payload,
            timeout=settings.request_timeout_seconds,
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise CoreAPIError(
            f"Core API incident creation failed: {exc}"
        ) from exc


def update_core_incident_analysis(
    incident_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    settings = get_settings()
    try:
        response = httpx.patch(
            (
                f"{settings.core_api_url.rstrip('/')}/internal/incidents/"
                f"{incident_id}/analysis"
            ),
            headers=_headers(),
            json=payload,
            timeout=settings.request_timeout_seconds,
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise CoreAPIError(
            f"Core API analysis update failed: {exc}"
        ) from exc
