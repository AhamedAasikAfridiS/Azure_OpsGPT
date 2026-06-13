"""Incident lifecycle operations."""

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.resolution_note import ResolutionNote
from app.models.timeline import IncidentTimeline
from app.models.user import User
from app.schemas.incident_schema import IncidentStatus, IncidentStatusUpdate
from app.schemas.internal_schema import (
    InternalAnalysisUpdate,
    InternalIncidentCreate,
    InternalTimelineCreate,
)
from app.services.audit_service import create_audit_log
from app.services.knowledge_base_service import upsert_from_resolved_incident
from app.utils.id_generator import generate_incident_id


def get_incident_or_404(db: Session, incident_id: str) -> Incident:
    incident = db.scalar(
        select(Incident).where(Incident.incident_id == incident_id)
    )
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )
    return incident


def list_incidents(
    db: Session,
    *,
    incident_status: str | None = None,
    severity: str | None = None,
    service_name: str | None = None,
    search: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Incident]:
    statement = select(Incident)
    if incident_status:
        statement = statement.where(Incident.status == incident_status)
    if severity:
        statement = statement.where(Incident.severity == severity)
    if service_name:
        statement = statement.where(Incident.service_name == service_name)
    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            or_(
                Incident.incident_id.ilike(search_term),
                Incident.title.ilike(search_term),
                Incident.service_name.ilike(search_term),
            )
        )
    statement = (
        statement.order_by(Incident.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_timeline(db: Session, incident_id: str) -> list[IncidentTimeline]:
    get_incident_or_404(db, incident_id)
    return list(
        db.scalars(
            select(IncidentTimeline)
            .where(IncidentTimeline.incident_id == incident_id)
            .order_by(IncidentTimeline.created_at.asc())
        )
    )


def get_resolution_notes(
    db: Session,
    incident_id: str,
) -> list[ResolutionNote]:
    return list(
        db.scalars(
            select(ResolutionNote)
            .where(ResolutionNote.incident_id == incident_id)
            .order_by(ResolutionNote.created_at.asc())
        )
    )


def create_internal_incident(
    db: Session,
    payload: InternalIncidentCreate,
) -> Incident:
    incident_id = payload.incident_id or generate_incident_id()
    existing = db.scalar(
        select(Incident).where(Incident.incident_id == incident_id)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incident ID already exists",
        )

    incident_data = payload.model_dump(mode="json")
    incident_data["incident_id"] = incident_id
    incident = Incident(**incident_data)
    if incident.status == IncidentStatus.resolved.value:
        incident.resolved_at = datetime.now(timezone.utc)
    db.add(incident)
    db.flush()

    db.add(
        IncidentTimeline(
            incident_id=incident.incident_id,
            event_type="incident_created",
            message="Incident created by AI Analysis Service",
            created_by=None,
        )
    )
    create_audit_log(
        db,
        user_id=None,
        action="internal_incident_created",
        entity_type="incident",
        entity_id=incident.incident_id,
        new_value={
            "title": incident.title,
            "service_name": incident.service_name,
            "severity": incident.severity,
            "status": incident.status,
        },
    )
    if incident.status == IncidentStatus.resolved.value:
        upsert_from_resolved_incident(db, incident)
    db.commit()
    db.refresh(incident)
    return incident


def update_internal_analysis(
    db: Session,
    incident_id: str,
    payload: InternalAnalysisUpdate,
) -> Incident:
    incident = get_incident_or_404(db, incident_id)
    old_value = {
        "ai_summary": incident.ai_summary,
        "root_cause": incident.root_cause,
        "supporting_evidence": incident.supporting_evidence,
        "confidence_score": incident.confidence_score,
        "recommended_fix": incident.recommended_fix,
    }
    analysis_data = payload.model_dump(mode="json")
    for field, value in analysis_data.items():
        setattr(incident, field, value)

    db.add(
        IncidentTimeline(
            incident_id=incident.incident_id,
            event_type="ai_analysis_completed",
            message="AI analysis was completed and stored",
            created_by=None,
        )
    )
    create_audit_log(
        db,
        user_id=None,
        action="incident_analysis_updated",
        entity_type="incident",
        entity_id=incident.incident_id,
        old_value=old_value,
        new_value=analysis_data,
    )
    db.commit()
    db.refresh(incident)
    return incident


def add_internal_timeline_event(
    db: Session,
    incident_id: str,
    payload: InternalTimelineCreate,
) -> IncidentTimeline:
    get_incident_or_404(db, incident_id)
    event = IncidentTimeline(
        incident_id=incident_id,
        event_type=payload.event_type,
        message=payload.message,
        created_by=None,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_status(
    db: Session,
    incident_id: str,
    payload: IncidentStatusUpdate,
    current_user: User,
) -> Incident:
    incident = get_incident_or_404(db, incident_id)
    old_status = incident.status
    incident.status = payload.status.value

    if payload.status == IncidentStatus.resolved:
        incident.resolved_at = datetime.now(timezone.utc)
        incident.resolved_by = current_user.id
        upsert_from_resolved_incident(db, incident)
    elif old_status == IncidentStatus.resolved.value:
        incident.resolved_at = None
        incident.resolved_by = None

    db.add(
        IncidentTimeline(
            incident_id=incident.incident_id,
            event_type="status_updated",
            message=(
                f"Status changed from {old_status} to {incident.status} "
                f"by {current_user.email}"
            ),
            created_by=current_user.id,
        )
    )
    create_audit_log(
        db,
        user_id=current_user.id,
        action="incident_status_updated",
        entity_type="incident",
        entity_id=incident.incident_id,
        old_value={"status": old_status},
        new_value={"status": incident.status},
    )
    db.commit()
    db.refresh(incident)
    return incident


def add_resolution_note(
    db: Session,
    incident_id: str,
    notes: str,
    current_user: User,
) -> ResolutionNote:
    incident = get_incident_or_404(db, incident_id)
    resolution_note = ResolutionNote(
        incident_id=incident.incident_id,
        notes=notes,
        created_by=current_user.id,
    )
    db.add(resolution_note)
    db.add(
        IncidentTimeline(
            incident_id=incident.incident_id,
            event_type="resolution_note_added",
            message=f"Resolution note added by {current_user.email}",
            created_by=current_user.id,
        )
    )
    create_audit_log(
        db,
        user_id=current_user.id,
        action="resolution_note_added",
        entity_type="incident",
        entity_id=incident.incident_id,
        new_value={"notes": notes},
    )
    db.flush()
    if incident.status == IncidentStatus.resolved.value:
        upsert_from_resolved_incident(db, incident)
    db.commit()
    db.refresh(resolution_note)
    return resolution_note
