from __future__ import annotations

from datetime import datetime
from typing import Any

from app.utils.id_generator import generate_alert_id


ALERT_ID_ALIASES = [
    "alert_id",
    "alertId",
    "id",
    "fingerprint",
    "event_id",
    "eventId",
    "incident_id",
    "incident_key",
    "dedup_key",
    "alert_uid",
    "ruleId",
]
SERVICE_ALIASES = [
    "service",
    "service_name",
    "serviceName",
    "app",
    "application",
    "application_name",
    "component",
    "resource",
    "resourceName",
    "resource_name",
    "project",
    "configurationItem",
    "configurationItems",
    "entity",
    "host",
    "hostname",
    "pod",
    "deployment",
    "workload",
]
SEVERITY_ALIASES = [
    "severity",
    "priority",
    "level",
    "status",
    "state",
    "alert_severity",
    "criticality",
    "severityLevel",
    "NewStateValue",
]
MESSAGE_ALIASES = [
    "message",
    "summary",
    "description",
    "title",
    "alertname",
    "alertName",
    "ruleName",
    "conditionName",
    "reason",
    "details",
    "AlarmDescription",
    "NewStateReason",
    "output",
    "displayName",
    "subject",
]
ENVIRONMENT_ALIASES = ["environment", "env", "stage", "namespace", "cluster", "account", "subscription"]
METRIC_ALIASES = ["metric", "metric_name", "metricName", "name", "query", "measure"]
METRIC_VALUE_ALIASES = ["value", "metric_value", "metricValue", "currentValue", "evalMatches.value", "values", "result"]
THRESHOLD_ALIASES = ["threshold", "limit", "target", "warning", "critical"]
URL_ALIASES = ["dashboardURL", "dashboard_url", "panelURL", "generatorURL", "alertRuleUrl", "source_url", "problemURL", "url"]
RUNBOOK_ALIASES = ["runbook_url", "runbookUrl"]
RESOURCE_ALIASES = ["resource_id", "resourceId", "resource", "resourceName", "host", "hostname", "entity"]
FIRED_AT_ALIASES = ["fired_at", "firedDateTime", "startsAt", "startTime", "timestamp", "time", "created_at"]


