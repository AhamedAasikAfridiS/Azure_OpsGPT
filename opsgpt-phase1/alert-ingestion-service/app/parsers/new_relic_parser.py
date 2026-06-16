from app.parsers.universal_alert_parser import parse_universal_alert


def parse_new_relic_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "new_relic", fallback_alert_id, "new_relic_parser")
