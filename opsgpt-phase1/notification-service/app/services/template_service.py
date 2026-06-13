"""Code-based Phase 1 notification templates."""

from app.schemas.notification_schema import NotificationEventRequest
from app.utils.message_formatter import format_action_list, format_template

EVENT_TEMPLATES = {
    "incident_created": """
\U0001F6A8 New Incident Created

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}
Severity: {severity}
Status: {status}

Title:
{title}
""",
    "critical_incident_created": """
\U0001F6A8 Critical Incident Detected

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}
Severity: {severity}
Status: {status}

Title:
{title}

Likely Root Cause:
{root_cause}

Confidence:
{confidence_score}%

Recommended Fix:
{immediate_actions}
""",
    "ai_analysis_completed": """
\U0001F9E0 AI Analysis Completed

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}
Severity: {severity}

Summary:
{ai_summary}

Likely Root Cause:
{root_cause}

Confidence:
{confidence_score}%

Recommended Immediate Actions:
{immediate_actions}
""",
    "incident_status_updated": """
\U0001F504 Incident Status Updated

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}
Status: {status}
""",
    "incident_resolved": """
\u2705 Incident Resolved

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}
Resolved By: {resolved_by}

Resolution Notes:
{resolution_notes}
""",
    "resolution_notes_added": """
\U0001F4DD Resolution Notes Added

Incident ID: {incident_id}
Project: {project_name}
Service: {service_name}

Notes:
{resolution_notes}
""",
}


def format_event_message(payload: NotificationEventRequest) -> str:
    recommended_fix = payload.recommended_fix
    immediate_actions = (
        recommended_fix.immediate_actions if recommended_fix else []
    )
    values = {
        **payload.model_dump(mode="python"),
        "immediate_actions": format_action_list(immediate_actions),
    }
    return format_template(
        EVENT_TEMPLATES[payload.event_type.value],
        values,
    )
