from app.parsers.universal_alert_parser import parse_universal_alert


def parse_appdynamics_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "appdynamics", fallback_alert_id, "appdynamics_parser")
