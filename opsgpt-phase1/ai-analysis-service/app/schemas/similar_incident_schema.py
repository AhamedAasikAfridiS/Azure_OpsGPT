"""Rule-based similar incident scoring schemas."""

from pydantic import BaseModel, Field

from app.schemas.alert_schema import AlertSeverity, AlertType


class HistoricalIncident(BaseModel):
    incident_id: str
    service_name: str
    root_cause: str
    alert_types: list[AlertType]
    severity: AlertSeverity
    resolution_summary: str | None = None


class SimilarIncidentRequest(BaseModel):
    service_name: str = Field(min_length=1)
    root_cause: str = Field(min_length=1)
    alert_types: list[AlertType]
    severity: AlertSeverity
    historical_incidents: list[HistoricalIncident]


class SimilarIncidentMatch(HistoricalIncident):
    similarity_percentage: int = Field(ge=0, le=100)


class SimilarIncidentResponse(BaseModel):
    matches: list[SimilarIncidentMatch]
