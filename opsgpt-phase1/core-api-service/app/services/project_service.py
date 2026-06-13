"""Project access, membership, and monitoring source operations."""

import secrets

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.rbac import ADMIN
from app.models.monitoring_source import MonitoringSource
from app.models.incident import Incident
from app.models.project import Project, ProjectMembership
from app.models.user import User
from app.schemas.project_schema import (
    MonitoringSourceCreate,
    MonitoringSourceUpdate,
    ProjectCreate,
    ProjectMembershipCreate,
    ProjectUpdate,
)
from app.services.audit_service import create_audit_log
from app.utils.project_id_generator import (
    generate_project_id,
    generate_source_id,
    generate_webhook_token,
)


def _unique_project_id(db: Session) -> str:
    while True:
        candidate = generate_project_id()
        if db.scalar(
            select(Project.id).where(Project.project_id == candidate)
        ) is None:
            return candidate


def _unique_source_id(db: Session) -> str:
    while True:
        candidate = generate_source_id()
        if db.scalar(
            select(MonitoringSource.id).where(
                MonitoringSource.source_id == candidate
            )
        ) is None:
            return candidate


def accessible_project_ids(db: Session, user: User) -> list[str] | None:
    if user.role == ADMIN:
        return None
    return list(
        db.scalars(
            select(ProjectMembership.project_id).where(
                ProjectMembership.user_id == user.id
            )
        )
    )


def list_projects_for_user(db: Session, user: User) -> list[Project]:
    statement = select(Project)
    project_ids = accessible_project_ids(db, user)
    if project_ids is not None:
        if not project_ids:
            return []
        statement = statement.where(Project.project_id.in_(project_ids))
    return list(
        db.scalars(
            statement.order_by(Project.is_active.desc(), Project.name.asc())
        )
    )


def get_project_or_404(db: Session, project_id: str) -> Project:
    project = db.scalar(
        select(Project).where(Project.project_id == project_id)
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


def ensure_project_access(
    db: Session,
    project_id: str,
    user: User,
) -> Project:
    project = get_project_or_404(db, project_id)
    if user.role == ADMIN:
        return project
    if not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This project is inactive",
        )
    membership = db.scalar(
        select(ProjectMembership.id).where(
            ProjectMembership.project_id == project_id,
            ProjectMembership.user_id == user.id,
        )
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this project",
        )
    return project


def ensure_incident_access(
    db: Session,
    incident: Incident,
    user: User,
) -> None:
    if user.role == ADMIN:
        return
    if not incident.project_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This incident is not assigned to an accessible project",
        )
    ensure_project_access(db, incident.project_id, user)


def create_project(
    db: Session,
    payload: ProjectCreate,
    admin: User,
) -> Project:
    project = Project(
        project_id=_unique_project_id(db),
        created_by=admin.id,
        **payload.model_dump(),
    )
    db.add(project)
    db.flush()
    create_audit_log(
        db,
        user_id=admin.id,
        action="project_created",
        entity_type="project",
        entity_id=project.project_id,
        new_value=payload.model_dump(mode="json"),
    )
    db.commit()
    db.refresh(project)
    return project


def update_project(
    db: Session,
    project_id: str,
    payload: ProjectUpdate,
    admin: User,
) -> Project:
    project = get_project_or_404(db, project_id)
    changes = payload.model_dump(exclude_unset=True)
    old_value = {field: getattr(project, field) for field in changes}
    for field, value in changes.items():
        setattr(project, field, value)
    create_audit_log(
        db,
        user_id=admin.id,
        action="project_updated",
        entity_type="project",
        entity_id=project.project_id,
        old_value=old_value,
        new_value=changes,
    )
    db.commit()
    db.refresh(project)
    return project


def deactivate_project(
    db: Session,
    project_id: str,
    admin: User,
) -> None:
    project = get_project_or_404(db, project_id)
    project.is_active = False
    create_audit_log(
        db,
        user_id=admin.id,
        action="project_deactivated",
        entity_type="project",
        entity_id=project.project_id,
        old_value={"is_active": True},
        new_value={"is_active": False},
    )
    db.commit()


def list_members(db: Session, project_id: str) -> list[ProjectMembership]:
    get_project_or_404(db, project_id)
    return list(
        db.scalars(
            select(ProjectMembership)
            .where(ProjectMembership.project_id == project_id)
            .order_by(ProjectMembership.created_at.asc())
        )
    )


