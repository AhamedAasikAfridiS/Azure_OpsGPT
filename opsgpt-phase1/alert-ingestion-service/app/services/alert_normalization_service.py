"""Source selection and normalization orchestration."""

from typing import Any

from app.parsers.azure_monitor_parser import parse_azure_monitor_alert
from app.parsers.grafana_parser import parse_grafana_alert
from app.parsers.manual_parser import parse_manual_alert
from app.utils.id_generator import generate_alert_id


def get_candidate_alert_id(
    source: str,
    payload: dict[str, Any],
) -> str:
    if source == "azure_monitor":
        data = payload.get("data")
        essentials = data.get("essentials") if isinstance(data, dict) else None
        alert_id = (
            essentials.get("alertId")
            if isinstance(essentials, dict)
            else None
        )
        return str(alert_id) if alert_id else generate_alert_id()

    if source == "grafana":
        alerts = payload.get("alerts")
        first_alert = (
            alerts[0]
            if isinstance(alerts, list)
            and alerts
            and isinstance(alerts[0], dict)
            else None
        )
        fingerprint = (
            first_alert.get("fingerprint")
            if isinstance(first_alert, dict)
            else None
        )
        return str(fingerprint) if fingerprint else generate_alert_id()

    return generate_alert_id()


def normalize_alert(
    source: str,
    payload: dict[str, Any],
    alert_id: str,
) -> dict[str, Any]:
    if source == "azure_monitor":
        return parse_azure_monitor_alert(payload, alert_id)
    if source == "grafana":
        return parse_grafana_alert(payload, alert_id)
    if source == "manual":
        return parse_manual_alert(payload, alert_id)
    if source == "custom":
        normalized = parse_manual_alert(payload, alert_id)
        normalized["source"] = "custom"
        return normalized
    raise ValueError(f"Unsupported alert source: {source}")
