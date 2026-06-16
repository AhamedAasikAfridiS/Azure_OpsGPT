from app.parsers.universal_alert_parser import parse_universal_alert


def parse_splunk_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "splunk", fallback_alert_id, "splunk_parser")
