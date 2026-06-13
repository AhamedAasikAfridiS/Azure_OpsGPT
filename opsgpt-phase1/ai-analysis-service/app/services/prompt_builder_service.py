"""Structured prompts for real AI providers."""

import json
from typing import Any

from app.schemas.alert_schema import NormalizedAlertInput

JSON_ONLY_INSTRUCTION = """
Return JSON only. Do not include Markdown fences, commentary, or text outside
the JSON object. Base conclusions only on the supplied alert evidence. Do not
invent metrics, systems, events, or remediation results.
""".strip()


def _serialize_alerts(alerts: list[Any]) -> str:
    serialized = []
    for alert in alerts:
        if isinstance(alert, NormalizedAlertInput):
            serialized.append(alert.model_dump(mode="json"))
        else:
            serialized.append(
                {
                    "alert_id": alert.alert_id,
                    "project_id": alert.project_id,
                    "source": alert.source,
                    "service_name": alert.service_name,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "description": alert.description,
                    "environment": alert.environment,
                    "metric_name": alert.metric_name,
                    "metric_value": alert.metric_value,
                    "threshold": alert.threshold,
                    "resource_id": alert.resource_id,
                    "dashboard_url": alert.dashboard_url,
                    "runbook_url": alert.runbook_url,
                    "fired_at": (
                        alert.fired_at.isoformat() if alert.fired_at else None
                    ),
                }
            )
    return json.dumps(serialized, default=str, indent=2)


def build_full_analysis_prompt(
    service_name: str,
    severity: str,
    alerts: list[Any],
) -> str:
    return f"""
You are analyzing an operational incident for service "{service_name}" with
calculated severity "{severity}".

{JSON_ONLY_INSTRUCTION}

Return exactly this structure:
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

Alerts:
{_serialize_alerts(alerts)}
""".strip()


def build_summary_prompt(
    service_name: str,
    severity: str,
    alerts: list[NormalizedAlertInput],
) -> str:
    return f"""
Create a concise operational incident summary for service "{service_name}"
with severity "{severity}".

{JSON_ONLY_INSTRUCTION}

Return exactly:
{{"incident_summary": "string"}}

Alerts:
{_serialize_alerts(alerts)}
""".strip()


def build_rca_prompt(
    service_name: str,
    alerts: list[NormalizedAlertInput],
) -> str:
    return f"""
Determine the most probable root cause for service "{service_name}" from the
provided evidence.

{JSON_ONLY_INSTRUCTION}

Return exactly:
{{
  "root_cause": "string",
  "supporting_evidence": ["string"],
  "confidence_score": 0
}}

Alerts:
{_serialize_alerts(alerts)}
""".strip()


def build_fix_prompt(
    root_cause: str,
    service_name: str,
    severity: str,
) -> str:
    return f"""
Recommend safe operational remediation for service "{service_name}" with
severity "{severity}" and probable root cause:
"{root_cause}"

{JSON_ONLY_INSTRUCTION}

Return exactly:
{{
  "recommended_fix": {{
    "immediate_actions": ["string"],
    "long_term_actions": ["string"],
    "runbook_suggestions": ["string"]
  }}
}}
""".strip()
