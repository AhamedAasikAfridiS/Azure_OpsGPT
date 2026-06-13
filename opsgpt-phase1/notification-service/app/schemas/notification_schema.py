"""Notification request and response schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NotificationEventType(StrEnum):
    incident_created = "incident_created"
    critical_incident_created = "critical_incident_created"
    ai_analysis_completed = "ai_analysis_completed"
    incident_status_updated = "incident_status_updated"
    incident_resolved = "incident_resolved"
    resolution_notes_added = "resolution_notes_added"


class NotificationChannel(StrEnum):
    slack = "slack"
    console = "console"


class DeliveryStatus(StrEnum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
    retrying = "retrying"


class RecommendedFixPayload(BaseModel):
    immediate_actions: list[str] = Field(default_factory=list)
    long_term_actions: list[str] = Field(default_factory=list)
    runbook_suggestions: list[str] = Field(default_factory=list)


class NotificationEventRequest(BaseModel):
    event_type: NotificationEventType
    incident_id: str = Field(min_length=1, max_length=50)
    service_name: str = Field(min_length=1, max_length=160)
    severity: str | None = None
    status: str | None = None
    title: str | None = None
    ai_summary: str | None = None
    root_cause: str | None = None
    confidence_score: float | None = Field(default=None, ge=0, le=100)
    recommended_fix: RecommendedFixPayload | None = None
    resolved_by: str | None = None
    resolution_notes: str | None = None
    created_at: datetime | None = None


class DeliveryAttemptResponse(BaseModel):
    id: int
    notification_id: str
    attempt_number: int
    channel: NotificationChannel
    status: DeliveryStatus
    error_message: str | None
    attempted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationResponse(BaseModel):
    id: int
    notification_id: str
    incident_id: str | None
    event_type: str
    channel: NotificationChannel
    message: str
    delivery_status: DeliveryStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationDetailResponse(NotificationResponse):
    delivery_attempts: list[DeliveryAttemptResponse] = Field(
        default_factory=list
    )


class NotificationDeliveryResponse(BaseModel):
    notification_id: str
    delivery_status: DeliveryStatus
    channel: NotificationChannel
    error_message: str | None = None


class SlackTestRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
