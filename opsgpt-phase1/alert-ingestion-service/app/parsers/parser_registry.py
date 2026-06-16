from typing import Any, Callable

from app.parsers.appdynamics_parser import parse_appdynamics_alert
from app.parsers.aws_cloudwatch_parser import parse_aws_cloudwatch_alert
from app.parsers.azure_monitor_parser import parse_azure_monitor_alert
from app.parsers.datadog_parser import parse_datadog_alert
from app.parsers.dynatrace_parser import parse_dynatrace_alert
from app.parsers.elastic_parser import parse_elastic_alert
from app.parsers.google_cloud_monitoring_parser import parse_google_cloud_monitoring_alert
from app.parsers.grafana_parser import parse_grafana_alert
from app.parsers.manual_parser import parse_manual_alert
from app.parsers.nagios_parser import parse_nagios_alert
from app.parsers.new_relic_parser import parse_new_relic_alert
from app.parsers.pagerduty_parser import parse_pagerduty_alert
from app.parsers.prometheus_alertmanager_parser import parse_prometheus_alertmanager_alert
from app.parsers.sentry_parser import parse_sentry_alert
from app.parsers.splunk_parser import parse_splunk_alert
from app.parsers.universal_alert_parser import parse_universal_alert
from app.parsers.zabbix_parser import parse_zabbix_alert


PARSER_MAP: dict[str, Callable[[dict[str, Any], str | None], dict[str, Any]]] = {
    "azure_monitor": parse_azure_monitor_alert,
    "grafana": parse_grafana_alert,
    "manual": parse_manual_alert,
    "prometheus_alertmanager": parse_prometheus_alertmanager_alert,
    "datadog": parse_datadog_alert,
    "new_relic": parse_new_relic_alert,
    "splunk": parse_splunk_alert,
    "elastic": parse_elastic_alert,
    "sentry": parse_sentry_alert,
    "pagerduty": parse_pagerduty_alert,
    "aws_cloudwatch": parse_aws_cloudwatch_alert,
    "google_cloud_monitoring": parse_google_cloud_monitoring_alert,
    "dynatrace": parse_dynatrace_alert,
    "appdynamics": parse_appdynamics_alert,
    "zabbix": parse_zabbix_alert,
    "nagios": parse_nagios_alert,
    "custom": lambda payload, fallback_alert_id=None: parse_universal_alert(
        payload,
        source_type="custom",
        fallback_alert_id=fallback_alert_id,
        parser_used="universal_alert_parser",
    ),
}


def _merge_with_universal(
    source_type: str,
    payload: dict[str, Any],
    parsed: dict[str, Any],
    fallback_alert_id: str | None,
) -> dict[str, Any]:
    universal = parse_universal_alert(
        payload,
        source_type=source_type,
        fallback_alert_id=fallback_alert_id,
        parser_used=f"{source_type}_parser",
    )
    merged = {**universal, **parsed}
    merged["source"] = source_type
    merged["source_type"] = source_type
    merged["parser_used"] = f"{source_type}_parser"
    merged["parsing_confidence"] = max(int(universal.get("parsing_confidence", 50)), 90)
    merged["labels"] = merged.get("labels") or universal.get("labels")
    merged["annotations"] = merged.get("annotations") or universal.get("annotations")
    merged["raw_payload_summary"] = merged.get("raw_payload_summary") or universal.get("raw_payload_summary")
    if merged.get("environment") not in {"production", "staging", "development"}:
        merged["environment"] = universal.get("environment", "production")
    if merged.get("severity") not in {"critical", "warning", "informational"}:
        merged["severity"] = universal.get("severity", "informational")
    if merged.get("alert_type") not in {
        "cpu",
        "memory",
        "api_latency",
        "database",
        "application_error",
        "disk",
        "network",
        "kubernetes",
        "availability",
        "custom",
    }:
        merged["alert_type"] = universal.get("alert_type", "custom")
    return merged


def parse_alert(source_type: str, payload: dict[str, Any], fallback_alert_id: str | None = None) -> dict[str, Any]:
    normalized_source_type = source_type or "custom"
    parser = PARSER_MAP.get(normalized_source_type, PARSER_MAP["custom"])
    try:
        parsed = parser(payload, fallback_alert_id)
    except Exception:
        return parse_universal_alert(
            payload,
            source_type=normalized_source_type,
            fallback_alert_id=fallback_alert_id,
            parser_used="universal_alert_parser",
        )

    if normalized_source_type in {"azure_monitor", "grafana", "manual"}:
        return _merge_with_universal(normalized_source_type, payload, parsed, fallback_alert_id)
    return parsed
