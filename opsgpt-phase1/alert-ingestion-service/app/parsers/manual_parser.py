"""Manual alert parser."""

from typing import Any

from app.schemas.manual_alert_schema import ManualAlertRequest


def parse_manual_alert(
    payload: dict[str, Any],
    alert_id: str,
) -> dict[str, Any]:
    parsed = ManualAlertRequest.model_validate(payload)
    return {
        "alert_id": alert_id,
        "source": "manual",
        **parsed.model_dump(mode="json"),
        "status": "received",
    }
