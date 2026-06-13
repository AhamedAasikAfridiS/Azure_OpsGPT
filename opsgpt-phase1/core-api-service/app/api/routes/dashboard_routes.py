"""Dashboard aggregate endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import CurrentUser
from app.db.database import get_db
from app.models.incident import Incident
from app.schemas.incident_schema import IncidentResponse
from app.services.dashboard_service import (
    get_recent_incidents,
    get_severity_counts,
    get_status_counts,
    get_summary,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=dict[str, int])
def dashboard_summary(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_summary(db)


@router.get("/severity-counts", response_model=dict[str, int])
def severity_counts(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_severity_counts(db)


@router.get("/status-counts", response_model=dict[str, int])
def status_counts(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_status_counts(db)


@router.get("/recent-incidents", response_model=list[IncidentResponse])
def recent_incidents(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[Incident]:
    return get_recent_incidents(db, limit)
