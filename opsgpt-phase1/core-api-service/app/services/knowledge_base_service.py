"""Knowledge base persistence and incident similarity matching."""

import re

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.knowledge_base import KnowledgeBase
from app.models.resolution_note import ResolutionNote
from app.schemas.incident_schema import SimilarIncidentResponse
from app.schemas.knowledge_base_schema import KnowledgeBaseCreate
from app.services.audit_service import create_audit_log

WORD_PATTERN = re.compile(r"[a-z0-9]+")


def list_entries(
    db: Session,
    *,
    service_name: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[KnowledgeBase]:
    statement = select(KnowledgeBase)
    if service_name:
        statement = statement.where(
            KnowledgeBase.service_name == service_name
        )
    statement = (
        statement.order_by(KnowledgeBase.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_entry_or_404(db: Session, kb_id: int) -> KnowledgeBase:
    entry = db.get(KnowledgeBase, kb_id)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge base entry not found",
        )
    return entry


def create_entry(
    db: Session,
    payload: KnowledgeBaseCreate,
    *,
    created_by: int,
) -> KnowledgeBase:
    if payload.source_incident_id:
        existing = db.scalar(
            select(KnowledgeBase).where(
                KnowledgeBase.source_incident_id
                == payload.source_incident_id
            )
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A knowledge base entry already exists for this incident",
            )

    entry = KnowledgeBase(**payload.model_dump())
    db.add(entry)
    db.flush()
    create_audit_log(
        db,
        user_id=created_by,
        action="knowledge_base_created",
        entity_type="knowledge_base",
        entity_id=str(entry.id),
        new_value={"title": entry.title, "service_name": entry.service_name},
    )
    db.commit()
    db.refresh(entry)
    return entry


def upsert_from_resolved_incident(
    db: Session,
    incident: Incident,
) -> KnowledgeBase:
    entry = db.scalar(
        select(KnowledgeBase).where(
            KnowledgeBase.source_incident_id == incident.incident_id
        )
    )
    notes = list(
        db.scalars(
            select(ResolutionNote)
            .where(ResolutionNote.incident_id == incident.incident_id)
            .order_by(ResolutionNote.created_at.asc())
        )
    )
    resolution_steps = (
        [{"note": note.notes, "created_at": note.created_at.isoformat()} for note in notes]
        if notes
        else incident.recommended_fix
    )

    if entry is None:
        entry = KnowledgeBase(source_incident_id=incident.incident_id)
        db.add(entry)

    entry.title = incident.title
    entry.service_name = incident.service_name
    entry.root_cause = incident.root_cause
    entry.summary = incident.ai_summary
    entry.resolution_steps = resolution_steps
    return entry


def _keywords(value: str | None) -> set[str]:
    if not value:
        return set()
    return {
        word
        for word in WORD_PATTERN.findall(value.lower())
        if len(word) > 2
    }


def find_similar_incidents(
    db: Session,
    incident: Incident,
) -> list[SimilarIncidentResponse]:
    entries = list(
        db.scalars(
            select(KnowledgeBase).where(
                or_(
                    KnowledgeBase.source_incident_id.is_(None),
                    KnowledgeBase.source_incident_id
                    != incident.incident_id,
                )
            )
        )
    )
    current_keywords = _keywords(incident.root_cause)
    matches: list[SimilarIncidentResponse] = []

    for entry in entries:
        score = 60 if entry.service_name == incident.service_name else 0
        entry_keywords = _keywords(entry.root_cause)
        if current_keywords and entry_keywords:
            overlap = len(current_keywords & entry_keywords)
            keyword_ratio = overlap / len(current_keywords | entry_keywords)
            score += round(keyword_ratio * 40)
        if score == 0:
            continue

        matches.append(
            SimilarIncidentResponse(
                knowledge_base_id=entry.id,
                title=entry.title,
                service_name=entry.service_name,
                root_cause=entry.root_cause,
                summary=entry.summary,
                source_incident_id=entry.source_incident_id,
                similarity_percentage=min(score, 100),
            )
        )

    return sorted(
        matches,
        key=lambda match: match.similarity_percentage,
        reverse=True,
    )
