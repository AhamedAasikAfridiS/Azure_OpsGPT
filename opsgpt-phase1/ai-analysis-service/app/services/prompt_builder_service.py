import json
from typing import Any


def _read(alert: Any, name: str) -> Any:
    if isinstance(alert, dict):
        return alert.get(name)
    return getattr(alert, name, None)


def _alert_to_dict(alert: Any) -> dict[str, Any]:
    return {
        "alert_id": _read(alert, "alert_id"),
        "project_id": _read(alert, "project_id"),
        "source": _read(alert, "source"),
        "source_type": _read(alert, "source_type"),
        "service_name": _read(alert, "service_name"),
        "alert_type": _read(alert, "alert_type"),
        "severity": _read(alert, "severity"),
        "message": _read(alert, "message"),
        "description": _read(alert, "description"),
        "metric_name": _read(alert, "metric_name"),
        "metric_value": _read(alert, "metric_value"),
        "threshold": _read(alert, "threshold"),
        "environment": _read(alert, "environment"),
        "resource_id": _read(alert, "resource_id"),
        "dashboard_url": _read(alert, "dashboard_url"),
        "runbook_url": _read(alert, "runbook_url"),
        "labels": _read(alert, "labels"),
        "annotations": _read(alert, "annotations"),
        "raw_payload_summary": _read(alert, "raw_payload_summary"),
        "parsing_confidence": _read(alert, "parsing_confidence"),
        "parser_used": _read(alert, "parser_used"),
        "fired_at": str(_read(alert, "fired_at") or ""),
    }


def _json(data: Any) -> str:
    return json.dumps(data, indent=2, default=str)


def build_full_analysis_prompt(correlation_group: Any, alerts: list[Any]) -> str:
    alert_payload = [_alert_to_dict(alert) for alert in alerts]
    low_confidence = any((alert.get("parsing_confidence") or 50) < 60 for alert in alert_payload)
    return f"""
Analyze the following OpsGPT incident correlation group.

The alerts may come from Grafana, Azure Monitor, Prometheus Alertmanager, Datadog, New Relic,
Splunk, Elastic, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace,
AppDynamics, Zabbix, Nagios, or a custom webhook. Payloads may be dynamic.

Rules:
- Use only the evidence provided.
- Do not invent infrastructure, services, metrics, or causes.
- If evidence is weak or parsing_confidence is low, lower the confidence_score.
- Return JSON only.
- Use this exact JSON shape:
{{
  "incident_summary": "string",
  "root_cause": "string",
  "supporting_evidence": ["string"],
  "confidence_score": 0,
  "recommended_fix": {{
    "immediate_actions": ["string"],
    "long_term_actions": ["string"],
    "runbook_suggestions": ["string"]
  }}
}}

Correlation group:
{_json({
        "correlation_id": getattr(correlation_group, "correlation_id", None),
        "project_id": getattr(correlation_group, "project_id", None),
        "service_name": getattr(correlation_group, "service_name", None),
        "environment": getattr(correlation_group, "environment", None),
        "severity": getattr(correlation_group, "severity", None),
        "related_alert_ids": getattr(correlation_group, "related_alert_ids", None),
        "low_parsing_confidence_present": low_confidence,
    })}

Alerts:
{_json(alert_payload)}
"""


def build_incident_analysis_prompt(correlation_group: Any, alerts: list[Any]) -> str:
    return build_full_analysis_prompt(correlation_group, alerts)


def build_summary_prompt(service_name: str, severity: str, alerts: list[Any]) -> str:
    return build_full_analysis_prompt(
        type(
            "SummaryGroup",
            (),
            {
                "correlation_id": "manual-summary",
                "project_id": None,
                "service_name": service_name,
                "environment": "unknown",
                "severity": severity,
                "related_alert_ids": [],
            },
        )(),
        alerts,
    )


def build_rca_prompt(service_name: str, alerts: list[Any]) -> str:
    return build_summary_prompt(service_name=service_name, severity="unknown", alerts=alerts)


def build_fix_prompt(root_cause: str, service_name: str, severity: str) -> str:
    return f"""
Create recommended incident fixes for this OpsGPT incident.

Service: {service_name}
Severity: {severity}
Root cause: {root_cause}

Rules:
- Use only the supplied root cause.
- Return JSON only.
- Use this JSON shape:
{{
  "recommended_fix": {{
    "immediate_actions": ["string"],
    "long_term_actions": ["string"],
    "runbook_suggestions": ["string"]
  }}
}}
"""
