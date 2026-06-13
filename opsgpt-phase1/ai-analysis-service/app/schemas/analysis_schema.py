"""AI task and orchestration schemas."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.alert_schema import (
    AlertSeverity,
    NormalizedAlertInput,
    StoredAnalysisAlertResponse,
)
from app.schemas.correlation_schema import CorrelationGroupResponse


class AnalysisStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class RecommendedFix(BaseModel):
    immediate_actions: list[str]
    long_term_actions: list[str]
    runbook_suggestions: list[str]


class AIAnalysisOutput(BaseModel):
    incident_summary: str = Field(min_length=1)
    root_cause: str = Field(min_length=1)
    supporting_evidence: list[str]
    confidence_score: float = Field(ge=0, le=100)
    recommended_fix: RecommendedFix


class SummaryRequest(BaseModel):
    service_name: str = Field(min_length=1)
    severity: AlertSeverity
    alerts: list[NormalizedAlertInput] = Field(min_length=1)


class SummaryResponse(BaseModel):
    incident_summary: str


class RCARequest(BaseModel):
    service_name: str = Field(min_length=1)
    alerts: list[NormalizedAlertInput] = Field(min_length=1)


class RCAResponse(BaseModel):
    root_cause: str
    supporting_evidence: list[str]
    confidence_score: float = Field(ge=0, le=100)


class FixRequest(BaseModel):
    root_cause: str = Field(min_length=1)
    service_name: str = Field(min_length=1)
    severity: AlertSeverity


class FixResponse(BaseModel):
    recommended_fix: RecommendedFix


class AnalysisResultResponse(BaseModel):
    id: int
    incident_id: str
    project_id: str | None
    correlation_id: str
    ai_summary: str | None
    root_cause: str | None
    supporting_evidence: list[Any] | None
    confidence_score: float | None
    recommended_fix: dict[str, Any] | None
    raw_ai_response: dict[str, Any] | None
    analysis_status: AnalysisStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertAnalysisResponse(BaseModel):
    alert: StoredAnalysisAlertResponse
    duplicate: bool
    correlation_group: CorrelationGroupResponse | None
    incident_id: str | None
    analysis_status: str
    error_message: str | None = None


class IncidentAnalysisDebugResponse(BaseModel):
    analysis: AnalysisResultResponse
    correlation_group: CorrelationGroupResponse
