"""Ingestion event log persistence."""

from sqlalchemy.orm import Session

from app.models.ingestion_log import AlertIngestionLog


def create_ingestion_log(
    db: Session,
    *,
    alert_id: str,
    event_type: str,
    message: str,
) -> AlertIngestionLog:
    log_entry = AlertIngestionLog(
        alert_id=alert_id,
        event_type=event_type,
        message=message,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