def add_member(
    db: Session,
    project_id: str,
    payload: ProjectMembershipCreate,
    admin: User,
) -> ProjectMembership:
    get_project_or_404(db, project_id)
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    membership = ProjectMembership(
        project_id=project_id,
        **payload.model_dump(),
    )
    db.add(membership)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already assigned to this project",
        ) from exc
    create_audit_log(
        db,
        user_id=admin.id,
        action="project_member_added",
        entity_type="project",
        entity_id=project_id,
        new_value={"user_id": user.id},
    )
    db.commit()
    db.refresh(membership)
    return membership


def remove_member(
    db: Session,
    project_id: str,
    user_id: int,
    admin: User,
) -> None:
    membership = db.scalar(
        select(ProjectMembership).where(
            ProjectMembership.project_id == project_id,
            ProjectMembership.user_id == user_id,
        )
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project membership not found",
        )
    db.delete(membership)
    create_audit_log(
        db,
        user_id=admin.id,
        action="project_member_removed",
        entity_type="project",
        entity_id=project_id,
        old_value={"user_id": user_id},
    )
    db.commit()


def list_monitoring_sources(
    db: Session,
    project_id: str,
) -> list[MonitoringSource]:
    get_project_or_404(db, project_id)
    return list(
        db.scalars(
            select(MonitoringSource)
            .where(MonitoringSource.project_id == project_id)
            .order_by(MonitoringSource.created_at.desc())
        )
    )


def get_monitoring_source_or_404(
    db: Session,
    project_id: str,
    source_id: str,
) -> MonitoringSource:
    source = db.scalar(
        select(MonitoringSource).where(
            MonitoringSource.project_id == project_id,
            MonitoringSource.source_id == source_id,
        )
    )
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring source not found",
        )
    return source


def create_monitoring_source(
    db: Session,
    project_id: str,
    payload: MonitoringSourceCreate,
    admin: User,
) -> MonitoringSource:
    get_project_or_404(db, project_id)
    token = generate_webhook_token()
    source = MonitoringSource(
        source_id=_unique_source_id(db),
        project_id=project_id,
        webhook_token=token,
        webhook_path=f"/alerts/webhook/project/{project_id}/{token}",
        created_by=admin.id,
        **payload.model_dump(mode="python"),
    )
    db.add(source)
    db.flush()
    create_audit_log(
        db,
        user_id=admin.id,
        action="monitoring_source_created",
        entity_type="monitoring_source",
        entity_id=source.source_id,
        new_value={
            "project_id": project_id,
            "source_type": source.source_type,
            "source_name": source.source_name,
        },
    )
    db.commit()
    db.refresh(source)
    return source


def update_monitoring_source(
    db: Session,
    project_id: str,
    source_id: str,
    payload: MonitoringSourceUpdate,
    admin: User,
) -> MonitoringSource:
    source = get_monitoring_source_or_404(db, project_id, source_id)
    changes = payload.model_dump(exclude_unset=True, mode="python")
    old_value = {field: getattr(source, field) for field in changes}
    for field, value in changes.items():
        setattr(source, field, value)
    create_audit_log(
        db,
        user_id=admin.id,
        action="monitoring_source_updated",
        entity_type="monitoring_source",
        entity_id=source.source_id,
        old_value=old_value,
        new_value=changes,
    )
    db.commit()
    db.refresh(source)
    return source


def deactivate_monitoring_source(
    db: Session,
    project_id: str,
    source_id: str,
    admin: User,
) -> None:
    source = get_monitoring_source_or_404(db, project_id, source_id)
    source.is_active = False
    create_audit_log(
        db,
        user_id=admin.id,
        action="monitoring_source_deactivated",
        entity_type="monitoring_source",
        entity_id=source.source_id,
        old_value={"is_active": True},
        new_value={"is_active": False},
    )
    db.commit()


def validate_monitoring_source_token(
    db: Session,
    project_id: str,
    token: str,
) -> MonitoringSource | None:
    project = db.scalar(
        select(Project).where(
            Project.project_id == project_id,
            Project.is_active.is_(True),
        )
    )
    if project is None:
        return None
    sources = list(
        db.scalars(
            select(MonitoringSource).where(
                MonitoringSource.project_id == project_id,
                MonitoringSource.is_active.is_(True),
            )
        )
    )
    return next(
        (
            source
            for source in sources
            if secrets.compare_digest(source.webhook_token, token)
        ),
        None,
    )


def project_display_name(
    db: Session,
    project_id: str | None,
) -> str | None:
    if not project_id:
        return None
    return db.scalar(
        select(Project.name).where(Project.project_id == project_id)
    )
