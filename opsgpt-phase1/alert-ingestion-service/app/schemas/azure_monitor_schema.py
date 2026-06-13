"""Azure Monitor Common Alert Schema payload models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AzureEssentials(BaseModel):
    alert_id: str | None = Field(default=None, alias="alertId")
    alert_rule: str | None = Field(default=None, alias="alertRule")
    severity: str | None = None
    signal_type: str | None = Field(default=None, alias="signalType")
    monitor_condition: str | None = Field(
        default=None, alias="monitorCondition"
    )
    monitoring_service: str | None = Field(
        default=None, alias="monitoringService"
    )
    alert_target_ids: list[str] = Field(
        default_factory=list, alias="alertTargetIDs"
    )
    configuration_items: list[str] = Field(
        default_factory=list, alias="configurationItems"
    )
    fired_at: str | None = Field(default=None, alias="firedDateTime")
    description: str | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class AzureConditionItem(BaseModel):
    metric_name: str | None = Field(default=None, alias="metricName")
    operator: str | None = None
    threshold: float | str | None = None
    metric_value: Any | None = Field(default=None, alias="metricValue")

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class AzureCondition(BaseModel):
    all_of: list[AzureConditionItem] = Field(
        default_factory=list, alias="allOf"
    )

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class AzureAlertContext(BaseModel):
    condition: AzureCondition | None = None

    model_config = ConfigDict(extra="allow")


class AzureAlertData(BaseModel):
    essentials: AzureEssentials
    alert_context: AzureAlertContext | None = Field(
        default=None, alias="alertContext"
    )
    custom_properties: dict[str, Any] = Field(
        default_factory=dict, alias="customProperties"
    )

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class AzureMonitorPayload(BaseModel):
    schema_id: str | None = Field(default=None, alias="schemaId")
    data: AzureAlertData

    model_config = ConfigDict(extra="allow", populate_by_name=True)
