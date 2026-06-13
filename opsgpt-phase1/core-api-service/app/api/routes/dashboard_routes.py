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
from app.services.project_service import accessible_project_ids

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=dict[str, int])
def dashboard_summary(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_summary(
        db,
        project_ids=accessible_project_ids(db, current_user),
    )


@router.get("/severity-counts", response_model=dict[str, int])
def severity_counts(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_severity_counts(
        db,
        accessible_project_ids(db, current_user),
    )


@router.get("/status-counts", response_model=dict[str, int])
def status_counts(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_status_counts(
        db,
        accessible_project_ids(db, current_user),
    )


@router.get("/recent-incidents", response_model=list[IncidentResponse])
def recent_incidents(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[Incident]:
    return get_recent_incidents(
        db,
        limit,
        accessible_project_ids(db, current_user),
    )
