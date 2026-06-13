"""Incident, timeline, and resolution-note schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class IncidentStatus(StrEnum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class IncidentSeverity(StrEnum):
    critical = "critical"
    warning = "warning"
    informational = "informational"


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


class ResolutionNoteCreate(BaseModel):
    notes: str = Field(min_length=1, max_length=10000)


class TimelineResponse(BaseModel):
    id: int
    incident_id: str
    event_type: str
    message: str
    created_by: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResolutionNoteResponse(BaseModel):
    id: int
    incident_id: str
    notes: str
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentResponse(BaseModel):
    id: int
    incident_id: str
    title: str
    service_name: str
    severity: IncidentSeverity
    status: IncidentStatus
    ai_summary: str | None
    root_cause: str | None
    supporting_evidence: list[Any] | dict[str, Any] | None
    confidence_score: float | None
    recommended_fix: list[Any] | dict[str, Any] | None
    related_alert_ids: list[Any] | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
    resolved_by: int | None

    model_config = ConfigDict(from_attributes=True)


class IncidentDetailResponse(IncidentResponse):
    timeline: list[TimelineResponse] = Field(default_factory=list)
    resolution_notes: list[ResolutionNoteResponse] = Field(default_factory=list)


class SimilarIncidentResponse(BaseModel):
    knowledge_base_id: int
    title: str
    service_name: str
    root_cause: str | None
    summary: str | None
    source_incident_id: str | None
    similarity_percentage: int
