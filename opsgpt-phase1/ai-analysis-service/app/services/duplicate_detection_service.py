"""Duplicate alert detection."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis_alert import AnalysisAlert
from app.schemas.alert_schema import NormalizedAlertInput
from app.utils.time_window import correlation_cutoff


def find_duplicate_alert(
    db: Session,
    alert: NormalizedAlertInput,
    window_minutes: int,
) -> AnalysisAlert | None:
    same_id = db.scalar(
        select(AnalysisAlert)
        .where(AnalysisAlert.alert_id == alert.alert_id)
        .order_by(AnalysisAlert.received_at.desc())
    )
    if same_id:
        return same_id

    return db.scalar(
        select(AnalysisAlert)
        .where(
            AnalysisAlert.service_name == alert.service_name,
            AnalysisAlert.alert_type == alert.alert_type.value,
            AnalysisAlert.message == alert.message,
            AnalysisAlert.received_at
            >= correlation_cutoff(window_minutes),
        )
        .order_by(AnalysisAlert.received_at.desc())
    )
