"""Explainable Phase 1 alert correlation."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis_alert import AnalysisAlert
from app.models.correlation_group import CorrelationGroup
from app.services.analysis_log_service import create_analysis_log
from app.utils.id_generator import generate_correlation_id
from app.utils.severity_utils import highest_severity, severities_are_close
from app.utils.time_window import correlation_cutoff

ACTIVE_GROUP_STATUSES = {"open", "incident_created", "updated"}

RELATED_ALERT_TYPES = {
    "cpu": {"cpu", "memory", "api_latency", "application_error"},
    "memory": {"cpu", "memory", "api_latency", "application_error"},
    "api_latency": {
        "cpu",
        "memory",
        "api_latency",
        "database",
        "application_error",
    },
    "database": {"database", "api_latency", "application_error"},
    "application_error": {
        "cpu",
        "memory",
        "api_latency",
        "database",
        "application_error",
    },
    "custom": {"custom"},
}


def alert_types_are_related(first: str, second: str) -> bool:
    return second in RELATED_ALERT_TYPES.get(first, {first})


def _generate_unique_correlation_id(db: Session) -> str:
    while True:
        candidate = generate_correlation_id()
        exists = db.scalar(
            select(CorrelationGroup.id).where(
                CorrelationGroup.correlation_id == candidate
            )
        )
        if exists is None:
            return candidate


def _group_alerts(
    db: Session,
    group: CorrelationGroup,
) -> list[AnalysisAlert]:
    if not group.related_alert_ids:
        return []
    return list(
        db.scalars(
            select(AnalysisAlert).where(
                AnalysisAlert.alert_id.in_(group.related_alert_ids),
                AnalysisAlert.is_duplicate.is_(False),
            )
        )
    )


def find_correlation_group(
    db: Session,
    alert: AnalysisAlert,
    window_minutes: int,
) -> CorrelationGroup | None:
    candidates = list(
        db.scalars(
            select(CorrelationGroup)
            .where(
                CorrelationGroup.service_name == alert.service_name,
                CorrelationGroup.environment == alert.environment,
                CorrelationGroup.status.in_(ACTIVE_GROUP_STATUSES),
                CorrelationGroup.updated_at
                >= correlation_cutoff(window_minutes),
            )
            .order_by(CorrelationGroup.updated_at.desc())
        )
    )

    for group in candidates:
        if not severities_are_close(group.severity, alert.severity):
            continue
        existing_alerts = _group_alerts(db, group)
        if not existing_alerts or any(
            alert_types_are_related(item.alert_type, alert.alert_type)
            for item in existing_alerts
        ):
            return group
    return None


def find_group_for_duplicate(
    db: Session,
    duplicate_of: AnalysisAlert,
    window_minutes: int,
) -> CorrelationGroup | None:
    groups = list(
        db.scalars(
            select(CorrelationGroup)
            .where(
                CorrelationGroup.service_name == duplicate_of.service_name,
                CorrelationGroup.environment == duplicate_of.environment,
                CorrelationGroup.status.in_(ACTIVE_GROUP_STATUSES),
                CorrelationGroup.updated_at
                >= correlation_cutoff(window_minutes),
            )
            .order_by(CorrelationGroup.updated_at.desc())
        )
    )
    return next(
        (
            group
            for group in groups
            if duplicate_of.alert_id in group.related_alert_ids
        ),
        None,
    )


def correlate_alert(
    db: Session,
    alert: AnalysisAlert,
    window_minutes: int,
) -> CorrelationGroup:
    group = find_correlation_group(db, alert, window_minutes)
    if group is None:
        group = CorrelationGroup(
            correlation_id=_generate_unique_correlation_id(db),
            service_name=alert.service_name,
            environment=alert.environment,
            severity=alert.severity,
            status="open",
            related_alert_ids=[alert.alert_id],
        )
        db.add(group)
        db.commit()
        db.refresh(group)
        create_analysis_log(
            db,
            correlation_id=group.correlation_id,
            alert_id=alert.alert_id,
            event_type="correlation_group_created",
            message="Created a new correlation group",
        )
        return group

    related_ids = list(group.related_alert_ids)
    if alert.alert_id not in related_ids:
        related_ids.append(alert.alert_id)
        group.related_alert_ids = related_ids
    group.severity = highest_severity([group.severity, alert.severity])
    if group.incident_id:
        group.status = "updated"
    db.commit()
    db.refresh(group)
    create_analysis_log(
        db,
        correlation_id=group.correlation_id,
        alert_id=alert.alert_id,
        event_type="correlation_group_updated",
        message="Attached alert to an existing correlation group",
    )
    return group


def group_has_meaningful_incident_state(
    db: Session,
    group: CorrelationGroup,
) -> bool:
    alerts = _group_alerts(db, group)
    if any(alert.severity == "critical" for alert in alerts):
        return True
    return len({alert.alert_id for alert in alerts}) >= 2


def get_group_alerts(
    db: Session,
    group: CorrelationGroup,
) -> list[AnalysisAlert]:
    return _group_alerts(db, group)
