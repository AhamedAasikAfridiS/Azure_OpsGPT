from app.parsers.universal_alert_parser import parse_universal_alert


def parse_zabbix_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "zabbix", fallback_alert_id, "zabbix_parser")
