from app.parsers.universal_alert_parser import parse_universal_alert


def parse_prometheus_alertmanager_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "prometheus_alertmanager", fallback_alert_id, "prometheus_alertmanager_parser")
