from app.parsers.parser_registry import parse_alert
from app.utils.id_generator import generate_alert_id


def get_candidate_alert_id(source: str, payload: dict) -> str:
    if source == "azure_monitor":
        return (
            payload.get("data", {})
            .get("essentials", {})
            .get("alertId")
            or generate_alert_id()
        )
    if source == "grafana":
        alerts = payload.get("alerts") or []
        if alerts:
            return alerts[0].get("fingerprint") or generate_alert_id()
    return generate_alert_id()


def normalize_alert(source: str, payload: dict, alert_id: str) -> dict:
    return parse_alert(source_type=source, payload=payload, fallback_alert_id=alert_id)
