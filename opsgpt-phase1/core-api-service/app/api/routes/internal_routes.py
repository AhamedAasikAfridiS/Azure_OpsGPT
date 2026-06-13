"""Trusted service-to-service endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.rbac import verify_internal_api_key
from app.db.database import get_db
from app.models.incident import Incident
from app.models.timeline import IncidentTimeline
from app.schemas.incident_schema import IncidentResponse, TimelineResponse
from app.schemas.internal_schema import (
    InternalAnalysisUpdate,
    InternalIncidentCreate,
    InternalTimelineCreate,
)
from app.schemas.project_schema import MonitoringSourceValidationResponse
from app.services.incident_service import (
    add_internal_timeline_event,
    create_internal_incident,
    update_internal_analysis,
)
from app.services.notification_client import send_notification_event
from app.services.project_service import (
    project_display_name,
    validate_monitoring_source_token,
)

router = APIRouter(
    prefix="/internal",
    tags=["Internal"],
    dependencies=[Depends(verify_internal_api_key)],
)


@router.post(
    "/incidents",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    payload: InternalIncidentCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Incident:
    incident = create_internal_incident(db, payload)
    send_notification_event(
        {
            "event_type": "incident_created",
            "incident_id": incident.incident_id,
            "project_id": incident.project_id,
            "project_name": project_display_name(db, incident.project_id),
            "service_name": incident.service_name,
            "severity": incident.severity,
            "status": incident.status,
            "title": incident.title,
            "ai_summary": incident.ai_summary,
            "root_cause": incident.root_cause,
            "confidence_score": incident.confidence_score,
            "recommended_fix": incident.recommended_fix,
        }
    )
    return incident


@router.patch(
    "/incidents/{incident_id}/analysis",
    response_model=IncidentResponse,
)
def update_analysis(
    incident_id: str,
    payload: InternalAnalysisUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Incident:
    incident = update_internal_analysis(db, incident_id, payload)
    send_notification_event(
        {
            "event_type": "ai_analysis_completed",
            "incident_id": incident.incident_id,
            "project_id": incident.project_id,
            "project_name": project_display_name(db, incident.project_id),
            "service_name": incident.service_name,
            "severity": incident.severity,
            "status": incident.status,
            "title": incident.title,
            "ai_summary": incident.ai_summary,
            "root_cause": incident.root_cause,
            "confidence_score": incident.confidence_score,
        }
    )
    return incident


@router.post(
    "/incidents/{incident_id}/timeline",
    response_model=TimelineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_timeline_event(
    incident_id: str,
    payload: InternalTimelineCreate,
    db: Annotated[Session, Depends(get_db)],
) -> IncidentTimeline:
    return add_internal_timeline_event(db, incident_id, payload)


@router.get(
    "/projects/{project_id}/monitoring-sources/validate",
    response_model=MonitoringSourceValidationResponse,
)
def validate_project_monitoring_source(
    project_id: str,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Query(min_length=1)],
) -> MonitoringSourceValidationResponse:
    source = validate_monitoring_source_token(db, project_id, token)
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid project webhook token",
        )
    return MonitoringSourceValidationResponse(
        valid=True,
        project_id=project_id,
        source_type=source.source_type,
        source_id=source.source_id,
    )
