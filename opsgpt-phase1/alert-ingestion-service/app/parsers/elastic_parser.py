from app.parsers.universal_alert_parser import parse_universal_alert


def parse_elastic_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "elastic", fallback_alert_id, "elastic_parser")
