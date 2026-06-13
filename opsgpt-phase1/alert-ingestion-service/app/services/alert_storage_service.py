"""Raw and normalized alert persistence."""

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.normalized_alert import NormalizedAlert
from app.models.raw_alert import RawAlert
from app.schemas.alert_schema import AlertStatus, NormalizedAlertCreate


def store_raw_alert(
    db: Session,
    *,
    alert_id: str,
    source: str,
    raw_payload: dict[str, Any],
    project_id: str | None = None,
) -> RawAlert:
    raw_alert = RawAlert(
        alert_id=alert_id,
        project_id=project_id,
        source=source,
        raw_payload=raw_payload,
    )
    db.add(raw_alert)
    db.commit()
    db.refresh(raw_alert)
    return raw_alert


def store_normalized_alert(
    db: Session,
    payload: NormalizedAlertCreate,
) -> NormalizedAlert:
    data = payload.model_dump(mode="python")
    if data["threshold"] is not None:
        data["threshold"] = str(data["threshold"])
    normalized_alert = NormalizedAlert(**data)
    db.add(normalized_alert)
    db.commit()
    db.refresh(normalized_alert)
    return normalized_alert


def update_alert_status(
    db: Session,
    alert: NormalizedAlert,
    new_status: AlertStatus,
) -> NormalizedAlert:
    alert.status = new_status.value
    db.commit()
    db.refresh(alert)
    return alert


def list_normalized_alerts(
    db: Session,
    *,
    source: str | None = None,
    alert_status: str | None = None,
    service_name: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[NormalizedAlert]:
    statement = select(NormalizedAlert)
    if source:
        statement = statement.where(NormalizedAlert.source == source)
    if alert_status:
        statement = statement.where(NormalizedAlert.status == alert_status)
    if service_name:
        statement = statement.where(
            NormalizedAlert.service_name == service_name
        )
    statement = (
        statement.order_by(NormalizedAlert.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_normalized_alert_or_404(
    db: Session,
    alert_id: str,
) -> NormalizedAlert:
    alert = db.scalar(
        select(NormalizedAlert)
        .where(NormalizedAlert.alert_id == alert_id)
        .order_by(NormalizedAlert.created_at.desc())
    )
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Normalized alert not found",
        )
    return alert


def get_raw_alert_or_404(db: Session, alert_id: str) -> RawAlert:
    raw_alert = db.scalar(
        select(RawAlert)
        .where(RawAlert.alert_id == alert_id)
        .order_by(RawAlert.received_at.desc())
    )
    if raw_alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Raw alert not found",
        )
    return raw_alert
