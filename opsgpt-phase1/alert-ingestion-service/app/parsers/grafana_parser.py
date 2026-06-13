"""Grafana webhook parser."""

from typing import Any

from app.schemas.grafana_schema import GrafanaPayload
from app.utils.alert_type_mapper import infer_alert_type
from app.utils.severity_mapper import map_standard_severity


def _normalize_environment(value: str | None) -> str:
    normalized = (value or "production").strip().lower()
    aliases = {
        "prod": "production",
        "stage": "staging",
        "stg": "staging",
        "dev": "development",
    }
    return aliases.get(normalized, normalized)


def parse_grafana_alert(
    payload: dict[str, Any],
    fallback_alert_id: str,
) -> dict[str, Any]:
    parsed = GrafanaPayload.model_validate(payload)
    alert = parsed.alerts[0]
    labels = alert.labels
    annotations = alert.annotations
    alert_name = labels.get("alertname", "")
    message = (
        annotations.get("description")
        or annotations.get("summary")
        or alert_name
    )

    return {
        "alert_id": alert.fingerprint or fallback_alert_id,
        "source": "grafana",
        "service_name": labels.get("service", ""),
        "alert_type": infer_alert_type(
            explicit_type=labels.get("alert_type"),
            message=f"{alert_name} {message}",
        ),
        "severity": map_standard_severity(labels.get("severity")),
        "message": message,
        "description": annotations.get("description"),
        "metric_name": None,
        "metric_value": alert.values,
        "threshold": None,
        "environment": _normalize_environment(labels.get("environment")),
        "resource_id": None,
        "dashboard_url": alert.dashboard_url,
        "runbook_url": annotations.get("runbook_url"),
        "fired_at": alert.starts_at,
        "status": "received",
    }
