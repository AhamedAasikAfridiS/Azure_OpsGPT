from app.parsers.universal_alert_parser import parse_universal_alert


def parse_pagerduty_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "pagerduty", fallback_alert_id, "pagerduty_parser")
