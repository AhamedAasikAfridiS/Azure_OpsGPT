"""Project, membership, and project-scoped incident endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN, require_roles
from app.core.security import CurrentUser
from app.db.database import get_db
from app.models.incident import Incident
from app.models.project import Project, ProjectMembership
from app.models.user import User
from app.schemas.incident_schema import (
    IncidentDetailResponse,
    IncidentResponse,
    IncidentSeverity,
    IncidentStatus,
)
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectMembershipCreate,
    ProjectMembershipResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.dashboard_service import get_summary
from app.services.incident_service import (
    get_incident_or_404,
    get_resolution_notes,
    get_timeline,
    list_incidents,
)
from app.services.project_service import (
    add_member,
    create_project,
    deactivate_project,
    ensure_project_access,
    get_project_or_404,
    list_members,
    list_projects_for_user,
    remove_member,
    update_project,
)

router = APIRouter(prefix="/projects", tags=["Projects"])
AdminUser = Annotated[User, Depends(require_roles(ADMIN))]


@router.get("", response_model=list[ProjectResponse])
def get_projects(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[Project]:
    return list_projects_for_user(db, current_user)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_project(
    payload: ProjectCreate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    return create_project(db, payload, current_user)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    return ensure_project_access(db, project_id, current_user)


@router.patch("/{project_id}", response_model=ProjectResponse)
def edit_project(
    project_id: str,
    payload: ProjectUpdate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> Project:
    return update_project(db, project_id, payload, current_user)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    deactivate_project(db, project_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMembershipResponse],
)
def get_project_members(
    project_id: str,
    _: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[ProjectMembership]:
    return list_members(db, project_id)


@router.post(
    "/{project_id}/members",
    response_model=ProjectMembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_project_member(
    project_id: str,
    payload: ProjectMembershipCreate,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> ProjectMembership:
    return add_member(db, project_id, payload, current_user)


@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_member(
    project_id: str,
    user_id: int,
    current_user: AdminUser,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    remove_member(db, project_id, user_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{project_id}/dashboard/summary", response_model=dict[str, int])
def project_dashboard_summary(
    project_id: str,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    ensure_project_access(db, project_id, current_user)
    return get_summary(db, project_id=project_id)


@router.get(
    "/{project_id}/incidents",
    response_model=list[IncidentResponse],
)
def get_project_incidents(
    project_id: str,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    incident_status: IncidentStatus | None = Query(default=None, alias="status"),
    severity: IncidentSeverity | None = None,
    service_name: str | None = None,
    search: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Incident]:
    ensure_project_access(db, project_id, current_user)
    return list_incidents(
        db,
        project_id=project_id,
        incident_status=incident_status.value if incident_status else None,
        severity=severity.value if severity else None,
        service_name=service_name,
        search=search,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{project_id}/incidents/{incident_id}",
    response_model=IncidentDetailResponse,
)
def get_project_incident(
    project_id: str,
    incident_id: str,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> IncidentDetailResponse:
    ensure_project_access(db, project_id, current_user)
    incident = get_incident_or_404(db, incident_id)
    if incident.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found in this project",
        )
    incident_data = IncidentResponse.model_validate(incident).model_dump()
    return IncidentDetailResponse(
        **incident_data,
        timeline=get_timeline(db, incident_id),
        resolution_notes=get_resolution_notes(db, incident_id),
    )