def _walk(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}" if path else str(key)
            yield str(key), item, next_path
            yield from _walk(item, next_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            next_path = f"{path}.{index}" if path else str(index)
            yield str(index), item, next_path
            yield from _walk(item, next_path)


def _normalize_key(value: str) -> str:
    return value.replace("_", "").replace("-", "").lower()


def _matches_alias(key: str, path: str, alias: str) -> bool:
    normalized_alias = _normalize_key(alias)
    normalized_key = _normalize_key(key)
    normalized_path = ".".join(_normalize_key(part) for part in path.split(".") if not part.isdigit())
    return (
        normalized_key == normalized_alias
        or normalized_path == normalized_alias
        or normalized_path.endswith(f".{normalized_alias}")
    )


def _find_first(payload: dict[str, Any], aliases: list[str]) -> Any | None:
    for alias in aliases:
        for key, value, path in _walk(payload):
            if _matches_alias(key, path, alias) and value not in (None, ""):
                return value
    return None


def _as_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        for item in value:
            text = _as_text(item)
            if text:
                return text
        return None
    if isinstance(value, dict):
        for key in ("name", "service", "summary", "message", "description", "value"):
            if key in value:
                text = _as_text(value[key])
                if text:
                    return text
        return None
    return str(value).strip() or None


def normalize_severity(value: Any) -> str:
    text = (_as_text(value) or "").lower()
    if text in {"critical", "crit", "sev0", "sev1", "p0", "p1", "high", "error", "firing", "alarm"}:
        return "critical"
    if text in {"warning", "warn", "sev2", "sev3", "p2", "medium", "degraded"}:
        return "warning"
    if text in {"info", "informational", "sev4", "p3", "p4", "low", "resolved", "ok"}:
        return "informational"
    return "informational"


def normalize_environment(value: Any) -> str:
    text = (_as_text(value) or "production").lower()
    if text in {"prod", "production"}:
        return "production"
    if text in {"stage", "staging", "preprod", "pre-production"}:
        return "staging"
    if text in {"dev", "development", "local"}:
        return "development"
    return "production"


def infer_alert_type(*values: Any) -> str:
    text = " ".join(_as_text(value) or "" for value in values).lower()
    if "cpu" in text or "processor" in text:
        return "cpu"
    if "memory" in text or "ram" in text or "oom" in text:
        return "memory"
    if "latency" in text or "response time" in text or "p95" in text or "p99" in text or "duration" in text:
        return "api_latency"
    if "database" in text or "postgres" in text or "mysql" in text or "sql" in text or "connection pool" in text or " db " in f" {text} ":
        return "database"
    if "500" in text or "http error" in text or "exception" in text or "error rate" in text or "stacktrace" in text:
        return "application_error"
    if "disk" in text or "filesystem" in text or "storage" in text:
        return "disk"
    if "network" in text or "packet" in text or "dns" in text or "tcp" in text or "connection" in text:
        return "network"
    if "pod" in text or "container" in text or "kubernetes" in text or "k8s" in text or "crashloop" in text:
        return "kubernetes"
    if "availability" in text or "uptime" in text or "down" in text or "health check" in text:
        return "availability"
    return "custom"


def normalize_alert_type(value: Any, *fallback_values: Any) -> str:
    text = (_as_text(value) or "").lower()
    allowed = {
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
    }
    if text in allowed:
        return text
    return infer_alert_type(*fallback_values)


def _extract_dict(payload: dict[str, Any], key_name: str) -> dict[str, Any] | None:
    for key, value, _path in _walk(payload):
        if _normalize_key(key) == _normalize_key(key_name) and isinstance(value, dict):
            return value
    return None


def _payload_summary(payload: dict[str, Any], source_type: str, parser_used: str, labels: dict[str, Any] | None, annotations: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "source_type": source_type,
        "parser_used": parser_used,
        "top_level_keys": list(payload.keys())[:30],
        "labels_keys": list((labels or {}).keys())[:30],
        "annotations_keys": list((annotations or {}).keys())[:30],
    }


def _confidence(service_name: str, severity_value: Any, message_value: Any, payload: dict[str, Any]) -> int:
    has_service = service_name != "unknown-service"
    has_severity = severity_value not in (None, "")
    has_message = message_value not in (None, "")
    if has_service and has_severity and has_message:
        return 70
    if has_message:
        return 50
    if payload:
        return 30
    return 0


def parse_universal_alert(
    payload: dict[str, Any],
    source_type: str = "custom",
    fallback_alert_id: str | None = None,
    parser_used: str = "universal_alert_parser",
) -> dict[str, Any]:
    labels = _extract_dict(payload, "labels")
    annotations = _extract_dict(payload, "annotations")

    alert_id = _as_text(_find_first(payload, ALERT_ID_ALIASES)) or fallback_alert_id or generate_alert_id()
    service_name = _as_text(_find_first(payload, SERVICE_ALIASES)) or "unknown-service"
    severity_value = _find_first(payload, SEVERITY_ALIASES)
    message_value = _find_first(payload, MESSAGE_ALIASES)
    metric_name = _as_text(_find_first(payload, METRIC_ALIASES))
    metric_value = _find_first(payload, METRIC_VALUE_ALIASES)
    explicit_alert_type = _find_first(payload, ["alert_type", "alertType", "type"])
    threshold = _as_text(_find_first(payload, THRESHOLD_ALIASES))
    environment = normalize_environment(_find_first(payload, ENVIRONMENT_ALIASES))
    dashboard_url = _as_text(_find_first(payload, URL_ALIASES))
    runbook_url = _as_text(_find_first(payload, RUNBOOK_ALIASES))
    resource_id = _as_text(_find_first(payload, RESOURCE_ALIASES))
    fired_at = _as_text(_find_first(payload, FIRED_AT_ALIASES))
    description = _as_text(_find_first(payload, ["description", "details", "body"]))
    message = _as_text(message_value) or f"Alert received from {source_type}"

    parsing_confidence = _confidence(service_name, severity_value, message_value, payload)

    return {
        "alert_id": alert_id,
        "source": source_type,
        "source_type": source_type,
        "service_name": service_name,
        "alert_type": normalize_alert_type(explicit_alert_type, message, description, metric_name, labels, annotations, payload),
        "severity": normalize_severity(severity_value),
        "message": message,
        "description": description,
        "metric_name": metric_name,
        "metric_value": metric_value,
        "threshold": threshold,
        "environment": environment,
        "resource_id": resource_id,
        "dashboard_url": dashboard_url,
        "runbook_url": runbook_url,
        "fired_at": fired_at,
        "labels": labels,
        "annotations": annotations,
        "raw_payload_summary": _payload_summary(payload, source_type, parser_used, labels, annotations),
        "parsing_confidence": parsing_confidence,
        "parser_used": parser_used,
        "status": "received",
    }
