"""User-facing incident endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, SENIOR_ENGINEER, require_roles
from app.core.security import CurrentUser
from app.db.database import get_db
from app.models.incident import Incident
from app.models.resolution_note import ResolutionNote
from app.models.user import User
from app.schemas.incident_schema import (
    IncidentDetailResponse,
    IncidentResponse,
    IncidentSeverity,
    IncidentStatus,
    IncidentStatusUpdate,
    ResolutionNoteCreate,
    ResolutionNoteResponse,
    SimilarIncidentResponse,
    TimelineResponse,
)
from app.services.incident_service import (
    add_resolution_note,
    get_incident_or_404,
    get_resolution_notes,
    get_timeline,
    list_incidents,
    update_status,
)
from app.services.knowledge_base_service import find_similar_incidents
from app.services.notification_client import send_notification_event

router = APIRouter(prefix="/incidents", tags=["Incidents"])
EditorUser = Annotated[
    User,
    Depends(require_roles(SENIOR_ENGINEER, ADMIN)),
]


@router.get("", response_model=list[IncidentResponse])
def get_incidents(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    incident_status: IncidentStatus | None = Query(default=None, alias="status"),
    severity: IncidentSeverity | None = None,
    service_name: str | None = None,
    search: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Incident]:
    return list_incidents(
        db,
        incident_status=incident_status.value if incident_status else None,
        severity=severity.value if severity else None,
        service_name=service_name,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get("/{incident_id}", response_model=IncidentDetailResponse)
def get_incident(
    incident_id: str,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> IncidentDetailResponse:
    incident = get_incident_or_404(db, incident_id)
    incident_data = IncidentResponse.model_validate(incident).model_dump()
    return IncidentDetailResponse(
        **incident_data,
        timeline=get_timeline(db, incident_id),
        resolution_notes=get_resolution_notes(db, incident_id),
    )


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def change_incident_status(
    incident_id: str,
    payload: IncidentStatusUpdate,
    current_user: EditorUser,
    db: Annotated[Session, Depends(get_db)],
) -> Incident:
    incident = update_status(db, incident_id, payload, current_user)
    event_type = (
        "incident_resolved"
        if incident.status == IncidentStatus.resolved.value
        else "incident_status_updated"
    )
    send_notification_event(
        {
            "event_type": event_type,
            "incident_id": incident.incident_id,
            "service_name": incident.service_name,
            "severity": incident.severity,
            "status": incident.status,
            "title": incident.title,
            "ai_summary": incident.ai_summary,
            "root_cause": incident.root_cause,
            "confidence_score": incident.confidence_score,
            "resolved_by": (
                current_user.email
                if incident.status == IncidentStatus.resolved.value
                else None
            ),
        }
    )
    return incident


@router.post(
    "/{incident_id}/resolution-notes",
    response_model=ResolutionNoteResponse,
    status_code=201,
)
def create_resolution_note(
    incident_id: str,
    payload: ResolutionNoteCreate,
    current_user: EditorUser,
    db: Annotated[Session, Depends(get_db)],
) -> ResolutionNote:
    note = add_resolution_note(
        db,
        incident_id,
        payload.notes,
        current_user,
    )
    incident = get_incident_or_404(db, incident_id)
    send_notification_event(
        {
            "event_type": "resolution_notes_added",
            "incident_id": incident.incident_id,
            "service_name": incident.service_name,
            "severity": incident.severity,
            "status": incident.status,
            "title": incident.title,
            "resolution_notes": note.notes,
        }
    )
    return note


@router.get("/{incident_id}/timeline", response_model=list[TimelineResponse])
def incident_timeline(
    incident_id: str,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    return get_timeline(db, incident_id)


@router.get(
    "/{incident_id}/similar",
    response_model=list[SimilarIncidentResponse],
)
def similar_incidents(
    incident_id: str,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[SimilarIncidentResponse]:
    incident = get_incident_or_404(db, incident_id)
    return find_similar_incidents(db, incident)
