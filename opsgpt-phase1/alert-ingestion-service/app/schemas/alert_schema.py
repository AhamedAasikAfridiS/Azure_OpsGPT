"""Common normalized alert and API response schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AlertSource(StrEnum):
    azure_monitor = "azure_monitor"
    grafana = "grafana"
    manual = "manual"
    custom = "custom"


class AlertType(StrEnum):
    cpu = "cpu"
    memory = "memory"
    api_latency = "api_latency"
    database = "database"
    application_error = "application_error"
    custom = "custom"


class AlertSeverity(StrEnum):
    critical = "critical"
    warning = "warning"
    informational = "informational"


class AlertEnvironment(StrEnum):
    production = "production"
    staging = "staging"
    development = "development"


class AlertStatus(StrEnum):
    received = "received"
    processed = "processed"
    forwarded = "forwarded"
    failed = "failed"


class NormalizedAlertCreate(BaseModel):
    alert_id: str = Field(min_length=1, max_length=255)
    source: AlertSource
    service_name: str = Field(min_length=1, max_length=160)
    alert_type: AlertType
    severity: AlertSeverity
    message: str = Field(min_length=1)
    description: str | None = None
    metric_name: str | None = Field(default=None, max_length=255)
    metric_value: Any | None = None
    threshold: float | str | None = None
    environment: AlertEnvironment = AlertEnvironment.production
    resource_id: str | None = None
    dashboard_url: str | None = None
    runbook_url: str | None = None
    fired_at: datetime | None = None
    status: AlertStatus = AlertStatus.received


class NormalizedAlertResponse(NormalizedAlertCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RawAlertResponse(BaseModel):
    id: int
    alert_id: str
    source: AlertSource
    raw_payload: dict[str, Any]
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)
