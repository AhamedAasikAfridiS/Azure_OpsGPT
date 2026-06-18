"""Manual alert submission schema."""

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.alert_schema import (
    Environment,
    Severity,
    AlertType,
)


class ManualAlertRequest(BaseModel):
    service_name: str = Field(min_length=1, max_length=160)
    alert_type: AlertType
    severity: Severity
    message: str = Field(min_length=1)
    description: str | None = None
    environment: Environment = Environment.production
    metric_name: str | None = Field(default=None, max_length=255)
    metric_value: Any | None = None
    threshold: float | str | None = None
    resource_id: str | None = None
    dashboard_url: str | None = None
    runbook_url: str | None = None
    fired_at: str | None = None
