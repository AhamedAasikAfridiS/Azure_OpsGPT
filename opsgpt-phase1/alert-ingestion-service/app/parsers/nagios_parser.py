from app.parsers.universal_alert_parser import parse_universal_alert


def parse_nagios_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "nagios", fallback_alert_id, "nagios_parser")
