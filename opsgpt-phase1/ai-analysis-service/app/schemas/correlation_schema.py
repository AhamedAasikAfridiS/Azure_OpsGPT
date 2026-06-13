"""Correlation request and response schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.alert_schema import AlertSeverity, NormalizedAlertInput


class CorrelationStatus(StrEnum):
    open = "open"
    incident_created = "incident_created"
    updated = "updated"
    closed = "closed"


class CorrelateRequest(BaseModel):
    alerts: list[NormalizedAlertInput] = Field(min_length=1)


class CorrelationGroupResponse(BaseModel):
    id: int
    correlation_id: str
    service_name: str
    environment: str
    severity: AlertSeverity
    status: CorrelationStatus
    related_alert_ids: list[Any]
    incident_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CorrelateResponse(BaseModel):
    groups: list[CorrelationGroupResponse]
