"""Dashboard aggregate queries."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.incident import Incident

SEVERITIES = ("critical", "warning", "informational")
STATUSES = ("open", "in_progress", "resolved")


def _group_counts(
    db: Session,
    column,
    project_ids: list[str] | None = None,
) -> dict[str, int]:
    statement = select(column, func.count()).group_by(column)
    statement = _apply_project_scope(statement, None, project_ids)
    rows = db.execute(statement).all()
    return {value: count for value, count in rows}


def _apply_project_scope(statement, project_id, project_ids):
    if project_id:
        return statement.where(Incident.project_id == project_id)
    if project_ids is not None:
        if not project_ids:
            return statement.where(False)
        return statement.where(Incident.project_id.in_(project_ids))
    return statement


def get_summary(
    db: Session,
    *,
    project_id: str | None = None,
    project_ids: list[str] | None = None,
) -> dict[str, int]:
    total_statement = _apply_project_scope(
        select(func.count()).select_from(Incident),
        project_id,
        project_ids,
    )
    total = db.scalar(total_statement) or 0
    active = (
        db.scalar(
            _apply_project_scope(
                select(func.count())
                .select_from(Incident)
                .where(Incident.status.in_(["open", "in_progress"])),
                project_id,
                project_ids,
            )
        )
        or 0
    )
    resolved = (
        db.scalar(
            _apply_project_scope(
                select(func.count())
                .select_from(Incident)
                .where(Incident.status == "resolved"),
                project_id,
                project_ids,
            )
        )
        or 0
    )
    critical = (
        db.scalar(
            _apply_project_scope(
                select(func.count())
                .select_from(Incident)
                .where(Incident.severity == "critical"),
                project_id,
                project_ids,
            )
        )
        or 0
    )
    return {
        "total_incidents": total,
        "active_incidents": active,
        "resolved_incidents": resolved,
        "critical_incidents": critical,
    }


def get_severity_counts(
    db: Session,
    project_ids: list[str] | None = None,
) -> dict[str, int]:
    counts = _group_counts(db, Incident.severity, project_ids)
    return {severity: counts.get(severity, 0) for severity in SEVERITIES}


def get_status_counts(
    db: Session,
    project_ids: list[str] | None = None,
) -> dict[str, int]:
    counts = _group_counts(db, Incident.status, project_ids)
    return {status: counts.get(status, 0) for status in STATUSES}


def get_recent_incidents(
    db: Session,
    limit: int = 10,
    project_ids: list[str] | None = None,
) -> list[Incident]:
    statement = select(Incident)
    statement = _apply_project_scope(statement, None, project_ids)
    return list(
        db.scalars(
            statement.order_by(Incident.created_at.desc()).limit(limit)
        )
    )
