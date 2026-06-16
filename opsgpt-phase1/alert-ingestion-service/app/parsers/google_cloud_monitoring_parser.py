from app.parsers.universal_alert_parser import parse_universal_alert


def parse_google_cloud_monitoring_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "google_cloud_monitoring", fallback_alert_id, "google_cloud_monitoring_parser")
