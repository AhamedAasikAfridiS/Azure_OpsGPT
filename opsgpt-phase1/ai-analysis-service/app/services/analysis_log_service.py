"""Analysis event log persistence."""

from sqlalchemy.orm import Session

from app.models.analysis_log import AnalysisLog


def create_analysis_log(
    db: Session,
    *,
    event_type: str,
    message: str,
    correlation_id: str | None = None,
    alert_id: str | None = None,
) -> AnalysisLog:
    log_entry = AnalysisLog(
        correlation_id=correlation_id,
        alert_id=alert_id,
        event_type=event_type,
        message=message,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
