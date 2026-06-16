import httpx

from app.core.config import get_settings
from app.schemas.alert_schema import NormalizedAlertCreate


def forward_alert_to_analysis(alert: NormalizedAlertCreate) -> tuple[bool, str | None]:
    settings = get_settings()
    if not settings.enable_analysis_forwarding:
        return False, None

    try:
        response = httpx.post(
            f"{settings.ai_analysis_service_url.rstrip('/')}/analysis/alerts",
            json=alert.model_dump(mode="json"),
            timeout=10,
        )
        response.raise_for_status()
        return True, None
    except Exception as exc:
        return False, str(exc)
