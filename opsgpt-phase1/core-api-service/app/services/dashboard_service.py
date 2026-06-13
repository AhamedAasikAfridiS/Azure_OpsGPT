"""Dashboard aggregate queries."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.incident import Incident

SEVERITIES = ("critical", "warning", "informational")
STATUSES = ("open", "in_progress", "resolved")


def _group_counts(db: Session, column) -> dict[str, int]:
    rows = db.execute(select(column, func.count()).group_by(column)).all()
    return {value: count for value, count in rows}


def get_summary(db: Session) -> dict[str, int]:
    total = db.scalar(select(func.count()).select_from(Incident)) or 0
    active = (
        db.scalar(
            select(func.count())
            .select_from(Incident)
            .where(Incident.status.in_(["open", "in_progress"]))
        )
        or 0
    )
    resolved = (
        db.scalar(
            select(func.count())
            .select_from(Incident)
            .where(Incident.status == "resolved")
        )
        or 0
    )
    critical = (
        db.scalar(
            select(func.count())
            .select_from(Incident)
            .where(Incident.severity == "critical")
        )
        or 0
    )
    return {
        "total_incidents": total,
        "active_incidents": active,
        "resolved_incidents": resolved,
        "critical_incidents": critical,
    }


def get_severity_counts(db: Session) -> dict[str, int]:
    counts = _group_counts(db, Incident.severity)
    return {severity: counts.get(severity, 0) for severity in SEVERITIES}


def get_status_counts(db: Session) -> dict[str, int]:
    counts = _group_counts(db, Incident.status)
    return {status: counts.get(status, 0) for status in STATUSES}


def get_recent_incidents(db: Session, limit: int = 10) -> list[Incident]:
    return list(
        db.scalars(
            select(Incident)
            .order_by(Incident.created_at.desc())
            .limit(limit)
        )
    )
