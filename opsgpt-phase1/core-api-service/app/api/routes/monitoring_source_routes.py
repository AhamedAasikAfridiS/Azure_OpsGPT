"""Admin monitoring source metadata endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, require_roles
from app.db.database import get_db
from app.models.monitoring_source import MonitoringSource
from app.models.user import User
from app.schemas.project_schema import (
    MonitoringSourceCreate,
    MonitoringSourceResponse,
    MonitoringSourceUpdate,
)
from app.services.project_service import (
    create_monitoring_source,
    deactivate_monitoring_source,
    get_monitoring_source_or_404,
    list_monitoring_sources,
    update_monitoring_source,
)

router = APIRouter(
    prefix="/projects/{project_id}/monitoring-sources",
    tags=["Monitoring Sources"],
)
AdminUser = Annotated[User, Depends(require_roles(ADMIN))]


@router.get("", response_model=list[MonitoringSourceResponse])
def get_monitoring_sources(
    project_id: str,
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[MonitoringSource]:
    return list_monitoring_sources(db, project_id)


@router.post(
    "",
    response_model=MonitoringSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_monitoring_source(
    project_id: str,
    payload: MonitoringSourceCreate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> MonitoringSource:
    return create_monitoring_source(db, project_id, payload, current_user)


@router.get(
    "/{source_id}",
    response_model=MonitoringSourceResponse,
)
def get_monitoring_source(
    project_id: str,
    source_id: str,
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> MonitoringSource:
    return get_monitoring_source_or_404(db, project_id, source_id)


@router.patch(
    "/{source_id}",
    response_model=MonitoringSourceResponse,
)
def edit_monitoring_source(
    project_id: str,
    source_id: str,
    payload: MonitoringSourceUpdate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> MonitoringSource:
    return update_monitoring_source(
        db,
        project_id,
        source_id,
        payload,
        current_user,
    )


@router.delete(
    "/{source_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_monitoring_source(
    project_id: str,
    source_id: str,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    deactivate_monitoring_source(
        db,
        project_id,
        source_id,
        current_user,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
