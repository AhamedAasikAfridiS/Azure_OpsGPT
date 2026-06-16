from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class AlertSource(StrEnum):
    azure_monitor = "azure_monitor"
    grafana = "grafana"
    prometheus_alertmanager = "prometheus_alertmanager"
    datadog = "datadog"
    new_relic = "new_relic"
    splunk = "splunk"
    elastic = "elastic"
    sentry = "sentry"
    pagerduty = "pagerduty"
    aws_cloudwatch = "aws_cloudwatch"
    google_cloud_monitoring = "google_cloud_monitoring"
    dynatrace = "dynatrace"
    appdynamics = "appdynamics"
    zabbix = "zabbix"
    nagios = "nagios"
    manual = "manual"
    custom = "custom"


class AlertType(StrEnum):
    cpu = "cpu"
    memory = "memory"
    api_latency = "api_latency"
    database = "database"
    application_error = "application_error"
    disk = "disk"
    network = "network"
    kubernetes = "kubernetes"
    availability = "availability"
    custom = "custom"


class Severity(StrEnum):
    critical = "critical"
    warning = "warning"
    informational = "informational"


class Environment(StrEnum):
    production = "production"
    staging = "staging"
    development = "development"


class AlertStatus(StrEnum):
    received = "received"
    processed = "processed"
    forwarded = "forwarded"
    failed = "failed"


class NormalizedAlertCreate(BaseModel):
    alert_id: str
    project_id: str | None = None
    source: AlertSource
    source_type: AlertSource | None = None
    service_name: str
    alert_type: AlertType
    severity: Severity
    message: str
    description: str | None = None
    metric_name: str | None = None
    metric_value: Any | None = None
    threshold: str | None = None
    environment: Environment = Environment.production
    resource_id: str | None = None
    dashboard_url: str | None = None
    runbook_url: str | None = None
    fired_at: datetime | None = None
    labels: dict[str, Any] | None = None
    annotations: dict[str, Any] | None = None
    raw_payload_summary: dict[str, Any] | None = None
    parsing_confidence: int = 50
    parser_used: str | None = None
    status: AlertStatus = AlertStatus.received


class NormalizedAlertResponse(NormalizedAlertCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RawAlertResponse(BaseModel):
    id: int
    alert_id: str
    project_id: str | None = None
    source: str
    raw_payload: dict[str, Any]
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertIngestionResponse(BaseModel):
    alert_id: str
    project_id: str | None = None
    status: AlertStatus
    forwarding_status: str
    message: str


class ProjectSourceValidationResponse(BaseModel):
    valid: bool
    project_id: str
    source_type: AlertSource
    source_id: str
