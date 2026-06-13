"""Forward normalized alerts to the AI Analysis Service."""

from dataclasses import dataclass

import httpx

from app.core.config import get_settings
from app.models.normalized_alert import NormalizedAlert
from app.schemas.alert_schema import NormalizedAlertResponse


@dataclass(frozen=True)
class ForwardingResult:
    attempted: bool
    succeeded: bool
    message: str


def forward_to_analysis(alert: NormalizedAlert) -> ForwardingResult:
    settings = get_settings()
    if not settings.enable_analysis_forwarding:
        return ForwardingResult(
            attempted=False,
            succeeded=False,
            message="AI Analysis forwarding is disabled",
        )

    payload = NormalizedAlertResponse.model_validate(alert).model_dump(
        mode="json"
    )
    endpoint = (
        f"{settings.ai_analysis_service_url.rstrip('/')}/analysis/alerts"
    )

    try:
        response = httpx.post(
            endpoint,
            json=payload,
            timeout=settings.analysis_forward_timeout_seconds,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        return ForwardingResult(
            attempted=True,
            succeeded=False,
            message=f"AI Analysis forwarding failed: {exc}",
        )

    return ForwardingResult(
        attempted=True,
        succeeded=True,
        message="Alert forwarded to AI Analysis Service",
    )
