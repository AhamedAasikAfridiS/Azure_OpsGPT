"""Schemas used by trusted internal service endpoints."""

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.incident_schema import IncidentSeverity, IncidentStatus


class InternalIncidentCreate(BaseModel):
    incident_id: str | None = Field(default=None, max_length=50)
    project_id: str | None = Field(default=None, max_length=50)
    title: str = Field(min_length=2, max_length=255)
    service_name: str = Field(min_length=1, max_length=120)
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.open
    ai_summary: str | None = None
    root_cause: str | None = None
    supporting_evidence: list[Any] | dict[str, Any] | None = None
    confidence_score: float | None = Field(default=None, ge=0, le=100)
    recommended_fix: list[Any] | dict[str, Any] | None = None
    related_alert_ids: list[Any] | None = None


class InternalAnalysisUpdate(BaseModel):
    ai_summary: str
    root_cause: str
    supporting_evidence: list[Any] | dict[str, Any]
    confidence_score: float = Field(ge=0, le=100)
    recommended_fix: list[Any] | dict[str, Any]


class InternalTimelineCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=80)
    message: str = Field(min_length=1, max_length=10000)
