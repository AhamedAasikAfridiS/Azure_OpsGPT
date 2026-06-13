"""Normalized alert schemas accepted from Alert Ingestion."""

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


class NormalizedAlertInput(BaseModel):
    alert_id: str = Field(min_length=1, max_length=255)
    project_id: str | None = Field(default=None, max_length=50)
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
    status: AlertStatus = AlertStatus.processed

    model_config = ConfigDict(extra="ignore")


class StoredAnalysisAlertResponse(BaseModel):
    id: int
    alert_id: str
    project_id: str | None
    source: AlertSource
    service_name: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    description: str | None
    environment: AlertEnvironment
    metric_name: str | None
    metric_value: Any | None
    threshold: str | None
    resource_id: str | None
    dashboard_url: str | None
    runbook_url: str | None
    fired_at: datetime | None
    received_at: datetime
    is_duplicate: bool

    model_config = ConfigDict(from_attributes=True)
