"""Azure Monitor Common Alert Schema parser."""

from typing import Any

from app.schemas.azure_monitor_schema import AzureMonitorPayload
from app.utils.alert_type_mapper import infer_alert_type
from app.utils.severity_mapper import map_azure_severity


def _extract_service_from_resource(resource_id: str | None) -> str | None:
    if not resource_id:
        return None

    parts = [part for part in resource_id.split("/") if part]
    resource_markers = {
        "sites",
        "virtualmachines",
        "servers",
        "managedclusters",
        "containerapps",
    }
    for index, part in enumerate(parts[:-1]):
        if part.lower() in resource_markers:
            return parts[index + 1]
    return parts[-1] if parts else None


def _normalize_environment(value: Any) -> str:
    normalized = str(value or "production").strip().lower()
    aliases = {
        "prod": "production",
        "stage": "staging",
        "stg": "staging",
        "dev": "development",
    }
    return aliases.get(normalized, normalized)


def parse_azure_monitor_alert(
    payload: dict[str, Any],
    fallback_alert_id: str,
) -> dict[str, Any]:
    parsed = AzureMonitorPayload.model_validate(payload)
    essentials = parsed.data.essentials
    custom_properties = parsed.data.custom_properties
    resource_id = (
        essentials.alert_target_ids[0]
        if essentials.alert_target_ids
        else None
    )
    condition_items = (
        parsed.data.alert_context.condition.all_of
        if parsed.data.alert_context
        and parsed.data.alert_context.condition
        else []
    )
    condition = condition_items[0] if condition_items else None
    metric_name = condition.metric_name if condition else None
    message = essentials.description or essentials.alert_rule or ""
    service_name = (
        custom_properties.get("service")
        or (
            essentials.configuration_items[0]
            if essentials.configuration_items
            else None
        )
        or _extract_service_from_resource(resource_id)
        or ""
    )

    return {
        "alert_id": essentials.alert_id or fallback_alert_id,
        "source": "azure_monitor",
        "service_name": str(service_name),
        "alert_type": infer_alert_type(
            metric_name=metric_name,
            message=message,
        ),
        "severity": map_azure_severity(essentials.severity),
        "message": message,
        "description": essentials.description,
        "metric_name": metric_name,
        "metric_value": condition.metric_value if condition else None,
        "threshold": condition.threshold if condition else None,
        "environment": _normalize_environment(
            custom_properties.get("environment")
        ),
        "resource_id": resource_id,
        "dashboard_url": None,
        "runbook_url": custom_properties.get("runbook_url"),
        "fired_at": essentials.fired_at,
        "status": "received",
    }
